# -*- coding: utf-8 -*-
{
    'name': 'Gestor de Estado de Cuenta de Cliente',
    'version': '16.0.1.7.0',
    'summary': 'Genera, envía por email/WhatsApp y gestiona estados de cuenta de clientes.',
    'description': """
        Módulo avanzado para la gestión de estados de cuenta de clientes.
        
        Versión 1.7.0:
        - Implementación de plantillas de mensajes para WhatsApp.
        - Se puede seleccionar entre plantillas (estándar, cobro, saldo a favor).
        - Configuración para plantilla de WhatsApp por defecto en Ajustes de Contabilidad.
        - Atajo para gestionar las plantillas desde la configuración.
    """,
    'author': 'Marlon Macario',
    'category': 'Accounting/Reporting',
    'depends': ['account', 'mail', 'base', 'website'],
    'data': [
        'security/partner_statement_security.xml',
        'security/ir.model.access.csv',
        # 1. Cargar las acciones de reporte primero.
        'report/report_actions.xml',     
        # 2. Ahora sí, cargar los datos que dependen de las acciones.
        'data/statement_mail_template.xml',
        'data/statement_whatsapp_templates.xml',
        'data/ir_cron_data.xml',        
        # 3. Cargar el resto de las vistas y asistentes.
        'wizards/partner_statement_wizard_views.xml',
        'wizards/whatsapp_statement_wizard_views.xml',
        'report/report_templates.xml',
        'views/partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}