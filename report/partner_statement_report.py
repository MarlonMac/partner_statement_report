# -*- coding: utf-8 -*-
from odoo import api, models

class PartnerStatementReport(models.AbstractModel):
    _name = 'report.partner_statement_report.report_partner_statement_template'
    _description = 'Motor del Reporte de Estado de Cuenta'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['partner.statement.wizard'].browse(docids)
        partners = wizard.partner_ids

        report_data = []
        for partner in partners:
            # 1. Calcular Saldo Inicial
            domain_initial = [
                ('partner_id', '=', partner.id),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('date', '<', wizard.date_from),
                ('parent_state', '=', 'posted'),
            ]
            initial_lines = self.env['account.move.line'].search(domain_initial)
            initial_balance = sum(initial_lines.mapped('debit')) - sum(initial_lines.mapped('credit'))

            # 2. Obtener Movimientos en el Rango
            domain_moves = [
                ('partner_id', '=', partner.id),
                ('account_id.account_type', '=', 'asset_receivable'),
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('parent_state', '=', 'posted'),
            ]
            move_lines = self.env['account.move.line'].search(domain_moves, order='date asc, id asc')

            # 3. Procesar líneas para el reporte
            lines_data = []
            balance = initial_balance
            for line in move_lines:
                balance += line.debit - line.credit
                lines_data.append({
                    'date': line.date,
                    'document': line.move_id.name,
                    'description': line.name,
                    'debit': line.debit,
                    'credit': line.credit,
                    'balance': balance,
                })

            report_data.append({
                'partner': partner,
                'initial_balance': initial_balance,
                'lines': lines_data,
                'final_balance': balance,
            })
        
        # El uso del ORM de Odoo (search, browse, etc.) previene inyecciones SQL
        # y respeta las reglas de seguridad multi-compañía de forma nativa.
        return {
            'doc_ids': docids,
            'doc_model': 'partner.statement.wizard',
            'docs': wizard,
            'report_data': report_data,
            'company': self.env.company,
        }