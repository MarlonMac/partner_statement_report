# -*- coding: utf-8 -*-
{
    'name': 'Reporte de Estado de Cuenta de Cliente',
    'version': '16.0.1.2.0',
    'summary': 'Genera un reporte PDF con el estado de cuenta detallado de clientes.',
    'description': """
        Este módulo añade la funcionalidad para generar estados de cuenta de clientes en PDF.
        Permite seleccionar rangos de fechas y muestra un historial cronológico de 
        facturas, pagos y saldos, incluyendo saldos a favor.

        Versión 1.2.0:
        - Panel de configuración en Ajustes Generales.
        - Activación de funcionalidad por compañía.
        - Opción de footer personalizado.
        - Grupo de seguridad para controlar el acceso.
    """,
    'author': 'Marlon Macario',
    'category': 'Accounting/Reporting',
    'depends': ['account', 'base'],
    'data': [
        'security/partner_statement_security.xml',
        'security/ir.model.access.csv',
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