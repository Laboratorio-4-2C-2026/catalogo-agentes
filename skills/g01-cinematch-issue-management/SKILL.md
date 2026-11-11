---
name: g01-cinematch-issue-management
description: "Planifica, secuencia y dimensiona issues de Cinematch desde el rol de Product Owner: junta el estado real (Linear, workbook de EVM, gantt, repo) antes de planificar, verifica en vez de suponer, sigue la cadena completa de dependencias y mantiene las estimaciones honestas contra la capacidad de la línea base. Usala para decidir qué entra en un sprint o una semana, si un issue está listo, en qué orden van, qué bloquea a qué, o para reconciliar el plan con Linear, el gantt o el presupuesto; redactar el cuerpo de un issue es de g01-cinematch-issue-draft."
author: Tomás
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
  - github
  - google-drive
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-issue-draft
  - g01-cinematch-baseline-change
  - g01-cycle-chain-sequencer
  - g04-planeamiento-sprint-tickets
---
# Cinematch issue management

Planning fails in one specific way: the plan is built from one source while the work happens against another. The rules below are all consequences of that.

Notes you write are in Spanish. This skill is in English.

## 1. Gather the real state before planning anything

**Linear is the source of truth for the backlog, but it is not the only source and it is not always current.** At least five places hold schedule or scope information, and they can disagree:

| Source | What it is authoritative for |
|---|---|
| Linear | What issues exist, their scope, status and assignment |
| The team's budget and earned value workbook, its EVM sheet | The vigente baseline. Planned Value per period |
| The team's gantt workbook | The week-by-week plan |
| The application repository | What is actually built |
| This vault | Why things are the way they are |

Two traps inside that table:

- **A budget workbook from before a re-baseline is superseded**, the Project Charter's one included. It has other periods and other hours. Plan only against the workbook that includes the last re-baseline.
- **The gantt and Linear count weeks differently.** The gantt numbers its weeks; Linear encodes the same weeks in the **due date** field. Say which one governs before planning against either.

Read the ones that bear on the question. A sprint question that ignores the baseline produces a number that does not match it.

## 2. Verify. Do not assume

- **Do not infer an assignment.** Query the field; a sibling issue's assignee says nothing about this one.
- **Do not trust status.** Without cycles, assignee, due date and status are the entire control surface, and a status can lag behind a merge. **Check git before describing anything as in flight or late.**
- **Do not trust a parent.** A parent's status can lag behind its children's.
- **Do not trust an issue's own acceptance criteria as evidence it is met.** Every task of a user story can be merged while the story's own criterion still fails, if nothing wires the tasks to each other.
- **Do not declare something missing from a local search.** It may exist under another name or in another form.

When planning a week, **read what is already assigned and dated before proposing anything**. A week with issues already assigned is not an empty slot.

## 3. Find the whole chain, not the obvious link

An issue that sounds like one thing is usually several. Setting up a deployment, for instance, can mean infrastructure as code, DNS records, a certificate, runtime configuration, a smoke check, and a CD pipeline per host.

The technique that works: **follow the data and the requests, not the ticket titles.** For each issue ask what it consumes, where that comes from, and whether that exists yet. Then ask the same of the answer.

Two things that surface only this way:

- **A consumer whose provider does not exist**: a screen that reads from an endpoint nobody was asked to build.
- **A signal whose table does not exist**: a computation that consumes data the schema does not hold yet.

**Read the code before sizing.** It cuts both ways: part of the work may already exist, or the running application may not reach a mechanism the ticket assumes.

## 4. Dependencies

**Avoid them first. Record them second. Sequence them third.**

- **Every dependency goes in as a real `blocked by` relation.** Prose in the description does not surface to whoever picks the issue up, and neither does `related to`.
- **At any point in time, an issue that is available to pick up must have every dependency satisfied.** If it does not, it is not ready, whatever its status says.
- **Prefer splitting by data availability over one large ticket.** When a feature consumes several inputs that land at different times, ship one ticket per input as its input becomes real, each with a single blocker.
- **An intra-week dependency is a last resort, and a cross-developer one inside the same week is worse.** If it cannot be avoided, order it explicitly and say so in both issues. "Coordinate early" is not an order.
- **A dependency with no date is invisible.** An issue with no due date belongs to no week, so nobody picks it up. Anything that blocks dated work needs a date.

## 5. Sizing and capacity

- **An estimate measures developer capacity consumed, not work performed.** Capacity is three developers times six hours, so eighteen points per week under the standing assumption that one point is one hour.
- **Management work is unestimated.** Configuring a DNS record, creating a hosted project, generating a token: none of it is programming, none of it comes out of developer capacity, and none of it earns value in the baseline, which capitalises developer effort only.
- **Management work does not go into Linear. Linear is developer-only.** The pendiente, with its date, lives in `TODO/`; the detail of what to do lives in the Ficha of the draft whose issue it unblocks, never as a document of its own. When it blocks a developer issue, that issue states the precondition in its own body ("the hosting project must exist and the secrets must be loaded; if they are not, say so before starting") instead of carrying a relation to something Linear does not hold.
- **Reconcile against the baseline, not the gantt.** Planned Value is flat at eighteen per period. A sprint that sums to something else needs a stated reason.
- **When scope will not fill the target, say so and give options** rather than padding or silently under-filling. Pulling work forward from a later sprint is legitimate and usually preferable when that sprint is over capacity.

## 6. Foresight

A plan that only describes the current week is not a plan.

- **Check that a week's contents are still real before planning around them.** Issues closed earlier can leave a week empty while the plan shows it full.
- **Look at what a change does to later sprints.** Moving an issue out of a sprint is only an improvement if the sprint receiving it can hold it.
- **Watch for scope with no week.** An issue with an estimate but no week, epic or place in the plan does not disappear because it is unscheduled.
- **Name what a sprint cannot demonstrate.** If a screen advertises a feature that lands two sprints later, that is a demo decision to take now.

## 7. When the plan changes

- **Do not delete a superseded breakdown.** Mark it `SUPERADO por [nota nueva]` and leave the text. The old plan is evidence of what was believed and when.
- **Write down what is deliberately unresolved**, with the options and the criterion, rather than leaving it implicit. An open decision that is recorded can be taken by someone else; one that is not gets rediscovered.
- **A closed decision goes to `Decisiones Técnicas.md`** with its rationale and the alternatives rejected, not only the choice.

## Ejemplo de uso

**Pedido:** ¿Qué entra en la semana que viene y en qué orden?

**Resultado:** Lee lo que ya está asignado y fechado en Linear, el PV del EVM y el gantt, verifica en git qué ya se mergeó y propone la semana contra la capacidad de la línea base, con cada dependencia como relación `blocked by` y diciendo explícitamente si el alcance no llega a llenarla.
