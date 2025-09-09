# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    statement_report_active = fields.Boolean(
        string="Activar Estado de Cuenta",
        related='company_id.statement_report_active',
        readonly=False,
        help="Activa la funcionalidad del estado de cuenta de cliente."
    )
    statement_custom_footer = fields.Boolean(
        string="Pie de Página Personalizado",
        related='company_id.statement_custom_footer',
        readonly=False,
        help="Permite definir un pie de página personalizado para el reporte."
    )
    statement_footer_text = fields.Html(
        string="Contenido del Pie de Página",
        related='company_id.statement_footer_text',
        readonly=False,
        help="Diseña el contenido que aparecerá en el pie de página."
    )
    statement_whatsapp_template = fields.Text(
        string="Plantilla de Mensaje de WhatsApp",
        related='company_id.statement_whatsapp_template',
        readonly=False,
        help="Define la plantilla para el envío por WhatsApp."
    )
    statement_link_expiration_days = fields.Integer(
        string="Duración del Enlace (días)",
        related='company_id.statement_link_expiration_days',
        readonly=False,
        help="Días que el enlace de descarga del PDF permanecerá activo."
    )