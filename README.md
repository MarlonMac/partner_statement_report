# Reporte de Estado de Cuenta de Cliente

Módulo para Odoo 16 Community Edition que proporciona una herramienta para generar reportes de estado de cuenta detallados para clientes en formato PDF.

## ✨ Características

-   **Asistente Intuitivo**: Un wizard fácil de usar para configurar la generación del reporte.
-   **Filtros de Fecha Flexibles**: Permite seleccionar rangos de fechas predefinidos (último mes, últimos 3 meses, etc.) o un rango personalizado.
-   **Selección de Clientes**: Genere reportes para uno o varios clientes a la vez.
-   **Acceso Rápido**: Un botón en la ficha del cliente permite generar su estado de cuenta con un solo clic.
-   **Nombre de Archivo Dinámico**: El PDF descargado se nombra automáticamente con el formato `Estado de Cuenta - {Nombre del Cliente}.pdf`.
-   **Reporte Profesional**: El PDF generado incluye:
    -   Saldo inicial al comienzo del periodo.
    -   Listado cronológico de facturas y pagos.
    -   Cálculo de saldo en tiempo real por cada movimiento.
    -   Saldo final claro y conciso.
    -   Refleja correctamente saldos a favor del cliente.

## 🚀 Uso# Reporte de Estado de Cuenta de Cliente

Módulo para Odoo 16 Community Edition que proporciona una herramienta para generar reportes de estado de cuenta detallados para clientes en formato PDF.

## ✨ Características

-   **Diseño Ejecutivo y Minimalista**: Reporte con un diseño limpio, profesional y fácil de leer.
-   **Asistente Intuitivo**: Un wizard fácil de usar para configurar la generación del reporte.
-   **Filtros de Fecha Flexibles**: Permite seleccionar rangos de fechas predefinidos o un rango personalizado.
-   **Multi-empresa**: El encabezado muestra dinámicamente el logo y datos de la compañía correspondiente.
-   **Personalización por Cliente**:
    -   Muestra la **imagen del contacto** si está disponible.
    -   Diferencia entre **Nombre Comercial (`x_biz_name`)** y Razón Social.
    -   Muestra datos comerciales como **Lista de Precios** y **Plazos de Pago**.
-   **Claridad Visual**:
    -   Indicadores de color sutiles para cada tipo de transacción (Factura, Pago).
    -   Resumen de saldos y estado de la cuenta (Pendiente, A favor, Al día).
    -   Bloque de totales al final del reporte.
-   **Acceso Rápido**: Un botón en la ficha del cliente permite generar su estado de cuenta con un solo clic.
-   **Nombre de Archivo Dinámico**: El PDF descargado se nombra automáticamente.

## 🚀 Uso

1.  **Desde la ficha del cliente**:
    -   Navegue a la ficha de cualquier cliente en el módulo de `Contactos`.
    -   Haga clic en el botón inteligente "Estado de Cuenta".
    -   Se abrirá el asistente con el cliente actual ya seleccionado.
    -   Elija el rango de fechas y haga clic en "Imprimir PDF".

## 🛠️ Entorno de Despliegue

Este módulo está diseñado y probado para **Odoo 16 Community Edition** en un entorno **Bitnami sobre AWS**.

1.  **Desde la ficha del cliente**:
    -   Navegue a la ficha de cualquier cliente en el módulo de `Contactos`.
    -   Haga clic en el botón inteligente "Estado de Cuenta".
    -   Se abrirá el asistente con el cliente actual ya seleccionado.
    -   Elija el rango de fechas y haga clic en "Imprimir PDF".