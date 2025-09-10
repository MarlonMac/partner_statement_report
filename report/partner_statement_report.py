# -*- coding: utf-8 -*-
from odoo import models, api
from collections import defaultdict

class PartnerStatementReport(models.AbstractModel):
    # --- NOMBRE CORREGIDO Y SIMPLIFICADO ---
    _name = 'report.partner_statement_report.statement_template'
    _description = 'Partner Statement Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        wizard = self.env['partner.statement.wizard'].browse(docids[0])
        partners = wizard.partner_ids
        date_from = wizard.date_from
        date_to = wizard.date_to
        company = wizard.company_id

        docs = []
        for partner in partners:
            domain = [
                ('partner_id', '=', partner.id),
                ('move_type', 'in', ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']),
                ('state', '=', 'posted'),
                ('date', '<=', date_to),
            ]
            
            moves = self.env['account.move'].search_read(
                domain,
                fields=['id', 'name', 'date', 'invoice_date_due', 'move_type', 'amount_total_signed', 'amount_residual_signed'],
                order='date asc, id asc'
            )

            initial_balance_data = self.env['account.move'].read_group(
                [
                    ('partner_id', '=', partner.id),
                    ('move_type', 'in', ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']),
                    ('state', '=', 'posted'),
                    ('date', '<', date_from),
                ],
                ['amount_total_signed'],
                []
            )
            initial_balance = initial_balance_data[0]['amount_total_signed'] if initial_balance_data and initial_balance_data[0]['amount_total_signed'] else 0.0

            lines = []
            balance = initial_balance
            for move in moves:
                if move['date'] >= date_from:
                    balance += move['amount_total_signed']
                    lines.append({
                        'date': move['date'],
                        'name': move['name'],
                        'due_date': move['invoice_date_due'],
                        'debit': move['amount_total_signed'] if move['amount_total_signed'] > 0 else 0.0,
                        'credit': -move['amount_total_signed'] if move['amount_total_signed'] < 0 else 0.0,
                        'balance': balance,
                    })

            docs.append({
                'partner': partner,
                'lines': lines,
                'initial_balance': initial_balance,
                'final_balance': balance,
            })

        return {
            'doc_ids': partners.ids,
            'doc_model': 'res.partner',
            'docs': docs,
            'company': company,
            'date_from': date_from,
            'date_to': date_to,
        }