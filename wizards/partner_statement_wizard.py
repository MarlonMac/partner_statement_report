# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta

class PartnerStatementWizard(models.TransientModel):
    _name = 'partner.statement.wizard'
    _description = 'Asistente para Reporte de Estado de Cuenta'

    def _get_default_partners(self):
        if self.env.context.get('active_model') == 'res.partner':
            return self.env.context.get('active_ids', [])
        return []

    date_range_option = fields.Selection([
        ('custom', 'Rango Personalizado'),
        ('last_month', 'Último Mes Completo'),
        ('last_month_to_date', 'Último Mes (a fecha actual)'),
        ('last_3_months', 'Últimos 3 Meses (a fecha actual)'),
        ('last_6_months', 'Últimos 6 Meses (a fecha actual)'),
    ], string='Opción de Rango', default='last_month_to_date', required=True)
    date_from = fields.Date('Desde', required=True, default=lambda self: date.today() - timedelta(days=30))
    date_to = fields.Date('Hasta', required=True, default=fields.Date.today)
    partner_ids = fields.Many2many('res.partner', string='Clientes', required=True, default=_get_default_partners)

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
        
        # El uso del ORM de Odoo para pasar datos al reporte
        # asegura que se respeten las reglas de acceso y multi-compañía,
        # constituyendo una práctica segura.
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('partner_statement_report.action_report_partner_statement').report_action(self, data=data)