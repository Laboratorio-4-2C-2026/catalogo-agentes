---
name: g10-guard-auth-auditor
description: Revisar que los controllers NestJS tengan el guard de autenticación correcto y que ningún endpoint quede expuesto sin querer. Usar al agregar un controller o endpoint nuevo, o antes de un merge a main.
metadata:
  tipo: skill
  area:
  - backend
  - seguridad
  fase:
  - revision
  tecnologias:
  - nestjs
  - typescript
  - firebase
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-dto-validation-checker
  - g01-session-revocation-adversary
  - g08-firebase-auth-claims-inspector
---
# Guard Auth Auditor

Auditar la cobertura de autenticación de los controllers NestJS del backend, usando como referencia el patrón ya establecido en el proyecto: `@UseGuards(FirebaseAuthGuard)` a nivel de clase (ver `backend/src/trips/trips.controller.ts`) y el decorador `@CurrentUser()` para leer el usuario autenticado.

## Qué revisar

1. Listar todos los archivos `*.controller.ts` del backend.
2. Para cada uno, verificar:
   - Si la clase tiene `@UseGuards(FirebaseAuthGuard)` (o el guard que corresponda al dominio).
   - Si algún método individual tiene `@UseGuards(...)` propio que contradiga o reemplace el de la clase sin que sea intencional.
   - Si existen rutas públicas (login, registro, verificación de email, health checks) que **no deberían** tener guard, y confirmar que están explícitamente excluidas, no simplemente olvidadas.
   - Si un endpoint usa `@CurrentUser()` pero el controller no tiene el guard que lo garantiza (esto rompe en runtime, no en compilación).
3. Señalar cualquier endpoint que reciba un `id` de recurso (trip, subject, schedule) sin validar que pertenezca al usuario autenticado (comparar contra `user.id`, como hace `trips.service.ts` en `findOneOrThrow`).

## Salida esperada

Tabla con columnas: `archivo` | `endpoint` | `guard presente` | `riesgo` | `recomendación`. Marcar como riesgo alto cualquier endpoint sin guard que no esté en la lista de rutas públicas conocidas (auth, registro, verificación de email).

No modificar código: esta skill solo reporta. Aplicar los cambios requiere pedido explícito.

## Ejemplo de uso

**Pedido:** Revisá si todos los controllers del backend de Conexia tienen bien puesto el guard de Firebase antes de mergear.
**Resultado:** Tabla con cada controller, si tiene el guard, y qué endpoints quedarían expuestos si se olvidó.
