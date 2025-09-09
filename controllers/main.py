# -*- coding: utf-8 -*-
import logging
from odoo import http, fields, SUPERUSER_ID
from odoo.http import request

_logger = logging.getLogger(__name__)

class StatementDownloadController(http.Controller):

    @http.route('/statement/download/<string:access_token>', type='http', auth="public", website=True)
    def download_statement(self, access_token, **kwargs):
        """
        Permite la descarga pública de un estado de cuenta a través de un token de acceso.
        """
        try:
            # Usamos sudo() aquí para poder encontrar el enlace sin problemas de permisos iniciales
            link = request.env['statement.download.link'].sudo().search([('access_token', '=', access_token)], limit=1)

            if not link or fields.Datetime.now() > link.expiration_date:
                return request.not_found("El enlace de descarga es inválido o ha expirado.")

            # --- SOLUCIÓN PRINCIPAL ---
            # Creamos un nuevo entorno con el usuario administrador (SUPERUSER_ID)
            # para que todo el proceso de renderizado del reporte tenga los permisos necesarios.
            report_env = request.env(user=SUPERUSER_ID)
            
            report_action_id = 'partner_statement_report.action_report_partner_statement'
            wizard_id = link.attachment_id.res_id
            
            # Llamamos a la función de renderizado usando el nuevo entorno con superpoderes
            pdf_content, _ = report_env['ir.actions.report']._render_qweb_pdf(report_action_id, [wizard_id])

            # Preparamos la respuesta para descargar el archivo
            pdf_http_headers = [
                ('Content-Type', 'application/pdf'),
                ('Content-Length', len(pdf_content)),
                ('Content-Disposition', f'attachment; filename="{link.attachment_id.name}";')
            ]
            return request.make_response(pdf_content, headers=pdf_http_headers)

        except Exception as e:
            # Corregimos el manejo de errores para que no falle y registre el error real.
            _logger.error(f"Error al generar el PDF del estado de cuenta público: {e}")
            # Devolvemos una respuesta de error 500 genérica pero funcional.
            return request.make_response(
                "No se pudo generar el estado de cuenta. Por favor, contacte al administrador.",
                headers=[('Content-Type', 'text/plain')],
                status=500
            )