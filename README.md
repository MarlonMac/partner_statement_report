# Reporte de Estado de Cuenta de Cliente para Odoo 16

Este módulo para Odoo 16 Community Edition provee una solución completa para generar, configurar, gestionar y enviar reportes de estado de cuenta de clientes.

## Características Principales

-   **Reporte Detallado**: Genera un PDF con el historial cronológico de transacciones.
-   **Cálculo de Saldos**: Muestra el saldo inicial, los movimientos del periodo y el saldo final.
-   **Envío por Email Interactivo**: Permite enviar el estado de cuenta por email a través del asistente de correo.
-   **Envío por WhatsApp Automatizado**: Abre WhatsApp Web con un mensaje de plantilla que incluye un **enlace de descarga seguro y temporal** para el estado de cuenta en PDF.
-   **Acceso Rápido**: Botón "Estado de Cuenta" en la ficha del cliente.
-   **Diseño Limpio y Profesional**: Plantilla de reporte clara y personalizable.
-   **Configuración por Compañía**: Se integra en **Ajustes de Contabilidad** para activar la funcionalidad, definir un pie de página y configurar plantillas de mensajes.
-   **Localización para Guatemala**: Muestra información del DTE en las descripciones de factura.
-   **Seguridad**: Control de acceso mediante grupos de permisos y generación de reportes públicos de forma segura.

## Uso

### 1. Generar Reporte
-   Ve al menú de **Contactos**, selecciona uno o varios clientes.
-   Haz clic en **Acción > Estado de Cuenta**.
-   O bien, desde la ficha de un solo cliente, haz clic en el botón inteligente **Estado de Cuenta**.
-   Ajusta las fechas en el asistente y haz clic en **Imprimir PDF**.

### 2. Enviar por Email
-   En el asistente, selecciona **un solo cliente**.
-   Haz clic en **Enviar Email**. Se abrirá el compositor de correo de Odoo con el PDF adjunto.

### 3. Enviar por WhatsApp
-   En el asistente, selecciona **un solo cliente** que tenga un número de móvil válido.
-   Haz clic en **Enviar por WhatsApp**.
-   Se abrirá una nueva pestaña de WhatsApp Web con un mensaje precargado que contiene el enlace de descarga del PDF.
-   ¡Simplemente presiona enviar en WhatsApp! El cliente recibirá el mensaje con el enlace para descargar su estado de cuenta.

## Configuración

Para acceder a la configuración, ve a **Ajustes > Contabilidad** y busca la sección "Estado de Cuenta de Cliente".
-   **Activar/Desactivar**: Puedes habilitar o deshabilitar la funcionalidad por compañía.
-   **Pie de Página**: Configura un pie de página personalizado en formato HTML.
-   **Plantilla de WhatsApp**: Edita el mensaje predeterminado. Puedes usar placeholders como `{partner_name}`, `{company_name}`, `{date_from}`, `{date_to}` y `{download_link}`.
-   **Duración del Enlace**: Define cuántos días (por defecto 2) permanecerá activo el enlace de descarga del PDF.

## Permisos y Seguridad

Para dar acceso a un usuario, añádelo al grupo **Generar Estados de Cuenta** desde **Ajustes > Usuarios y Compañías > Grupos**.