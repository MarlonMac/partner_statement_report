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

    def send_email_report(self):
        self.ensure_one()
        if not self.partner_ids:
            raise UserError(_('Debe seleccionar al menos un cliente.'))

        template = self.env.ref('partner_statement_report.partner_statement_mail_template')
        sent_partners = []

        for partner in self.partner_ids:
            if not partner.email:
                _logger.warning("Cliente '%s' (ID: %s) no tiene un email configurado. Omitiendo envío.", partner.name, partner.id)
                continue

            wizard_values = {
                'partner_ids': [(6, 0, [partner.id])],
                'date_from': self.date_from,
                'date_to': self.date_to,
                'company_id': self.company_id.id,
            }
            wizard_for_partner = self.env['partner.statement.wizard'].create(wizard_values)
            
            template.send_mail(wizard_for_partner.id, force_send=False)
            sent_partners.append(partner.name)
            _logger.info("Estado de cuenta para '%s' añadido a la cola de envío.", partner.name)
        
        # Devolvemos una notificación al usuario para una mejor UX.
        if sent_partners:
            message = _("Se han añadido a la cola de envío los estados de cuenta para: %s") % (", ".join(sent_partners))
        else:
            message = _("No se pudo enviar ningún correo. Verifique que los clientes seleccionados tengan una dirección de correo electrónico.")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Envío en Proceso'),
                'message': message,
                'sticky': False,
            }
        }