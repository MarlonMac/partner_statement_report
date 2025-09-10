# Changelog

Todas las versiones y cambios notables de este módulo serán documentados en este archivo.

## [16.0.1.7.0] - 2025-09-10

### Added
-   **Gestión de Plantillas para WhatsApp**: Se reemplazó el mensaje de texto fijo por un sistema de plantillas (`mail.template`).
-   **Nuevas Plantillas por Defecto**: Se incluyen 3 plantillas iniciales: Mensaje Estándar, Mensaje de Cobro y Notificación de Saldo a Favor.
-   **Configuración Avanzada**: Se añadió una opción en `Ajustes > Contabilidad` para seleccionar la plantilla de WhatsApp por defecto.
-   **Atajo de Gestión**: Se incluyó un botón en los ajustes para acceder directamente a la gestión de plantillas de correo.
-   **Mejora del Wizard de WhatsApp**: El asistente ahora permite seleccionar la plantilla a utilizar antes de enviar el mensaje.

## [16.0.1.6.0]

### Added
-   **Asistente de Envío para WhatsApp**: Al hacer clic en "Enviar por WhatsApp", ahora se abre un asistente intermedio.
-   **Previsualización de Mensaje**: El nuevo asistente muestra el mensaje completo con los placeholders reemplazados antes de enviarlo.
-   **Selección de Contacto**: Se puede seleccionar a qué contacto del cliente (incluyendo los contactos hijos) se enviará el estado de cuenta. El sistema sugiere automáticamente el contacto de tipo "Facturación" si existe.


## [16.0.1.5.2] - 2025-09-09

### Fixed
-   **Maquetación del Reporte**: Se realizaron múltiples ajustes de estilo en la plantilla QWeb para mejorar la consistencia y profesionalismo del PDF.
-   Se eliminaron bordes inconsistentes en el bloque de información del cliente.
-   Se corrigió la superposición de la imagen y el texto del cliente usando una maquetación basada en `float`.
-   Se reestructuró el pie de página para alinear correctamente el texto y centrar la paginación.
-   Se añadió una línea separadora horizontal debajo del título del reporte.
-   Se resaltó la fila del saldo final con los colores corporativos para mayor impacto visual.

## [16.0.1.5.1] - 2025-09-09

### Fixed
-   **Mejora de Usabilidad**: Se optimizaron los textos de ayuda para la configuración de la plantilla de WhatsApp, detallando cada placeholder.
-   **Nuevo Placeholder**: Se añadió `{expiration_days}` a la plantilla de WhatsApp para informar al cliente sobre la validez del enlace.


## [16.0.1.5.0] - 2025-09-09

### Added
-   **Integración Avanzada con WhatsApp**: Se implementó la funcionalidad "Enviar por WhatsApp" que genera un enlace de descarga temporal, público y seguro para el estado de cuenta en PDF.
-   **Controlador Público Seguro**: Se añadió un controlador HTTP para gestionar las descargas de reportes desde enlaces públicos, validando tokens y fechas de expiración.
-   **Configuración de Expiración**: Nueva opción en `Ajustes > Contabilidad` para definir por cuántos días serán válidos los enlaces de descarga.
-   **Limpieza Automática**: Se configuró un trabajo programado (cron) que se ejecuta diariamente para eliminar los enlaces y archivos adjuntos expirados, manteniendo la base de datos limpia.

### Fixed
-   **Permisos de Acceso para Reportes Públicos**: Se solucionó un error crítico de `AccessError` al generar el reporte desde el controlador público. La solución fue ejecutar el proceso de renderizado con el entorno del superusuario para sobrepasar las ACL y Reglas de Registro.
-   **Widget de Vista del Wizard**: Se corrigió un error de `OwlError` en el frontend reemplazando el widget incompatible `many2one_avatar_user` por `many2many_tags_avatar`.
-   **API de Renderizado de Reportes**: Se corrigió la llamada a la función `_render_qweb_pdf` para usar la API de modelo correcta, solucionando un `AttributeError` en el backend.
-   **Carga de Controlador**: Se aseguró la correcta importación del directorio de controladores en el `__init__.py` principal del módulo para resolver un error 404.


## [16.0.1.3.0] - 2025-09-09

### Added
-   **Envío de Email**: Se añadió un botón "Revisar y Enviar Email" en el asistente.
-   **Plantilla de Correo**: Se creó una plantilla de correo para el estado de cuenta.

### Changed
-   **Funcionalidad de Email**: El envío de correo se implementó usando el asistente interactivo (`mail.compose.message`) para gestionar un solo cliente a la vez, en lugar de un envío masivo en segundo plano.

### Fixed
-   **Errores de Renderizado de Plantillas**: Se solucionaron múltiples `ValueError` y fallos silenciosos relacionados con el renderizado de plantillas de correo y la creación de registros `mail.mail`, adoptando el patrón de `mail.compose.message` para mayor estabilidad.

## [16.0.1.2.0] - 2025-09-08

### Added
- **Panel de Configuración**: Nueva sección en `Ajustes > Contabilidad` para gestionar el módulo.
- **Activación por Compañía**: Se añadió un booleano para activar o desactivar la funcionalidad por empresa.
- **Footer Personalizado**: Opción para habilitar y editar un pie de página personalizado en formato HTML.
- **Grupo de Seguridad**: Se creó el grupo `Generar Estados de Cuenta` para controlar el acceso a la funcionalidad.

### Changed
- **Ubicación de Ajustes**: La configuración ahora está integrada dentro de los ajustes de Contabilidad en lugar de ser una pestaña independiente.

### Fixed
- **Error de Carga de Modelos**: Solucionado un `ParseError` al actualizar el módulo, asegurando que los modelos Python se carguen antes que las vistas XML mediante la correcta importación en `__init__.py`.
- **Error de XPath en Ajustes**: Corregido el selector `xpath` para posicionar la vista de ajustes de forma estable usando el `data-key` del módulo de contabilidad.
- **Error de Método en Wizard**: Corregido el nombre del método en la vista del wizard para que coincida con el definido en el modelo Python, solucionando un `ParseError`.
- **Alineación del Pie de Página**: Eliminado un margen innecesario en el footer para que la paginación se alinee correctamente al extremo derecho del reporte.
- **Contenido del Pie de Página**: El pie de página personalizado ahora reemplaza solo el texto de políticas, conservando siempre la paginación.

## [16.0.1.1.1] - 2025-09-08

### Changed
- **Localización para Guatemala**: La descripción de las líneas de factura en el reporte ahora muestra los datos del DTE (Número, Serie, Autorización) para compañías configuradas en Guatemala.

### Fixed
- **Borde en Reporte**: Eliminado un borde negro inconsistente que aparecía en la sección de información del cliente en el reporte PDF.