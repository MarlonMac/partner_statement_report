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
        
        _logger.info("--- INICIO REPORTE ESTADO DE CUENTA ---")
        _logger.info("ID del Asistente (docids): %s", docids)
        if not wizard.exists():
            _logger.error("Error: No se encontró el asistente con ID %s", docids)
            return {}

        partners = wizard.partner_ids
        _logger.info("Clientes a procesar: %s", partners.mapped('name'))

        receivable_accounts = self.env['account.account'].search([
            ('account_type', '=', 'asset_receivable'),
            ('company_id', 'in', [self.env.company.id, False]) # Filtro de compañía añadido
        ])
        _logger.info("Cuentas por cobrar encontradas: %s", receivable_accounts.ids)

        report_data = []
        for partner in partners:
            _logger.info("Procesando partner: %s (ID: %s)", partner.name, partner.id)
            
            # 1. Calcular Saldo Inicial
            domain_initial = [
                ('partner_id', '=', partner.id),
                ('account_id', 'in', receivable_accounts.ids),
                ('date', '<', wizard.date_from),
                ('parent_state', '=', 'posted'),
            ]
            initial_lines = self.env['account.move.line'].search(domain_initial)
            initial_balance = sum(initial_lines.mapped('debit')) - sum(initial_lines.mapped('credit'))
            _logger.info("Líneas para saldo inicial: %s. Saldo inicial calculado: %s", len(initial_lines), initial_balance)

            # 2. Obtener Movimientos en el Rango
            domain_moves = [
                ('partner_id', '=', partner.id),
                ('account_id', 'in', receivable_accounts.ids),
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('parent_state', '=', 'posted'),
            ]
            move_lines = self.env['account.move.line'].search(domain_moves, order='date asc, id asc')
            _logger.info("Líneas de movimiento encontradas en el periodo: %s", len(move_lines))

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
        
        _logger.info("Estructura de datos final a enviar al template: %s", report_data)
        _logger.info("--- FIN REPORTE ESTADO DE CUENTA ---")

        return {
            'doc_ids': docids,
            'doc_model': 'partner.statement.wizard',
            'docs': wizard,
            'report_data': report_data,
            'company': self.env.company,
        }