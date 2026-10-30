---
name: g07-ready-check
description: "Audita los tickets de Jira (MCP) que el equipo está por empezar contra una Definition of Ready configurable (user story, criterios de aceptación verificables, dueño, fecha, épica, contrato de API y dependencias resueltas a tiempo) y devuelve por ticket qué falta y la corrección propuesta, más las cadenas de bloqueo que ponen en riesgo una entrega. Usar antes del planning o cuando el PO o QA quiera saber si lo comprometido está listo para arrancar."
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: "07"
  autor:
    nombre: Josefina Sapag
    github: jmsapag
  responsables:
  - jmsapag
  madurez: experimental
  relacionados:
  - g07-qa-acceptance
  - g07-delivery-digest
  - g07-role-handoff
---

# Ready Check

Revisá si los tickets que el equipo está por empezar están **listos para empezar** (Definition of Ready), antes de que alguien se siente a desarrollarlos y descubra que falta el criterio de aceptación, que depende de algo que nadie tiene asignado, o que el contrato con el backend no existe.

Es el control previo al desarrollo; `g07-qa-acceptance` es el control posterior. Lo que esta skill encuentra temprano es lo que QA, si no, encuentra tarde.

## Cuándo usar esta skill

Cuando el usuario (PO, PM o QA) pida "revisar si los tickets están listos", "definition of ready", "qué falta para el planning", "están bien escritos los tickets de la semana que viene", o antes de comprometer una entrega.

## Setup (una sola vez)

