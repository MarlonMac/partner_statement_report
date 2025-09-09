# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class StatementDownloadLink(models.Model):
    _name = 'statement.download.link'
    _description = 'Enlace de Descarga Temporal para Estado de Cuenta'

    access_token = fields.Char(
        string='Token de Acceso',
        required=True,
        index=True,
        default=lambda self: str(uuid.uuid4()),
        copy=False
    )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='Adjunto',
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True
    )
    expiration_date = fields.Datetime(
        string='Fecha de Expiración',
        required=True
    )

    _sql_constraints = [
        ('access_token_uniq', 'unique (access_token)', 'El token de acceso debe ser único.')
    ]

    @api.model
    def _get_link_expiration_days(self):
        """Obtiene los días de expiración desde la configuración de la compañía."""
        company = self.env.company
        return company.statement_link_expiration_days or 2

    def create_statement_link(self, attachment, partner):
        """Crea un nuevo enlace de descarga para un adjunto y cliente."""
        expiration_days = self._get_link_expiration_days()
        expiration_date = fields.Datetime.now() + relativedelta(days=expiration_days)
        
        link = self.create({
            'attachment_id': attachment.id,
            'partner_id': partner.id,
            'expiration_date': expiration_date,
        })
        return link

    @api.model
    def _cron_cleanup_expired_links(self):
        """Limpia los enlaces y adjuntos expirados."""
        expired_links = self.search([('expiration_date', '<=', fields.Datetime.now())])
        _logger.info(f"Limpiando {len(expired_links)} enlaces de estado de cuenta expirados.")
        
        # attachments_to_delete = expired_links.mapped('attachment_id')
        # attachments_to_delete.unlink() # El ondelete='cascade' en el attachment_id debería encargarse de esto
        
        expired_links.unlink()