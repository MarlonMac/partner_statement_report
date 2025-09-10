# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    # --- Campos restaurados ---
    statement_report_active = fields.Boolean(
        string="Activar Estado de Cuenta",
        default=True
    )
    statement_custom_footer = fields.Boolean(
        string="Pie de Página Personalizado"
    )
    statement_footer_text = fields.Html(
        string="Contenido del Pie de Página"
    )
    
    # --- Campos existentes/nuevos ---
    statement_link_expiration_days = fields.Integer(
        string='Días de Expiración del Enlace',
        default=7,
        help="Número de días que el enlace de descarga del estado de cuenta permanecerá activo."
    )
    statement_whatsapp_template_id = fields.Many2one(
        'mail.template',
        string="Plantilla WhatsApp por Defecto",
        domain="[('is_statement_whatsapp_template', '=', True)]",
        help="Seleccione la plantilla de mensaje por defecto para enviar estados de cuenta por WhatsApp."
    )