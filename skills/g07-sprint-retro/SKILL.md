---
name: g07-sprint-retro
description: "Genera la retro de un sprint cerrado desde Jira (MCP), con lo completado vs. lo planificado, las issues arrastradas, las señales de bloqueo y acciones para el próximo sprint, y la envía al canal de Discord del equipo. Usar cuando el PM cierre un sprint y necesite armar la retro o un resumen para la cátedra."
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - discord
  grupo: "07"
  autor:
    nombre: Josefina Sapag
    github: jmsapag
  responsables:
  - jmsapag
  madurez: usado-en-proyecto
  relacionados:
  - g07-sprint-status-report
  - g07-weekly-process-checklist
---

# Sprint Retro

Generá el reporte de cierre de un sprint: qué se completó vs. lo planificado, qué issues se arrastraron de sprints anteriores, qué señales de bloqueo hubo, y una agenda de retro con acciones concretas. A diferencia de `g07-sprint-status-report` (que mira el sprint *en curso*), esta skill mira un sprint que ya *cerró*.

## Cuándo usar esta skill

Cuando el PM (usuario) pida una "retro", "retro de sprint", "cómo salió el sprint", "reporte de cierre de sprint", o quiera armar la agenda para la reunión de retro o una entrega a la cátedra.

## Setup (una sola vez)

