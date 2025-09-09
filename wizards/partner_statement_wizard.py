# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta

_logger = logging.getLogger(__name__)

class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'
    _description = 'Asistente para Reporte de Estado de Cuenta'

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