# Roadmap del Proyecto

Este documento describe los planes futuros y las posibles mejoras para el módulo de Estado de Cuenta.

---

### ✅ Versión 1.2 - Configuración y Seguridad (Completado)

-   **Panel de Configuración Centralizado**: Se creó una nueva sección en **Ajustes > Contabilidad** para gestionar la configuración del módulo.
-   **Activación por Compañía**: Se implementó la opción para que los administradores activen o desactiven la funcionalidad del estado de cuenta para cada compañía en el entorno.
-   **Gestión de Permisos**: Se creó un grupo de seguridad dedicado ("Generar Estados de Cuenta") para asignar permisos de acceso a la funcionalidad, en lugar de un campo de selección.

---

### 🚀 Próxima Versión: Funcionalidades de Comunicación

-   **Envío por Email Directo**: Añadir un botón "Enviar por Email" en el asistente que generará el PDF y lo adjuntará a un borrador de correo, utilizando una plantilla de email configurable, listo para ser enviado al cliente.
-   **Integración con WhatsApp**: Añadir un botón "Enviar por WhatsApp" que abrirá WhatsApp Web en una nueva pestaña con un mensaje de plantilla predefinido. Este mensaje incluirá un enlace de descarga seguro y temporal para el estado de cuenta.

---

### 📆 Versiones Futuras

-   **Filtro por Saldos**: Añadir una opción en el asistente para generar el reporte únicamente para clientes con saldo pendiente (deudor o a favor).
-   **Generación Masiva Programada**: Crear una acción programada (cron job) para enviar automáticamente los estados de cuenta a fin de mes a los clientes con saldo pendiente.
-   **Mejorar la Descripción de Movimientos**: Analizar y hacer más claras las etiquetas de las facturas y los pagos en la columna "Descripción", mostrando información más relevante si es necesario.