# Roadmap del Módulo: Gestor Financiero de Clientes

Este documento describe el plan de desarrollo y las futuras características para el módulo.

## Fase 1: Reporte y Envío de Estado de Cuenta (Completada)

- [x] **Versión 1.0.0 - 1.4.0**: Funcionalidad base de generación de reportes PDF.
- [x] **Versión 1.5.0**: Envío de estado de cuenta por WhatsApp con enlace de descarga seguro.
- [x] **Versión 1.6.0**: Asistente intermedio para envío por WhatsApp, con previsualización y selección de contacto.
- [x] **Versión 1.7.0**: Implementación de plantillas de mensajes para WhatsApp y configuración centralizada.

---

## Fase 2: Evolución a Gestor Financiero de Clientes

El enfoque del módulo se expande para convertirse en una herramienta proactiva para la administración de todos los aspectos financieros de la cuenta del cliente.

### Versión 1.8.0 (Planificada): Recordatorios de Pago Automáticos

- [ ] **Motor de Reglas para Recordatorios**: Crear un sistema que permita configurar cuándo enviar recordatorios (ej. X días antes del vencimiento, el día del vencimiento, X días después).
- [ ] **Cron Job Automatizado**: Un proceso automático que evalúe las facturas pendientes y envíe los recordatorios según las reglas.
- [ ] **Configuración por Cliente**: Permitir activar o desactivar los recordatorios automáticos para clientes específicos.
- [ ] **Plantillas de Mensajes para Recordatorios**: Usar el sistema de plantillas `mail.template` para definir los mensajes de los recordatorios.

### Versión 1.9.0 (Planificada): Notificaciones y Log de Cuenta

- [ ] **Motor de Notificaciones**: Crear un sistema para notificar al cliente sobre eventos importantes en su cuenta:
  - Aplicación de una nota de crédito.
  - Registro de un pago.
  - Cambio en sus términos de pago o categoría de cliente.
- [ ] **Log de Comunicaciones**: Añadir una pestaña o widget en la ficha del cliente que registre todos los estados de cuenta y notificaciones enviadas, mostrando la fecha, el canal (Email/WhatsApp) y el usuario que lo envió.

### Versión 2.0.0 (Hito Estratégico): Consolidación y Dashboard

- [ ] **Dashboard de Cuentas por Cobrar**: Una nueva vista o dashboard que resuma la salud de las cuentas por cobrar, mostrando saldos vencidos, promesas de pago, y clientes con mayor riesgo.
- [ ] **Consolidación de Funcionalidades**: Refinar la interfaz de usuario para presentar todas las herramientas (enviar estado de cuenta, registrar comunicación, enviar notificación) en un único lugar cohesivo.
- [ ] **Lanzamiento Mayor**: El lanzamiento de la versión 2.0.0 marcará la transición completa del módulo de una herramienta de reporte a una suite de gestión financiera de clientes.