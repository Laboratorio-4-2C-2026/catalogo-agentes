---
name: g09-mercadopago-integration
description: Guía la integración de Mercado Pago Checkout Pro con Next.js y PostgreSQL, incluidos pagos y webhooks.
metadata:
  tipo: skill
  area:
  - frontend
  - backend
  fase:
  - desarrollo
  tecnologias:
  - nextjs
  - postgresql
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: 09
  autor:
    nombre: Agustín Martínez
    github: Agustin5421
  responsables:
  - Agustin5421
  madurez: experimental
  relacionados: []
  autor_original: martinacostadev (copia distribuida por NeverSight)
---

# Mercado Pago Checkout Pro

Guía la integración de Checkout Pro con Next.js y PostgreSQL. Esta versión resume una edición histórica de la skill distribuida por NeverSight, publicada originalmente por martinacostadev. La versión original posterior cambió su alcance y medidas de seguridad.

1. Identificá el país, moneda, SDK oficial, modelo de datos y entorno de pruebas. Consultá la documentación vigente antes de implementar.
2. Creá una compra pendiente en el servidor y una preferencia de pago; mantené los tokens secretos exclusivamente en el servidor.
3. Redirigí al comprador a Mercado Pago y mostrale los estados de éxito, rechazo y pago pendiente.
4. Procesá las notificaciones con validación de autenticidad, idempotencia y comprobación del estado, importe y moneda mediante fuentes confiables. No consideres aprobado un pago solo por la redirección.
5. Probá casos exitosos, pendientes, rechazados, notificaciones repetidas y errores antes de habilitar producción.

## Ejemplo de uso

**Pedido:** Integrá Checkout Pro en mi aplicación Next.js con PostgreSQL.

**Resultado:** Propone el flujo de pago, persistencia, notificaciones y validación adaptado al proyecto.
