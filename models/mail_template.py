# -*- coding: utf-8 -*-
from odoo import models, fields

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    is_statement_whatsapp_template = fields.Boolean(
        string="Es plantilla de WhatsApp para Estado de Cuenta",
        help="Marque esta casilla si esta plantilla está diseñada para ser usada en el asistente de envío de estados de cuenta por WhatsApp."
    )