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