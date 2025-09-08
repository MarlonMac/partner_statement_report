# -*- coding: utf-8 -*-
import logging
from odoo import api, models

_logger = logging.getLogger(__name__)

class PartnerStatementReport(models.AbstractModel):
    _name = 'report.partner_statement_report.statement_template'
    _description = 'Motor del Reporte de Estado de Cuenta'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['partner.statement.wizard'].browse(docids)
        partners = wizard.partner_ids

        receivable_accounts = self.env['account.account'].search([
            ('account_type', '=', 'asset_receivable'),
            ('company_id', 'in', [self.env.company.id, False])
        ])

        report_data = []
        for partner in partners:
            domain_initial = [
                ('partner_id', '=', partner.id),
                ('account_id', 'in', receivable_accounts.ids),
                ('date', '<', wizard.date_from),
                ('parent_state', '=', 'posted'),
            ]
            initial_lines = self.env['account.move.line'].search(domain_initial)
            initial_balance = sum(initial_lines.mapped('debit')) - sum(initial_lines.mapped('credit'))

            domain_moves = [
                ('partner_id', '=', partner.id),
                ('account_id', 'in', receivable_accounts.ids),
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('parent_state', '=', 'posted'),
            ]
            move_lines = self.env['account.move.line'].search(domain_moves, order='date asc, id asc')

            lines_data = []
            balance = initial_balance

            total_debit = 0.0
            total_credit = 0.0
            
            for line in move_lines:
                balance += line.debit - line.credit
                total_debit += line.debit
                total_credit += line.credit
                
                line_type = 'Asiento Manual'
                if line.move_id.move_type == 'out_invoice':
                    line_type = 'Factura'
                elif line.move_id.move_type == 'out_refund':
                    line_type = 'Nota de Crédito'
                elif line.payment_id:
                    line_type = 'Pago'

                lines_data.append({
                    'date': line.date,
                    'document': line.move_id.name,
                    'description': line.name,
                    'debit': line.debit,
                    'credit': line.credit,
                    'balance': balance,
                    'type': line_type,
                })

            report_data.append({
                'partner': partner,
                'initial_balance': initial_balance,
                'lines': lines_data,
                'final_balance': balance,
                'total_debit': total_debit,
                'total_credit': total_credit,
            })
        
        return {
            'doc_ids': docids,
            'doc_model': 'partner.statement.wizard',
            'docs': wizard,
            'report_data': report_data,
            'company': self.env.company,
        }