1. **Jira**: conectá el MCP de Atlassian a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`). Con permisos de lectura alcanza.
2. **Datos del proyecto**: completá `config.md` en esta carpeta. Los dos campos personalizados (story points y sprint) se pueden dejar vacíos: la skill los descubre la primera vez y te propone guardarlos.
3. **Discord (opcional)**: webhook en la variable de entorno que indica `config.md`, o en `config.local.md` (copiá `config.local.example.md`).

## Configuración

Leé `config.md` de esta carpeta. Si el site o el project key siguen con un placeholder (`<...>`), avisale al usuario en una línea y no sigas: sin project key no hay forma de resolver un sprint.

**Campos personalizados.** Cada Jira tiene sus propios IDs para story points y sprint (`customfield_NNNNN`). Si en `config.md` están vacíos o con placeholder, descubrilos con la tool que termine en `getJiraIssueTypeMetaWithFields` sobre el tipo de issue más común del proyecto (buscá los campos llamados "Story point estimate"/"Story Points" y "Sprint"), avisale al PM qué encontraste y ofrecé guardarlos en `config.md`. Si hay issues de tipos distintos (Story, Bug) con puntos cargados y el total no cierra, puede que usen otro campo: chequealo para ese tipo antes de sumar, y avisá la discrepancia en vez de sumar como si nada.

## Paso 0: resolver el sprint

Con la tool MCP que termine en `searchJiraIssuesUsingJql`:

1. Si el PM nombra el sprint ("hacé la retro de Sprint 1"), usalo directo: `project = <KEY> AND sprint = "<nombre>"`.
2. Si no, buscá sprints cerrados: `project = <KEY> AND sprint in closedSprints()`.
   - Si aparece un único sprint cerrado, usalo.
   - Si aparece más de uno, **no asumas cuál es el más reciente**: el campo sprint expone `id`, `name`, `state` y `boardId`, pero no una fecha de cierre confiable para ordenar. Preguntale al PM cuál quiere.
3. Si la consulta falla o no hay tools de Jira, avisale en una línea y pedile el estado del sprint pegado a mano (issues con estado y asignado). No inventes issues ni estados.

## Paso 0.5: verificar que el sprint esté cerrado

**No generes una retro para un sprint que no cerró.** Si el sprint del Paso 0 está `future` o `active`:

- No completes las secciones 2 a 5 con datos de ese sprint.
- Decile al PM que ese sprint todavía no cerró (con su estado real) y mostrale el scope planificado (cuántas issues, cuántas sin asignar) etiquetado como "planificado, no retro".

Si no se nombró sprint y `closedSprints()` no devolvió nada (el proyecto recién arranca):

- Decilo: no hay sprints cerrados; hace falta iniciar y cerrar uno en Jira antes de poder hacer una retro.
- Opcionalmente, mostrá el scope del sprint activo o futuro más próximo, siempre etiquetado como planificado.

## Paso 1: completado vs. no completado

Con el sprint confirmado como `closed`:

1. Completadas: `project = <KEY> AND sprint = "<nombre>" AND statusCategory = Done`.
2. No completadas: `project = <KEY> AND sprint = "<nombre>" AND statusCategory != Done`.
3. Para ambas, traé `key`, `summary`, `status`, `assignee`, `issuetype`, el campo de story points, el campo de sprint e `issuelinks`. Paginá hasta `hasNextPage = false`.
4. Dentro de las no completadas, separá las que nunca se empezaron (siguieron en To Do) de las que quedaron a mitad: son conversaciones de retro distintas.
5. Si hay story points cargados, sumalos por bucket (completado vs. no completado). Si a alguna issue le falta estimación, decilo en el reporte — no la cuentes como 0.

## Paso 2: issues arrastradas (carry-over)

Usá el campo de sprint que ya trajiste (es un array de sprints):

- Si el array de una issue tiene más de un elemento, se arrastró de un sprint anterior. Reportá los sprints en el orden en que aparecen, aclarando que el orden es una inferencia.
- Limitación a declarar en el reporte: esto solo detecta issues que siguen ligadas a algún sprint. Una issue que salió del sprint y volvió al backlog sin sprint no se detecta sin acceso al changelog.

## Paso 3: señales de bloqueo

En este orden de prioridad, sin mezclar los niveles:

1. **Flagged/Impediment** (la señal más fuerte y barata): `project = <KEY> AND sprint = "<nombre>" AND Flagged = Impediment`.
2. **Links "Blocks" / "is blocked by"** (ya vienen en `issuelinks`): para cada issue no completada, si está bloqueada por otra que tampoco está Done o que se arrastró, es una causa concreta de por qué no se terminó. Distinguí "dependencia planificada sin resolver" (el link existía desde antes y no hubo movimiento) de "bloqueo real durante el sprint" (hubo movimiento de estado y se frenó).
3. **Comentarios** (el más débil, último recurso): solo para las no completadas sin señal de los niveles 1 o 2. Traé los comentarios de ese subconjunto y buscá "bloque", "blocked", "esperando", "depende de", "impedimento".

## Otro input, siempre manual

Si el PM tiene contexto del equipo (standups, bloqueos reportados por Discord que no quedaron en Jira), pedíselo — sin bloquear el reporte esperándolo.

## Output

Un reporte en Markdown con estas seis secciones, en este orden:

1. **Resumen del sprint cerrado** — nombre, N de M issues completadas (+ puntos si hay datos confiables), semáforo (🟢 mayoría entregada / 🟡 entrega parcial / 🔴 entrega baja) con el número que lo justifica.
2. **Completado vs. no completado** — dos listas (key, resumen, asignado), separando lo que nunca se empezó de lo que quedó a mitad.
3. **Señales de qué no salió bien** — carry-overs (cuántas veces y desde qué sprint), Flagged, dependencias sin resolver y lo del barrido de comentarios, cada ítem atado a un issue key.
4. **Qué salió bien** — issues completadas sin señales de bloqueo. Si no hay nada que destacar, decilo así de plano en vez de inventar un positivo.
5. **Agenda de retro / Acciones para el próximo sprint** — accionables atados a datos ("reestimar KEY-8: bloqueó a 5 issues y ninguna arrancó", "asignar dueño a las 3 issues arrastradas sin asignar antes del planning"). Nada genérico.
6. **Datos no disponibles / limitaciones** — lo que no se pudo verificar: sin changelog, sin novedades del equipo si el PM no las pasó, puntos parciales si falta alguna estimación.

No inventes issues, developers, estados ni causas de bloqueo.

Ver `example-output.md` en esta carpeta.

## Envío a Discord

El reporte se manda siempre, apenas se genera, además de mostrarlo en el chat.

1. **Resolvé la URL del webhook**, en este orden: la variable de entorno cuyo nombre figura en `config.md`; la línea "Discord webhook URL" de `config.local.md` en esta carpeta. Si no hay ninguna, avisale al PM en una línea (que copie `config.local.example.md`) y quedate con el reporte en el chat.
2. Armá el JSON en un archivo temporal `payload.json` en el directorio de trabajo.
3. Hasta ~2000 caracteres por mensaje: si entra, un POST con `{"content": "<reporte>"}`; si no, un POST por sección (`## `), en orden, sin cortar ninguna.
4. Enviá con exactamente esta forma, URL literal al final: `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`.
5. Nunca imprimas la URL ni la escribas en un archivo versionado.
6. Confirmá si salió bien (204) o mostrá el error tal cual, sin reintentar en loop.

## Ejemplo de uso

**Pedido:** Hacé la retro del Sprint 2.

**Resultado:** Verifica en Jira que el sprint esté cerrado, separa lo completado de lo no completado (nunca empezado vs. a mitad), detecta issues arrastradas y señales de bloqueo, y arma una agenda de retro con acciones atadas a issues concretas; lo muestra en el chat y lo envía a Discord.
