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