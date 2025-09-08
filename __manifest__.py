# -*- coding: utf-8 -*-
{
    'name': 'Reporte de Estado de Cuenta de Cliente',
    'version': '16.0.1.0.0',
    'summary': 'Genera un reporte PDF con el estado de cuenta detallado de clientes.',
    'description': """
        Este módulo añade la funcionalidad para generar estados de cuenta de clientes en PDF.
        Permite seleccionar rangos de fechas y muestra un historial cronológico de 
        facturas, pagos y saldos, incluyendo saldos a favor.
    """,
    'author': 'Marlon Macario',
    'category': 'Accounting/Reporting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/partner_statement_wizard_views.xml',
        'report/report_actions.xml',
        'report/report_templates.xml',
        'views/partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}