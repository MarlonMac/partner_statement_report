# Reporte de Estado de Cuenta de Cliente para Odoo 16

Este módulo para Odoo 16 Community Edition provee una solución completa para generar, configurar, gestionar y enviar reportes de estado de cuenta de clientes.

## Características Principales

-   **Reporte Detallado**: Genera un PDF con el historial cronológico de transacciones (facturas, notas de crédito, pagos) de un cliente dentro de un rango de fechas específico.
-   **Cálculo de Saldos**: Muestra el saldo inicial, los movimientos del periodo y el saldo final, identificando claramente si el cliente tiene un saldo pendiente o a favor.
-   **Envío de Email Interactivo**: Permite enviar el estado de cuenta a un cliente individual a través del asistente de correo estándar de Odoo, permitiendo la revisión antes del envío.
-   **Acceso Rápido**: Añade un botón "Estado de Cuenta" directamente en la ficha del cliente para un acceso rápido y contextual.
-   **Diseño Limpio y Profesional**: La plantilla del reporte está diseñada para ser clara, legible y personalizable.
-   **Configuración por Compañía**: Se integra en los **Ajustes de Contabilidad**, permitiendo activar la funcionalidad y definir un pie de página personalizado por compañía.
-   **Localización para Guatemala**: Para compañías guatemaltechas, la descripción de las facturas muestra automáticamente la información del DTE (Número, Serie y Autorización).
-   **Seguridad**: El acceso a la funcionalidad está controlado por el grupo de permisos "Generar Estados de Cuenta".

## Uso

1.  **Generar Reporte**:
    * Ve a la ficha de un cliente y haz clic en el botón **Estado de Cuenta**.
    * También puedes ir a **Facturación > Clientes > Estados de Cuenta**.
    * Selecciona uno o más clientes y el rango de fechas.
    * Haz clic en **Imprimir PDF** para descargar el reporte.

2.  **Enviar por Email**:
    * En el asistente, selecciona **un solo cliente**.
    * Haz clic en **Revisar y Enviar Email**.
    * Se abrirá una ventana de correo con el destinatario, el asunto y el PDF ya adjuntos.
    * Revisa el contenido y haz clic en **Enviar**.

## Permisos y Seguridad

Para dar acceso a un usuario, añádelo al grupo **Generar Estados de Cuenta** desde **Ajustes > Usuarios y Compañías > Grupos**.