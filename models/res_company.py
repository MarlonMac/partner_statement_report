# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    statement_link_expiration_days = fields.Integer(
        string='Días de Expiración del Enlace',
        default=7,
        help="Número de días que el enlace de descarga del estado de cuenta permanecerá activo."
    )
    # Campo obsoleto, reemplazado por la plantilla
    # statement_whatsapp_template = fields.Text(string="Plantilla de Mensaje WhatsApp")
    
    statement_whatsapp_template_id = fields.Many2one(
        'mail.template',
        string="Plantilla WhatsApp por Defecto",
        domain="[('is_statement_whatsapp_template', '=', True)]",
        help="Seleccione la plantilla de mensaje por defecto para enviar estados de cuenta por WhatsApp."
    )