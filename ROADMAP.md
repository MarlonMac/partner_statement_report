# Roadmap del Proyecto

Este documento describe los planes futuros y las posibles mejoras para el módulo de Estado de Cuenta.

## Versión 1.2 (Funcionalidades de Comunicación y Configuración)

-   **Envío por Email Directo**: Añadir un botón "Enviar por Email" en el asistente que generará el PDF y lo adjuntará a un borrador de correo, utilizando una plantilla de email configurable, listo para ser enviado al cliente.

-   **Integración con WhatsApp**: Añadir un botón "Enviar por WhatsApp" que abrirá WhatsApp Web en una nueva pestaña con un mensaje de plantilla predefinido. Este mensaje incluirá un enlace de descarga seguro y temporal para el estado de cuenta.

-   **Panel de Configuración Centralizado**: Crear una nueva sección en los **Ajustes Generales** de Odoo para gestionar la configuración del módulo. Esto incluirá:
    -   **Activación por Compañía**: Permitir a los administradores activar o desactivar la funcionalidad del estado de cuenta para cada compañía en el entorno multi-empresa.
    -   **Gestión de Permisos Simplificada**: Un campo para seleccionar el grupo de seguridad autorizado para generar y administrar los reportes, facilitando la gestión de permisos.

## Versiones Futuras

-   **Filtro por Saldos**: Añadir una opción en el asistente para generar el reporte únicamente para clientes con saldo pendiente (deudor o a favor).

-   **Generación Masiva Programada**: Crear una acción programada (cron job) para enviar automáticamente los estados de cuenta a fin de mes a los clientes con saldo pendiente.

-   **Mejorar la Descripción de Movimientos**: Analizar y hacer más claras las etiquetas de las facturas y los pagos en la columna "Descripción", mostrando información más relevante si es necesario.