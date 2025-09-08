# Reporte de Estado de Cuenta de Cliente para Odoo 16

Este módulo para Odoo 16 Community Edition provee una solución completa para generar, configurar y gestionar reportes de estado de cuenta de clientes en formato PDF.

## Características Principales

- **Reporte Detallado**: Genera un PDF con el historial cronológico de transacciones (facturas, notas de crédito, pagos) de un cliente dentro de un rango de fechas específico.
- **Cálculo de Saldos**: Muestra el saldo inicial, los movimientos del periodo y el saldo final, identificando claramente si el cliente tiene un saldo pendiente o a favor.
- **Acceso Rápido**: Añade un botón "Estado de Cuenta" directamente en la ficha del cliente para un acceso rápido y contextual.
- **Diseño Limpio y Profesional**: La plantilla del reporte está diseñada para ser clara, legible y personalizable.
- **Soporte Multi-Empresa**: La configuración se gestiona por compañía, permitiendo diferentes ajustes en entornos multi-empresa.
- **Localización para Guatemala**: Para compañías guatemaltecas, la descripción de las facturas muestra automáticamente la información del DTE (Número, Serie y Autorización).

## Configuración

Para configurar el módulo, navega a **Ajustes > Contabilidad** y encontrarás la sección **"Estado de Cuenta de Cliente"**.

Las opciones disponibles son:

- **Activar Estado de Cuenta**: Permite activar o desactivar globalmente la funcionalidad del reporte para la compañía actual.
- **Usar Pie de Página Personalizado**:
    - Si está desmarcado, el reporte usará un pie de página con una política de pagos estándar.
    - Si está marcado, aparecerá un editor de texto que te permitirá diseñar un pie de página personalizado usando formato HTML. El número de página se conservará en ambos casos.

## Permisos y Seguridad

El acceso a la funcionalidad de este módulo está controlado por un grupo de seguridad.

- **Grupo**: `Generar Estados de Cuenta`
- **Para dar acceso**:
    1. Ve a **Ajustes > Usuarios y Compañías > Grupos**.
    2. Busca y abre el grupo "Generar Estados de Cuenta".
    3. En la pestaña "Usuarios", añade a todos los usuarios que necesiten generar estos reportes.

Los usuarios que no pertenezcan a este grupo no verán el botón "Estado de Cuenta" ni podrán acceder al asistente.

## Instalación

1.  Copia la carpeta `partner_statement_report` en tu directorio de addons personalizados.
2.  Reinicia el servicio de Odoo.
3.  Ve a **Aplicaciones**, haz clic en "Actualizar Lista de Aplicaciones".
4.  Busca "Reporte de Estado de Cuenta de Cliente" e instálalo.