# Roadmap del Módulo: Estado de Cuenta de Cliente

Este documento traza el plan de desarrollo y las futuras mejoras para el módulo `partner_statement_report`.

## Próximas Características (Pendientes)

### Versión 1.6.0
-   [ ] **Wizard de Envío para WhatsApp**: Crear un asistente intermedio (similar al de "Enviar Email") que se active al presionar "Enviar por WhatsApp". Este asistente debería:
    -   Mostrar una previsualización del mensaje final, con todos los placeholders ya reemplazados.
    -   Permitir al usuario seleccionar a qué contacto (hijo) del cliente se enviará el mensaje, buscando por defecto el contacto de tipo "Facturación".

### Versión 1.7.0
-   [ ] **Filtrado por Saldo**: Añadir una opción en el wizard para generar el reporte solo para clientes con saldo pendiente (`total_due > 0`).
-   [ ] **Soporte Multi-Moneda**: Mejorar el reporte para mostrar claramente los saldos en la moneda del cliente y en la moneda de la compañía, si son diferentes.
-   [ ] **Envío Masivo por Email**: Implementar una acción para enviar los estados de cuenta por email a todos los clientes seleccionados de una vez, utilizando una acción de servidor o una cola de trabajos.

## Características Completadas

-   [x] **(v1.5.2) Refinamiento Visual del Reporte**: Múltiples mejoras de CSS y maquetación en la plantilla QWeb.
-   [x] **(v1.5.0) Integración con WhatsApp**: Permitir el envío de un mensaje de WhatsApp con un enlace de descarga seguro y temporal para el estado de cuenta.
-   [x] **(v1.3.0) Envío por Email**: Integración para enviar el estado de cuenta por correo electrónico directamente desde el asistente.
-   [x] **(v1.2.0) Pie de Página Configurable**: Permitir al usuario definir un pie de página personalizado para el reporte desde los ajustes de contabilidad.
-   [x] **(v1.1.0) Mejoras de Usabilidad**: Añadir botón inteligente en la ficha del cliente y opciones de rango de fechas predefinidas.
-   [x] **(v1.0.0) Funcionalidad Base**: Creación del reporte en PDF, wizard de generación y modelo de datos inicial.