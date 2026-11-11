---
name: g12-actualizar-modelo-de-datos
description: Crea o actualiza el documento del modelo de datos de un proyecto (diagrama ER en Mermaid más notas) a partir de las migraciones reales de la rama principal, marcando qué cambió desde la versión anterior y cualquier diferencia entre migraciones y modelos del código. Usar cuando se mergea una migración o antes de diseñar algo que toca la base.
owner: '@lucasmonteverdi1'
role: tl
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - backend
  - documentacion
  fase:
  - diseno
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: usado-en-proyecto
  relacionados:
  - g12-preparar-deploy
---

# Actualizar el modelo de datos

## Para qué

Un modelo de datos documentado que quedó atrás de las migraciones es peor que ninguno:
alguien diseña sobre él. Esta skill lo reconstruye desde lo que de verdad existe y deja a la
vista lo que cambió.

## Entrada

- El repo de la aplicación, actualizado a la rama principal.
- El documento existente, si lo hay. Si no se indica, buscar un `erDiagram` de Mermaid o un
  archivo de modelo de datos en el repo (o en el repo de documentación del proyecto) y
  preguntar si es ese. Si no hay, se crea uno nuevo donde el usuario diga.

## Pasos

1. Actualizar la rama principal y anotar el último merge (`git log -1 --merges`).
2. Ubicar las migraciones (Flyway, Liquibase, Prisma, Alembic, Rails, Knex, etc.) y leerlas
   **todas** en orden. Son la autoridad, no los modelos: es lo que existe en la base. Si el
   proyecto no tiene migraciones y el esquema lo genera el ORM, decirlo y usar los modelos.
3. Armar tablas, columnas (tipo, `PK`, `FK`, `UK`, largos, `NOT NULL` relevantes) y relaciones
   con su cardinalidad. Un `ALTER` o `DROP` posterior pisa lo anterior.
4. Cruzar contra los modelos del ORM. Cada diferencia es un **hallazgo**: campo en el modelo
   sin migración, tabla migrada sin modelo, tipos o largos que no coinciden. Se lista, no se
   corrige.
5. Comparar contra el documento anterior: qué tablas o columnas aparecen, cambian o
   desaparecen, y en qué migración.

## Salida

Escribir el documento manteniendo la forma del existente (o, si es nuevo: encabezado,
diagrama `erDiagram`, notas por tabla solo donde aporten). El encabezado dice fecha, último
merge y las migraciones de las que sale. Al final, dos secciones cortas:

- **Cambios desde la versión anterior** — una línea por cambio, con la migración.
- **Diferencias con el código** — solo si hay.

Mostrar el diff antes de commitear, y no commitear sin que el usuario lo pida.

## Qué no hace

No crea migraciones ni toca modelos. Si una diferencia va a impedir el arranque (el ORM
valida el esquema y no coincide), lo dice primero, arriba de todo.

## Ejemplo de uso

**Pedido:** Se mergeó una migración nueva, actualizá el modelo de datos.

**Resultado:** Reescribe el diagrama ER en Mermaid desde las migraciones de main, con la lista de cambios desde la versión anterior y las diferencias con los modelos del ORM, y muestra el diff sin commitear.
