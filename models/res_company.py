# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    statement_report_active = fields.Boolean(
        string="Activar Estado de Cuenta de Cliente",
        default=True,
        help="Si se desmarca, la funcionalidad del estado de cuenta se desactivará para esta compañía."
    )
    statement_custom_footer = fields.Boolean(
        string="Usar Pie de Página Personalizado",
        help="Activa esta opción para reemplazar el pie de página por defecto del reporte."
    )
    statement_footer_text = fields.Html(
        string="Texto del Pie de Página",
        translate=True,
        help="Introduce el contenido personalizado para el pie de página del reporte."
    )
    statement_whatsapp_template = fields.Text(
        string="Plantilla de Mensaje de WhatsApp",
        translate=True,
        default="""Estimado cliente: {partner_name},
Adjunto encontrará su estado de cuenta para el periodo del {date_from} al {date_to}.
Puede descargarlo aquí: {download_link}
_Por políticas de WhatsApp debe agregar este número a sus contactos para que el enlace se active_
_Este enlace estará activo durante {expiration_days} días._
_Si necesita un nuevo enlace, por favor contáctenos._

Saludos cordiales,
{company_name}""",
        help="""Define la plantilla para el envío por WhatsApp. 
Puedes usar los siguientes placeholders:
- {partner_name}: Nombre del cliente
- {company_name}: Nombre de tu compañía
- {date_from}: Fecha de inicio del reporte
- {date_to}: Fecha de fin del reporte
- {download_link}: Enlace de descarga del PDF
- {expiration_days}: Días de validez del enlace"""
    )
    statement_link_expiration_days = fields.Integer(
        string="Duración del Enlace de Descarga (días)",
        default=2,
        help="Número de días que el enlace de descarga del estado de cuenta permanecerá activo."
    )