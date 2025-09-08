# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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