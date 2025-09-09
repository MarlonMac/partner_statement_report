# -*- coding: utf-8 -*-
import logging
from odoo import http, fields
from odoo.http import request

_logger = logging.getLogger(__name__)

class StatementDownloadController(http.Controller):

    @http.route('/statement/download/<string:access_token>', type='http', auth="public", website=True, is_public=True)
    def download_statement(self, access_token, **kwargs):
        """
        Permite la descarga pública de un estado de cuenta a través de un token de acceso.
        """
        Link = request.env['statement.download.link'].sudo()
        link = Link.search([('access_token', '=', access_token)], limit=1)

        if not link or fields.Datetime.now() > link.expiration_date:
            return request.not_found("El enlace de descarga es inválido o ha expirado.")

        try:
            report_action_id = 'partner_statement_report.action_report_partner_statement'
            wizard_id = link.attachment_id.res_id
            
            pdf_content, _ = request.env['ir.actions.report']._render_qweb_pdf(report_action_id, [wizard_id])

            pdf_http_headers = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf_content)),
                ('Content-Disposition', f'attachment; filename="{link.attachment_id.name}";')
            ]
            return request.make_response(pdf_content, headers=pdf_http_headers)

        except Exception as e:
            _logger.error(f"Error al generar el PDF del estado de cuenta público: {e}")
            return request.server_error("No se pudo generar el estado de cuenta. Por favor, contacte al administrador.")