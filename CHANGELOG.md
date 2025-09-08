# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-09-08

### Added

-   Creación inicial del módulo `partner_statement_report`.
-   Asistente (wizard) para la generación de reportes con selección de clientes y rangos de fechas (predeterminados y personalizados).
-   Lógica en Python para calcular el saldo inicial, movimientos del periodo y saldo final.
-   Plantilla QWeb para la generación de un reporte PDF profesional.
-   Botón de acceso rápido en la ficha del `res.partner`.
-   Nombre de archivo dinámico para el PDF descargado.
-   Archivos de seguridad y vistas necesarios para la operación del módulo.