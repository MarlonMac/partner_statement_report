# -*- coding: utf-8 -*-
{
    'name': 'Reporte de Estado de Cuenta de Cliente',
    'version': '16.0.1.5.0',
    'summary': 'Genera un reporte PDF con el estado de cuenta detallado de clientes y permite enviarlo por email o WhatsApp.',
    'description': """
        Este módulo añade la funcionalidad para generar estados de cuenta de clientes en PDF.
        
        Versión 1.5.0:
        - Envío por WhatsApp con enlace de descarga temporal y seguro para el PDF.
        - Nuevo controlador para gestionar las descargas públicas.
        - Tarea programada (cron) para limpiar enlaces y adjuntos expirados.
        - Configuración de la duración de validez de los enlaces.
    """,
    'author': 'Marlon Macario',
    'category': 'Accounting/Reporting',
    'depends': ['account', 'mail', 'base', 'website'],
    'data': [
        'security/partner_statement_security.xml',
        'security/ir.model.access.csv',
        'data/statement_mail_template.xml',
        'data/ir_cron_data.xml',
        'wizards/partner_statement_wizard_views.xml',
        'report/report_actions.xml',
        'report/report_templates.xml',
        'views/partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}