---
name: g04-planeamiento-sprint-tickets
description: Elige qué funcionalidades del backlog de PitStop entran en la semana o el sprint según prioridad, fechas del cronograma y capacidad de 18 SP, sin crear los tickets todavía. Usar cuando se pide planificar la semana, el sprint o qué entra en el próximo corte.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "04"
  autor:
    nombre: Manuel Lostaló
    github: ManuLosta
  colaboradores:
  - nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - ManuLosta
  madurez: usado-en-proyecto
  relacionados:
  - g11-planear-sprint
---

# Planeamiento de sprint en tickets

Define el corte; `g04-ticket-orquestador` crea después los tickets.

## El backlog

`features.yaml` tiene **epicas** (`epics`) y dentro de cada una sus
**funcionalidades** (`features`).

**El orden de los arrays es el orden de prioridad que fijo el PM.** Se respeta:
para llenar la semana se avanza de arriba hacia abajo, primero por epicas y dentro
de cada epica por funcionalidades. No reordenar por conveniencia; si hay un motivo
tecnico para alterar el orden, decirlo y esperar confirmacion.

Los estados siguen el mismo flujo que Linear:

`todo` (sin ticket) → `backlog` (ticket creado) → `in_progress` → `done`, mas `blocked`.

- Solo se planifican funcionalidades en `todo`.
- `backlog` significa que el ticket **ya se subio a Linear**: no se duplica. Lo
  mismo si tiene `ticket_refs`.
- Para `in_progress`, cruzar contra Linear antes de crear mas trabajo.
- Nunca crear trabajo para funcionalidades `done`.
- Una funcionalidad `blocked` no se planifica: se reporta que la bloquea.
- Las epicas con `moscow: could` estan **fuera del MVP**: solo se planifican si el
  usuario lo pide explicitamente porque sobro tiempo.
- Nunca generar tickets para nada de `out_of_scope`.

## Analisis previo

**Que exista en el prototipo no significa que este implementado.**

1. Si `project.repos.monorepo.local_path` en `team.yaml` es `null`, el repo real
   todavia no existe: todo el prototipo cuenta como no implementado y la unica
   verdad de lo hecho es Linear mas los estados del backlog.
2. Cuando el repo exista, inspeccionarlo antes de planificar: estructura de
   `apps/web` y `apps/api`, rutas, componentes, servicios, modelo de datos y que
   esta realmente andando contra la API. Si tiene `.codegraph/`, usar CodeGraph
   antes que grep.

## La semana

Las semanas del equipo van de **jueves a jueves** (`team.yaml` → `week`).

- La semana a planificar arranca el **proximo jueves** y su fecha limite es el
  **jueves siguiente**. Ejemplo: se cargan los tickets el lunes 10, los devs
  arrancan el jueves 13 y todo vence el jueves 20.
- Una semana pertenece al sprint que contiene su **fecha limite**, porque es
  cuando el trabajo tiene que estar terminado. Ese sprint define de que epicas se
  saca el trabajo y a que projects van los tickets.
- **Todos los tickets de la corrida llevan la misma `dueDate`**: el jueves de
  cierre.

Si el usuario nombra otra semana, usar la que pidio.

### Las fechas del cronograma

Cada funcionalidad de `features.yaml` tiene `starts` y `ends`: las fechas estimadas que
el PM ve en la pestana Cronograma. Al elegir que entra en la semana:

1. Primero, las funcionalidades pendientes cuyo `starts` cae en la semana que se esta
   planificando. Ese es el plan que el PM ya miro.
2. Si sobra capacidad, seguir por orden de prioridad como siempre, empezando por lo
   que quedo atrasado (`starts` anterior a la semana y todavia sin ticket).
3. Si algo del plan de la semana no entra o no corresponde, decirlo y explicar por que.

Al terminar, las funcionalidades que hayan quedado con ticket y cuyas fechas no
coincidan con la semana planificada se actualizan: `starts` = jueves de arranque y
`ends` = la `dueDate` del ticket. Asi el cronograma refleja lo que realmente se cargo.

## Capacidad

Segun `team.yaml`:

- 3 desarrolladores que toman tickets (`takes_tickets: true`).
- 6 SP por desarrollador por semana → **18 SP totales**.
- El margen del sprint no se descuenta de la semana: es la epica **`Fixes y carry`**, que
  tiene dos tickets de 5 SP en la ultima semana de cada sprint. Cuando toca planificar
  esa semana, esos tickets genericos se reemplazan por los arreglos concretos que hayan
  salido del QA y de las pruebas; si no aparecio nada, se usa para adelantar trabajo del sprint
  que sigue. Nunca generar tickets de esa epica en otra semana.
- **1 SP = 1 hora estimada con margen** (cada dev tiene 6 h semanales por el charter).

Apuntar a los puntos de cada dev sin inventar relleno. Si la epica pedida no tiene
suficiente trabajo pendiente:

1. Planificar todo lo que queda de esa epica.
2. Seguir por la siguiente epica incompleta **del mismo sprint**, en orden.
3. Traer solo lo necesario y marcar de donde salio.
4. Si aun asi no alcanza, dejar capacidad sin llenar y decirlo.

Nunca adelantar trabajo de un sprint posterior sin avisarlo y justificar por que no
rompe el orden de dependencias.

## Tickets fullstack

**Un ticket es una vertical completa**: modelo de Prisma, endpoint de Nest y
pantalla de Vite, todo de la misma persona. Nadie queda esperando el backend o el
frontend de otro.

**Los tests van adentro del ticket, y solo en el backend.** Nunca generar un ticket
separado de tests, de QA automatizado ni de smoke tests: si el ticket toca la API, sus
tests de Jest son parte de ese mismo ticket y de la definicion de terminado. El frontend
no lleva tests automatizados; se prueba corriendo la app.

## Salida

Mostrar las funcionalidades elegidas con sus SP, el total, la fecha límite, lo atrasado y lo que no entró. No crear nada en Linear.

## Ejemplo de uso
**Pedido:** Planificá la semana que arranca el jueves 13.

**Resultado:** El corte de funcionalidades de la semana hasta 18 SP, en orden de prioridad, con la fecha límite, lo que quedó afuera y por qué.
