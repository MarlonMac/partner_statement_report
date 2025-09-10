# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from html import unescape

class WhatsappStatementWizard(models.TransientModel):
    _name = 'whatsapp.statement.wizard'
    _description = 'Asistente para Enviar Estado de Cuenta por WhatsApp'

    def _render_template_body(self, template, wizard_id):
            """Método helper para renderizar y limpiar el cuerpo de la plantilla."""
            if not template or not wizard_id:
                return ''
            
            try:
                # Obtener el wizard para usar como contexto
                wizard = self.env['partner.statement.wizard'].browse(wizard_id)
                if not wizard.exists():
                    return 'Error: No se encontró el wizard de estado de cuenta'
                
                # Método alternativo 1: Usar generate_email (método estándar de Odoo)
                try:
                    email_values = template.generate_email([wizard_id], ['body_html'])
                    body = email_values.get(wizard_id, {}).get('body_html', '')
                except:
                    # Método alternativo 2: Renderizar directamente con el motor Jinja2
                    body = template.body_html or ''
                    if body:
                        # Crear contexto para el renderizado
                        template_ctx = {
                            'object': wizard,
                            'format_date': lambda d: d.strftime('%d/%m/%Y') if d else '',
                            'user': self.env.user,
                            'ctx': self._context,
                        }
                        
                        # Usar el motor de plantillas de Odoo
                        body = template._render_template(body, template.model_id.model, [wizard_id], engine='inline_template')[wizard_id]

                # Limpiar el HTML
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                
                if not body:
                    return 'La plantilla no tiene contenido en el campo "Cuerpo del mensaje"'
                
                # Remover tags HTML y convertir a texto plano para WhatsApp
                # Convertir divs y párrafos a saltos de línea
                clean_message = re.sub(r'<div[^>]*>', '\n', body)
                clean_message = re.sub(r'</div>', '', clean_message)
                clean_message = re.sub(r'<p[^>]*>', '\n', clean_message)
                clean_message = re.sub(r'</p>', '', clean_message)
                clean_message = re.sub(r'<br\s*/?>', '\n', clean_message)
                
                # Preservar texto en negritas y cursivas para WhatsApp
                clean_message = re.sub(r'<strong[^>]*>(.*?)</strong>', r'*\1*', clean_message)
                clean_message = re.sub(r'<b[^>]*>(.*?)</b>', r'*\1*', clean_message)
                clean_message = re.sub(r'<em[^>]*>(.*?)</em>', r'_\1_', clean_message)
                clean_message = re.sub(r'<i[^>]*>(.*?)</i>', r'_\1_', clean_message)
                
                # Remover cualquier otro tag HTML
                clean_message = re.sub(r'<[^>]+>', '', clean_message)
                
                # Decodificar entidades HTML
                clean_message = unescape(clean_message)
                
                # Limpiar espacios excesivos y líneas vacías
                lines = []
                for line in clean_message.split('\n'):
                    line = line.strip()
                    if line:  # Solo agregar líneas no vacías
                        lines.append(line)
                
                result = '\n'.join(lines)
                return result if result else 'La plantilla está vacía después del procesamiento'
                
            except Exception as e:
                # Log del error para debugging
                import logging
                _logger = logging.getLogger(__name__)
                _logger.error(f"Error renderizando plantilla: {e}")
                _logger.error(f"Template ID: {template.id}, Wizard ID: {wizard_id}")
                
                # Como fallback, devolver el contenido crudo de la plantilla
                try:
                    raw_content = template.body_html or 'No hay contenido en la plantilla'
                    return f"[Vista previa sin renderizar]\n{raw_content}"
                except:
                    return f"Error crítico al cargar la plantilla: {str(e)}"
    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        
        # Obtener el wizard activo del contexto
        active_wizard_id = self.env.context.get('active_wizard_id')
        partner_id = self.env.context.get('default_partner_id')
        
        if not partner_id:
            return defaults
            
        partner = self.env['res.partner'].browse(partner_id)
        
        # Buscar contacto de facturación, sino el primer hijo, sino el mismo partner
        billing_contact = partner.child_ids.filtered(lambda c: c.type == 'invoice')
        contact = billing_contact[0] if billing_contact else (partner.child_ids[0] if partner.child_ids else partner)
        
        # Plantilla por defecto de la compañía
        default_template = self.env.company.statement_whatsapp_template_id
        
        # Establecer valores por defecto
        if 'partner_id' in fields_list:
            defaults['partner_id'] = partner_id
        if 'contact_id' in fields_list:
            defaults['contact_id'] = contact.id
        if 'template_id' in fields_list and default_template:
            defaults['template_id'] = default_template.id
            
        # Renderizar mensaje inicial si hay plantilla y wizard
        if 'message' in fields_list and default_template and active_wizard_id:
            defaults['message'] = self._render_template_body(default_template, active_wizard_id)
            
        return defaults
    
    template_id = fields.Many2one(
        'mail.template', 
        string="Plantilla de Mensaje",
        domain="[('is_statement_whatsapp_template', '=', True)]", 
        required=True
    )
    partner_id = fields.Many2one(
        'res.partner', 
        string='Cliente Principal', 
        required=True, 
        readonly=True
    )
    contact_id = fields.Many2one(
        'res.partner', 
        string='Contacto de Envío', 
        required=True,
        domain="['|', ('id', '=', partner_id), ('parent_id', '=', partner_id)]"
    )
    
    contact_type = fields.Selection(
        related='contact_id.type',
        string="Tipo de Contacto",
        readonly=True
    )

    mobile = fields.Char(
        string='Móvil de Envío', 
        related='contact_id.mobile', 
        readonly=False
    )
    message = fields.Text(
        string='Vista Previa del Mensaje', 
        required=True
    )

    @api.onchange('template_id', 'contact_id')
    def _onchange_template_id(self):
        """Actualizar el mensaje cuando cambie la plantilla o el contacto."""
        active_wizard_id = self.env.context.get('active_wizard_id')
        
        if self.template_id and active_wizard_id:
            # Actualizar el contacto en el wizard original si es necesario
            if self.contact_id:
                original_wizard = self.env['partner.statement.wizard'].browse(active_wizard_id)
                if original_wizard.exists():
                    # Aquí podrías actualizar campos adicionales si es necesario
                    pass
            
            # Renderizar el nuevo mensaje
            self.message = self._render_template_body(self.template_id, active_wizard_id)
        else:
            self.message = ''

    def action_send_whatsapp_direct(self):
        """Enviar mensaje por WhatsApp Web."""
        self.ensure_one()
        
        if not self.mobile:
            raise UserError(_('El contacto seleccionado no tiene un número de móvil configurado.'))

        # Limpiar y formatear número de teléfono
        phone_number = re.sub(r'\D', '', self.mobile)
        
        # Agregar código de país si es necesario
        if self.contact_id.country_id and self.contact_id.country_id.phone_code:
            country_code = str(self.contact_id.country_id.phone_code)
            if not phone_number.startswith(country_code):
                phone_number = country_code + phone_number

        # Codificar mensaje para URL
        encoded_message = quote(self.message or '')
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }