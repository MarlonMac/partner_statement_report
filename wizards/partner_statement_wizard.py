# -*- coding: utf-8 -*-
import logging
import re
import base64
from urllib.parse import quote
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta

_logger = logging.getLogger(__name__)

class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'
    _description = 'Asistente para Generar Estado de Cuenta'
    
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    date_range_option = fields.Selection([
        ('custom', 'Rango Personalizado'),
        ('last_month', 'Último Mes Completo'),
        ('last_month_to_date', 'Último Mes (a fecha actual)'),
        ('last_3_months', 'Últimos 3 Meses (a fecha actual)'),
        ('last_6_months', 'Últimos 6 Meses (a fecha actual)'),
    ], string='Opción de Rango', default='last_month_to_date', required=True)
    date_from = fields.Date('Desde', required=True, default=lambda self: date.today() - timedelta(days=30))
    date_to = fields.Date('Hasta', required=True, default=fields.Date.today)
    partner_ids = fields.Many2many('res.partner', string='Clientes', required=True, default=lambda self: self.env.context.get('active_ids', []) if self.env.context.get('active_model') == 'res.partner' else [])

    @api.onchange('date_range_option')
    def _onchange_date_range_option(self):
        today = date.today()
        if self.date_range_option == 'last_month':
            first_day_current_month = today.replace(day=1)
            last_day_last_month = first_day_current_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            self.date_from = first_day_last_month
            self.date_to = last_day_last_month
        elif self.date_range_option == 'last_month_to_date':
            self.date_from = today - timedelta(days=30)
            self.date_to = today
        elif self.date_range_option == 'last_3_months':
            self.date_from = today - timedelta(days=90)
            self.date_to = today
        elif self.date_range_option == 'last_6_months':
            self.date_from = today - timedelta(days=180)
            self.date_to = today
        else: # custom
            self.date_from = today - timedelta(days=30)
            self.date_to = today

    def print_report(self):
        self.ensure_one()
        if not self.partner_ids:
            raise UserError(_('Debe seleccionar al menos un cliente.'))
        return self.env.ref('partner_statement_report.action_report_partner_statement').report_action(self)

    def action_review_and_send(self):
        self.ensure_one()
        
        if len(self.partner_ids) > 1:
            raise UserError(_('Para revisar y enviar, por favor seleccione solo un cliente a la vez.'))
        if not self.partner_ids:
            raise UserError(_('Debe seleccionar al menos un cliente.'))

        template = self.env.ref('partner_statement_report.partner_statement_mail_template', raise_if_not_found=False)

        ctx = {
            'default_model': 'partner.statement.wizard',
            'default_res_id': self.id,
            'default_use_template': bool(template),
            'default_template_id': template.id if template else False,
            'default_composition_mode': 'comment',
            'force_email': True,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'target': 'new',
            'context': ctx,
        }

    def _generate_statement_pdf(self):
        """Genera el contenido del PDF y su nombre."""
        report_xml_id = 'partner_statement_report.action_report_partner_statement'
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report_xml_id, self.ids)
        
        partner_name = self.partner_ids[0].name.replace('/', '_')
        filename = f"Estado de Cuenta - {partner_name}.pdf"
        
        return pdf_content, filename
    
    def action_send_whatsapp(self):
        self.ensure_one()
        if len(self.partner_ids) != 1:
            raise UserError(_('Para enviar por WhatsApp, por favor seleccione solo un cliente a la vez.'))
        
        partner = self.partner_ids[0]

        # 1. Generar y guardar el PDF
        pdf_content, filename = self._generate_statement_pdf()
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        # 2. Crear el enlace de descarga
        Link = self.env['statement.download.link']
        download_link = Link.create_statement_link(attachment, partner)
        
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if base_url and base_url.startswith('http://'):
            base_url = base_url.replace('http://', 'https://')
        full_download_url = f"{base_url}/statement/download/{download_link.access_token}"

        # 3. Preparar placeholders para la plantilla
        template_placeholders = {
            'partner_name': partner.name,
            'company_name': self.company_id.name,
            'date_from': self.date_from.strftime('%d/%m/%Y'),
            'date_to': self.date_to.strftime('%d/%m/%Y'),
            'download_link': full_download_url,
            'expiration_days': self.company_id.statement_link_expiration_days
        }
        
        # 4. Abrir el wizard intermedio, pasando los placeholders
        ctx = {
            'default_partner_id': partner.id,
            'template_placeholders': template_placeholders, # Nuevo
        }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Enviar Estado de Cuenta por WhatsApp',
            'res_model': 'whatsapp.statement.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
        }