1. **Jira**: MCP de Atlassian conectado a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`). Para leer alcanza; para dejar comentarios con los hallazgos hace falta permiso de escritura.
2. **Datos del proyecto y criterios**: completá `config.md` en esta carpeta. Ahí se define qué exige la Definition of Ready del equipo (por ejemplo, si el equipo estima o no) — la skill no exige lo que el equipo no usa.

## Configuración

Leé `config.md` de esta carpeta: site y project key de Jira, día de entrega y la **Definition of Ready** del equipo (qué criterios aplican y cuáles son obligatorios u opcionales). Si el project key sigue con un placeholder (`<...>`), pedíselo al usuario y no sigas.

## Paso 0: qué tickets revisar

En este orden de prioridad:

1. Si el usuario nombra tickets (`KEY-12, KEY-15`) o un sprint, revisá esos.
2. Si no, revisá el **trabajo comprometido sin arrancar**: tickets en estado To Do (statusCategory "To Do") con due date en la próxima entrega o en la siguiente. Calculá las dos fechas con el día de entrega de `config.md`.
3. Sumá siempre los **bloqueantes de esos tickets**, aunque no tengan fecha ni estén en To Do: un ticket comprometido no está listo si depende de algo que no va a llegar a tiempo.
4. Si el usuario pide "el backlog" o "lo que viene", sumá los To Do sin due date, separados: no están comprometidos, así que lo que les falte no es urgente.

Decí al principio qué conjunto revisaste y por qué.

## Paso 1: traer los tickets

Con la tool MCP cuyo nombre termine en `searchJiraIssuesUsingJql`, en formato `markdown`, pedí `summary`, `status`, `assignee`, `duedate`, `issuetype`, `parent`, `issuelinks`, `description` y, si el equipo estima, el campo de story points de `config.md`. Paginá hasta `hasNextPage = false`.

Las descripciones pueden ser largas: si la respuesta es demasiado grande, partí la consulta en tandas de pocos tickets en vez de pedir menos campos — sin la descripción no se puede evaluar nada.

Para cada bloqueante (link "is blocked by" en `issuelinks`), traé su estado, asignado y due date si no vino en la misma consulta.

Si no hay conexión a Jira, pedile al usuario los tickets pegados (título, descripción, asignado, fecha, dependencias). No inventes contenido de tickets.

## Paso 2: evaluar cada ticket contra la Definition of Ready

Aplicá solo los criterios que `config.md` marque como activos. Para cada uno, el resultado es ✅ cumple, ⚠️ cumple a medias, o ❌ no cumple, con la evidencia (qué dice o qué falta en el ticket).

1. **Objetivo claro** — hay una user story ("Como … quiero … para …") o un objetivo explícito de qué cambia para quién. Un título solo no alcanza.
2. **Criterios de aceptación verificables** — existen, y cada uno se puede comprobar con un resultado observable (en Gherkin o en una lista). Marcá ⚠️ los criterios vagos ("funciona correctamente", "rápido", "intuitivo", "se ve bien") sin una medida o un resultado concreto, y los que mezclan varios comportamientos en uno.
3. **Alcance acotado** — dice qué entra y, idealmente, qué queda fuera. Sin esto, QA no puede distinguir un bug de algo fuera de alcance.
4. **Contrato definido** (solo si el ticket cruza front y back) — si el ticket consume o expone una API, el endpoint, el request y la respuesta están escritos en el ticket o en el ticket del que depende. Un front que consume un endpoint de un ticket que todavía no existe o no tiene contrato es ❌.
5. **Dueño asignado**.
6. **Fecha de entrega** — tiene due date, y cae en un día de entrega.
7. **Épica** — tiene `parent`, para saber a qué funcionalidad pertenece (y para las release notes).
8. **Dependencias resueltas a tiempo** — cada bloqueante está Done, o tiene dueño y una due date **anterior** a la del ticket. Bloqueante sin dueño, sin fecha, en To Do o con la misma fecha que el ticket: ❌ (mismo día = cero margen para integrar).
   - **Dependencias no linkeadas**: buscá en la descripción keys de otros tickets (`<KEY>-<número>`), por ejemplo en una sección de "Contrato consumido". Las que apunten a tickets ya Done son contexto y no importan; las que apunten a tickets **no terminados** y no estén linkeadas como "is blocked by" son dependencias ocultas: el board no las muestra y nadie las va a seguir. Traé su estado en una sola consulta (`key in (...) AND statusCategory != Done`) y marcalas ⚠️ con la propuesta de linkearlas.
9. **Estimación** (solo si el equipo estima) — tiene story points cargados.
10. **Tamaño razonable** — señales de que conviene partirlo: muchos criterios de aceptación (más del umbral de `config.md`), o mezcla de trabajo de backend y frontend en un solo ticket cuando el equipo los separa.

No penalices lo que el equipo decidió no usar. No juzgues el contenido técnico de la solución: eso es del code review.

## Paso 3: veredicto y cadenas de bloqueo

**Por ticket:**

- 🟢 **Ready** — cumple todos los obligatorios.
- 🟡 **Casi** — falla solo en opcionales, o en obligatorios que se resuelven en minutos (asignar dueño, poner fecha, linkear la épica).
- 🔴 **No ready** — falta objetivo, criterios de aceptación o contrato, o tiene una dependencia que no llega a tiempo.

**Cadenas de bloqueo.** Recorré los links "is blocked by" (y las dependencias no linkeadas que encontraste) desde cada ticket comprometido hacia atrás. Si en la cadena hay un ticket sin dueño, sin fecha o en To Do, la entrega del ticket comprometido está en riesgo aunque él mismo esté perfecto. Mostrá la cadena completa: `KEY-106 (vence 05/11) ← KEY-105 (In Progress, vence 05/11) ← KEY-79 (To Do, sin dueño, sin fecha)`.

## Paso 4: correcciones propuestas

Para cada ❌ y ⚠️, proponé la corrección concreta, lista para pegar en el ticket:

- **Criterios faltantes o vagos**: reescribilos en Gherkin a partir de lo que ya dice el ticket (user story, alcance, contrato). Marcá que la redacción es tuya y que el PO la tiene que validar. Si el ticket no da información suficiente para escribirlos, no los inventes: escribí las preguntas que el PO tiene que responder.
- **Sin dueño, fecha o épica**: no elijas vos a quién asignarlo ni qué fecha ponerle. Decí qué hay que decidir y, si ayuda, cuál es la fecha límite según las dependencias ("tiene que estar antes del 05/11 porque bloquea a KEY-105").
- **Ticket demasiado grande**: proponé cómo partirlo (por ejemplo, back y front, o por escenario), con un título para cada parte.

## Output

Markdown, en español:

1. `✅ **Ready check — <proyecto> — DD/MM**` y una línea con qué se revisó ("tickets To Do de las entregas del 05/11 y 12/11 + sus bloqueantes").
2. **Resumen** — N 🟢 · M 🟡 · K 🔴, y en una línea lo más urgente.
3. **⛓️ Cadenas de bloqueo que ponen en riesgo una entrega** (si hay) — una por línea, con la acción para destrabarla.
4. **Por ticket**, primero los 🔴, después 🟡, después 🟢. Para cada uno: key con link, título, veredicto; solo los criterios que fallan, con la evidencia; y la corrección propuesta. Los 🟢 en una sola línea cada uno.
5. **Backlog sin comprometer** (si se pidió) — separado y en formato corto: qué le falta a cada uno para poder comprometerlo.
6. **Lo que no se pudo evaluar** — tickets que no se pudieron leer, criterios que no aplican, supuestos.

Ver `example-output.md` en esta carpeta.

## Qué no hacer

- No edites tickets ni cambies asignados, fechas o estados. Si el usuario quiere dejar los hallazgos en Jira, ofrecé agregar **un comentario por ticket** con su veredicto y la corrección propuesta (tool que termine en `addCommentToJiraIssue`), y hacelo solo con un "sí" explícito, ticket por ticket o con una lista que el usuario confirme.
- No inventes criterios de aceptación como si fueran del PO: lo que redactes va marcado como propuesta.
- No mandes nada a Discord ni a otro canal.

## Ejemplo de uso

**Pedido:** Antes del planning, revisá si los tickets de la próxima entrega están listos para arrancar.

**Resultado:** Trae de Jira los tickets To Do de las dos próximas entregas y sus bloqueantes, los evalúa contra la Definition of Ready de config.md, marca cada uno 🟢/🟡/🔴 con lo que falta y la corrección propuesta (por ejemplo, criterios vagos reescritos en Gherkin), y muestra las cadenas de bloqueo y dependencias no linkeadas que ponen en riesgo una entrega. Solo comenta en Jira si le confirmás.
