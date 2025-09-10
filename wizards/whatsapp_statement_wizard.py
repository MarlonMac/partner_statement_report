# -*- coding: utf-8 -*-

import re
from urllib.parse import quote
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from html import unescape

class WhatsappStatementWizard(models.TransientModel):
    _name = 'whatsapp.statement.wizard'
    _description = 'Asistente para Enviar Estado de Cuenta por WhatsApp'

    @api.model
    def _render_template_body(self, template, wizard_id):
        """Método helper para renderizar y limpiar el cuerpo de la plantilla."""
        if not template or not wizard_id:
            return ''
        
        render_result = template.generate_email(wizard_id, ['body_html'])
        body = render_result.get(wizard_id, {}).get('body_html', '')

        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        clean_message = re.sub(r'<div.*?>|</div>', '\n', body)
        clean_message = re.sub(r'<p.*?>|</p>', '\n', clean_message)
        clean_message = re.sub(r'<br\s*/?>', '\n', clean_message)
        clean_message = re.sub(r'<.*?>', '', clean_message)
        return unescape(clean_message).strip()

    @api.model
    def default_get(self, fields_list):
        defaults = super(WhatsappStatementWizard, self).default_get(fields_list)
        
        active_wizard_id = self.env.context.get('active_wizard_id')
        partner_id = self.env.context.get('default_partner_id')
        
        partner = self.env['res.partner'].browse(partner_id)
        billing_contact = partner.child_ids.filtered(lambda c: c.type == 'invoice')
        contact = billing_contact[0] if billing_contact else (partner.child_ids[0] if partner.child_ids else partner)
        
        default_template = self.env.company.statement_whatsapp_template_id
        if 'message' in fields_list and default_template and active_wizard_id:
            defaults['message'] = self._render_template_body(default_template, active_wizard_id)

        if 'partner_id' in fields_list:
            defaults['partner_id'] = partner_id
        if 'contact_id' in fields_list:
            defaults['contact_id'] = contact.id
        if 'template_id' in fields_list and default_template:
            defaults['template_id'] = default_template.id
            
        return defaults
    
    template_id = fields.Many2one(
        'mail.template', string="Plantilla de Mensaje",
        domain="[('is_statement_whatsapp_template', '=', True)]", required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Cliente Principal', required=True, readonly=True)
    contact_id = fields.Many2one(
        'res.partner', string='Contacto de Envío', required=True,
        domain="['|', ('id', '=', partner_id), ('parent_id', '=', partner_id)]")
    
    contact_type = fields.Selection(
        related='contact_id.type',
        string="Tipo de Contacto",
        readonly=True)

    mobile = fields.Char(
        string='Móvil de Envío', related='contact_id.mobile', readonly=False)
    message = fields.Text(string='Mensaje', required=True)

    @api.onchange('template_id')
    def _onchange_template_id(self):
        active_wizard_id = self.env.context.get('active_wizard_id')
        if self.template_id and active_wizard_id:
            self.message = self._render_template_body(self.template_id, active_wizard_id)
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