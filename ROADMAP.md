# Roadmap del Proyecto

Este documento describe los planes futuros y las posibles mejoras para el módulo de Estado de Cuenta.

---

### ✅ Versión 1.3 - Comunicación (Completado)

-   **Envío por Email Individual**: Se implementó un botón "Revisar y Enviar Email" que abre el asistente de correo de Odoo para enviar un estado de cuenta a un solo cliente, permitiendo la revisión y edición manual antes de enviar.

---

### ✅ Versión 1.2 - Configuración y Seguridad (Completado)

-   **Panel de Configuración Centralizado**: Se creó una nueva sección en **Ajustes > Contabilidad**.
-   **Activación por Compañía**: Implementada la opción para activar/desactivar la funcionalidad.
-   **Gestión de Permisos**: Creado el grupo de seguridad "Generar Estados de Cuenta".

---

### 🚀 Próxima Versión: Funcionalidades Avanzadas


-   **Integración con WhatsApp**: Añadir un botón "Enviar por WhatsApp" que abrirá WhatsApp Web en una nueva pestaña con un mensaje de plantilla predefinido.

---

### 📆 Versiones Futuras

-   **Filtro por Saldos**: Añadir una opción en el asistente para generar el reporte únicamente para clientes con saldo pendiente.

-   **Envío Masivo por Email**: Implementar un segundo botón (ej: "Enviar a Todos por Email") que utilice la cola de correos para enviar los estados de cuenta a todos los clientes seleccionados en segundo plano.
-   **Generación Masiva Programada**: Crear una acción programada (cron job) para enviar automáticamente los estados de cuenta a fin de mes.