---
name: g10-migration-safety-reviewer
description: Revisar una migración de Prisma antes de aplicarla, para detectar drops, columnas no-nullable sin default y otros cambios que puedan romper datos existentes. Usar antes de correr `prisma migrate dev` o `migrate deploy` sobre una base con datos.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - revision
  - despliegue
  tecnologias:
  - prisma
  - postgresql
  - typescript
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
  - g01-prisma-migration-guard
  - g11-revisar-migracion
  - g06-neon-prisma-safety
  - g03-prisma
---
# Migration Safety Reviewer

Revisar los cambios entre la versión anterior y la nueva de `backend/prisma/schema.prisma`, junto con el SQL generado en `backend/prisma/migrations/`, antes de que se apliquen sobre una base con datos (no solo en local vacío).

## Qué revisar

1. Comparar el schema anterior contra el nuevo (usar `git diff` sobre `schema.prisma`) y el SQL de la migración más reciente.
2. Marcar como riesgo alto:
   - `DROP TABLE` o `DROP COLUMN` sobre modelos que ya tienen datos en algún entorno (User, StudentProfile, Subject, Schedule, Trip, TripPassenger, TravelIntent, TravelMatch, University, Campus, Notification). Esta lista cambia seguido: si `schema.prisma` tiene un modelo nuevo que no está acá, tratarlo igual si ya tiene datos en algún entorno.
   - Columnas nuevas `NOT NULL` sin `@default(...)` en el schema (rompe el insert de filas existentes).
   - Cambios de tipo de columna (ej. `String` a `Int`) que puedan truncar o fallar en la conversión.
   - Cambios en relaciones (`onDelete`, claves foráneas) que puedan borrar en cascada datos que antes no se borraban.
3. Revisar si la migración es reversible: si no hay script de rollback ni `prisma migrate diff` guardado, señalarlo.
4. Si el cambio afecta `TravelMatch` o `TravelIntent`, verificar que no invalide matches ya calculados sin un plan de recálculo.

## Salida esperada

Lista de hallazgos con: `cambio` | `tabla/columna` | `riesgo (alto/medio/bajo)` | `por qué` | `mitigación sugerida` (ej. agregar default, migración en dos pasos, backfill antes del deploy).

No ejecutar `prisma migrate` ni modificar el schema: esta skill solo analiza y reporta.

## Ejemplo de uso

**Pedido:** Antes de aplicar esta migración de Prisma en producción, revisá si rompe algo con los datos que ya tenemos.
**Resultado:** Lista de cambios riesgosos de la migración (por ejemplo una columna NOT NULL sin default en Trip) con la mitigación sugerida antes de aplicarla.
