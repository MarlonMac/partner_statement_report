# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2025-09-08

### Changed

-   **Rediseño visual completo** del reporte a un estilo ejecutivo y minimalista.
-   Reemplazo de la información del asesor de ventas por **Lista de Precios** y **Plazo de Pago**.
-   **Alineación de layout** mejorada en el encabezado y secciones de resumen.
-   Se eliminaron líneas horizontales innecesarias para un diseño más limpio.
-   Se ajustaron los colores de las barras de estado para ser más sutiles.

### Added

-   **Nombre Comercial (`x_biz_name`)**: El reporte ahora muestra el nombre comercial del cliente si está disponible.
-   **Imagen del Cliente**: Se muestra la foto del contacto a la izquierda de sus datos si existe.
-   **Resumen de Estado**: Se reintrodujo el cuadro de "Estado" (Saldo Pendiente, Saldo a Favor, Al día).
-   **Fila de Totales**: Se añadió un resumen con los totales de cargos y abonos del periodo al final del reporte.
-   **Pie de página** con políticas de pago y numeración de página.

## [1.0.0] - 2025-09-08

### Added

-   Creación inicial del módulo `partner_statement_report`.
-   Asistente (wizard) para la generación de reportes con selección de clientes y rangos de fechas.
-   Lógica en Python para calcular saldos e historial de movimientos.
-   Plantilla QWeb para la generación de un reporte PDF funcional.
-   Botón de acceso rápido en la ficha del `res.partner`.
-   Nombre de archivo dinámico para el PDF descargado.