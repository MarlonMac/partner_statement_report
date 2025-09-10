# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval

class WhatsappStatementWizard(models.TransientModel):
    _name = 'whatsapp.statement.wizard'
    _description = 'Asistente para Enviar Estado de Cuenta por WhatsApp'

    def _default_partner_id(self):
        return self.env['res.partner'].browse(self.env.context.get('default_partner_id'))
    
    def _default_template_id(self):
        return self.env.company.statement_whatsapp_template_id

    def _default_contact_id(self):
        partner = self._default_partner_id()
        if not partner:
            return False
        
        billing_contact = partner.child_ids.filtered(lambda c: c.type == 'invoice')
        if billing_contact:
            return billing_contact[0]
        elif partner.child_ids:
            return partner.child_ids[0]
        return partner
    
    template_id = fields.Many2one(
        'mail.template',
        string="Plantilla de Mensaje",
        domain="[('is_statement_whatsapp_template', '=', True)]",
        default=_default_template_id,
        required=True
    )
    partner_id = fields.Many2one(
        'res.partner', 
        string='Cliente Principal', 
        required=True, 
        default=_default_partner_id,
        readonly=True,
        ondelete='cascade'
    )
    contact_id = fields.Many2one(
        'res.partner', 
        string='Contacto de Envío', 
        required=True,
        default=_default_contact_id,
        domain="['|', ('id', '=', partner_id), ('parent_id', '=', partner_id)]",
        help="Seleccione el contacto (o el cliente principal) al que se enviará el mensaje."
    )
    mobile = fields.Char(
        string='Móvil de Envío', 
        related='contact_id.mobile',
        readonly=False,
        help="Número de móvil del contacto seleccionado. Puede editarlo si es necesario."
    )
    message = fields.Text(
        string='Mensaje', 
        required=True
    )

    @api.model
    def create(self, vals):
        # Cargar el mensaje inicial al crear el wizard
        res = super(WhatsappStatementWizard, self).create(vals)
        if not vals.get('message'):
             res._onchange_template_id()
        return res

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            # Recuperar los placeholders del contexto
            placeholders = self.env.context.get('template_placeholders', {})
            
            # Formatear el cuerpo de la plantilla
            # Usamos `_render_field` para procesar los placeholders correctamente
            body = self.template_id._render_field('body_html', self.ids, compute_lang=True)[self.id]

            # El motor de plantillas puede devolver un objeto 'str' o 'bytes'
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            
            # Rellenar los placeholders personalizados
            formatted_body = body.format(**placeholders)

            # Limpiar HTML y convertir a formato de texto plano para WhatsApp
            # Quitar etiquetas <p>, <div> y saltos de línea
            clean_message = re.sub(r'<div.*?>|</div>', '\n', formatted_body)
            clean_message = re.sub(r'<p.*?>|</p>', '\n', clean_message)
            # Reemplazar <br> con saltos de línea
            clean_message = re.sub(r'<br\s*/?>', '\n', clean_message)
            # Quitar el resto de etiquetas HTML
            clean_message = re.sub(r'<.*?>', '', clean_message)
            # Decodificar entidades HTML como &amp;
            from html import unescape
            clean_message = unescape(clean_message).strip()
            
            self.message = clean_message
        else:
            self.message = ''


    def action_send_whatsapp_direct(self):
        self.ensure_one()
        if not self.mobile:
            raise UserError(_('El contacto seleccionado no tiene un número de móvil configurado.'))

        phone_number = re.sub(r'\D', '', self.mobile)
        if self.contact_id.country_id and self.contact_id.country_id.phone_code:
            country_code = self.contact_id.country_id.phone_code
            if not phone_number.startswith(str(country_code)):
                phone_number = str(country_code) + phone_number

        encoded_message = quote(self.message or '')
        
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }