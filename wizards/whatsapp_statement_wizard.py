# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from html import unescape
import logging

_logger = logging.getLogger(__name__)

class WhatsappStatementWizard(models.TransientModel):
    _name = 'whatsapp.statement.wizard'
    _description = 'Asistente para Enviar Estado de Cuenta por WhatsApp'

    # --- REFACTOR: Método de renderizado simplificado y robusto ---
    def _render_whatsapp_message(self, template, wizard_id):
        """
        Renderiza el cuerpo de la plantilla de correo usando la API estándar de Odoo
        y lo convierte a formato de texto plano para WhatsApp.
        """
        if not template or not wizard_id:
            return ''
        
        try:
            # Usamos el método `_render_template` que es el motor base de Odoo.
            # Es más directo y fiable que `generate_email`.
            # Le pasamos el cuerpo HTML, el modelo y los IDs de los registros.
            rendered_bodies = template._render_template(
                template.body_html,
                'partner.statement.wizard',
                [wizard_id]
            )
            body = rendered_bodies.get(wizard_id, '')

            # Limpiar el HTML para convertirlo en un mensaje de texto plano apto para WhatsApp
            if isinstance(body, bytes):
                body = body.decode('utf-8')

            if not body:
                return 'La plantilla seleccionada no tiene contenido.'

            # Regex para convertir HTML básico a formato de WhatsApp (*bold*, _italic_) y limpiar lo demás.
            clean_message = re.sub(r'<div[^>]*>', '\n', body) # Divs a saltos de línea
            clean_message = re.sub(r'</p>|<br\s*/?>', '\n', clean_message, flags=re.IGNORECASE) # Párrafos y br a saltos de línea
            clean_message = re.sub(r'<strong[^>]*>(.*?)</strong>', r'*\1*', clean_message) # Strong a bold
            clean_message = re.sub(r'<b[^>]*>(.*?)</b>', r'*\1*', clean_message) # B a bold
            clean_message = re.sub(r'<em[^>]*>(.*?)</em>', r'_\1_', clean_message) # Em a italic
            clean_message = re.sub(r'<i[^>]*>(.*?)</i>', r'_\1_', clean_message) # I a italic
            clean_message = re.sub(r'<[^>]+>', '', clean_message) # Eliminar cualquier otra etiqueta
            clean_message = unescape(clean_message) # Decodificar entidades HTML como &nbsp;

            # Limpieza final de espacios y saltos de línea excesivos
            lines = [line.strip() for line in clean_message.split('\n') if line.strip()]
            return '\n'.join(lines)

        except Exception as e:
            _logger.error(f"Error al renderizar la plantilla de WhatsApp (ID: {template.id}) para el wizard (ID: {wizard_id}): {e}")
            return "Error al procesar la plantilla. Revise los logs del servidor."

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        
        active_wizard_id = self.env.context.get('active_wizard_id')
        partner_id = self.env.context.get('default_partner_id')
        
        if not partner_id:
            return defaults
            
        partner = self.env['res.partner'].browse(partner_id)
        
        billing_contact = partner.child_ids.filtered(lambda c: c.type == 'invoice')
        contact = billing_contact[0] if billing_contact else (partner.child_ids[0] if partner.child_ids else partner)
        
        default_template = self.env.company.statement_whatsapp_template_id
        
        if 'partner_id' in fields_list:
            defaults['partner_id'] = partner_id
        if 'contact_id' in fields_list:
            defaults['contact_id'] = contact.id
        if 'template_id' in fields_list and default_template:
            defaults['template_id'] = default_template.id
            
        if 'message' in fields_list and default_template and active_wizard_id:
            defaults['message'] = self._render_whatsapp_message(default_template, active_wizard_id)
            
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

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """Actualizar el mensaje cuando cambie la plantilla."""
        active_wizard_id = self.env.context.get('active_wizard_id')
        
        if self.template_id and active_wizard_id:
            self.message = self._render_whatsapp_message(self.template_id, active_wizard_id)
        else:
            self.message = ''

    def action_send_whatsapp_direct(self):
        """Enviar mensaje por WhatsApp Web."""
        self.ensure_one()
        
        if not self.mobile:
            raise UserError(_('El contacto seleccionado no tiene un número de móvil configurado.'))

        phone_number = re.sub(r'\D', '', self.mobile)
        
        if self.contact_id.country_id and self.contact_id.country_id.phone_code:
            country_code = str(self.contact_id.country_id.phone_code)
            if not phone_number.startswith(country_code):
                phone_number = country_code + phone_number

        encoded_message = quote(self.message or '')
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        # Verificación de seguridad: El mensaje y el número de teléfono son controlados por el usuario
        # y la codificación de la URL (quote) previene la inyección de parámetros. Considero el código seguro.
        
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }