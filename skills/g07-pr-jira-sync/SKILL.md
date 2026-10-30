---
name: g07-pr-jira-sync
description: "Cruza los PRs de GitHub con el estado de los tickets en Jira (MCP) y detecta inconsistencias de trazabilidad (tickets In Review sin PR, PRs mergeados con el ticket abierto, tickets Done con el PR abierto, PRs sin key, viejos o sin reviewer), con una acción concreta por hallazgo. Usar cuando el TL o el PM quiera verificar que el board refleja el código antes de una reunión, un cierre de semana o una entrega."
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - github
  grupo: "07"
  autor:
    nombre: Josefina Sapag
    github: jmsapag
  responsables:
  - jmsapag
  madurez: usado-en-proyecto
  relacionados:
  - g07-code-review-tl
  - g07-release-notes
  - g07-role-handoff
---

# PR ↔ Jira Sync

Verificá que el board de Jira y los PRs de GitHub cuenten la misma historia. Los reportes de estado (como `g07-sprint-status-report` o `g07-delivery-digest`) confían en Jira tal cual está; esta skill chequea si ese estado es verdad mirando el código.

La parte de GitHub la resuelve un script determinístico (`pr_snapshot.py`, en esta carpeta) que no depende de Claude: se puede correr a mano o desde CI. La parte de Jira y el cruce los hacés vos con el MCP de Atlassian.

## Cuándo usar esta skill

Cuando el usuario pida "cruzar PRs con Jira", "chequear trazabilidad", "qué está desactualizado en el board", "qué PRs están colgados", o antes de un cierre de semana/sprint para no reportar como hecho algo que no está mergeado (ni como pendiente algo que ya se mergeó).

## Setup (una sola vez)

- **GitHub**: CLI `gh` instalado y autenticado (`gh auth login`). El script solo lee.
- **Jira**: MCP de Atlassian conectado a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`).
- **Python 3** para correr `pr_snapshot.py` (sin dependencias externas).
- **Datos del proyecto**: completá `config.md` en esta carpeta, incluidos los nombres de los estados de tu workflow.
- **Discord (opcional, solo si querés mandar el reporte)**: webhook en la variable de entorno que indica `config.md`, o en `config.local.md` (copiá `config.local.example.md`).

## Configuración

`config.md` en esta carpeta: repo de GitHub, site y project key de Jira, nombres de los estados del workflow, ventana de días y umbral de PR viejo. Si algún valor sigue con un placeholder (`<...>`), pedíselo al usuario y ofrecé guardarlo.

## Paso 1: snapshot de GitHub

Ejecutá el script que está en esta misma carpeta (usá la ruta absoluta de la carpeta de la skill):

```
python3 -I <carpeta de esta skill>/pr_snapshot.py --repo <repo> --project <KEY> --days <ventana> --stale-days <umbral>
```

El script imprime un JSON con `prs` (cada PR con `state`, `jira_keys`, `flags`, `reviewers`, `idle_days`, `url`) y `by_key` (key de Jira → números de PR). Si falla (sin `gh`, sin auth, sin red), mostrá el error tal cual y no sigas — sin GitHub no hay cruce posible.

Los `flags` que ya calcula el script (no los recalcules): `sin_key_jira`, `draft`, `viejo`, `sin_reviewer`, `cambios_pedidos`.

## Paso 2: estado de Jira

Usá la tool MCP cuyo nombre termine en `searchJiraIssuesUsingJql` (el prefijo cambia según el entorno). Pedí solo los campos `summary`, `status`, `assignee`, `duedate`, `updated` — las descripciones suelen ser largas y acá no hacen falta.

1. Tickets activos: `project = <KEY> AND status in (<estados "en curso" y "en revisión" de config.md>) ORDER BY key`
2. Tickets cerrados en la ventana: `project = <KEY> AND statusCategory = Done AND updated >= -<ventana>d ORDER BY key`
3. Tickets mencionados por PRs que no aparecieron en 1 ni 2: `project = <KEY> AND key in (<keys de by_key que faltan>)` — para saber en qué estado está cualquier ticket que tenga un PR.

Paginá cada consulta hasta que `hasNextPage` sea `false`. Si una key de un PR no existe en Jira, eso es un hallazgo en sí (key mal escrita o ticket borrado).

## Paso 3: reglas de cruce

Evaluá cada regla y quedate solo con lo que la dispara:

| # | Regla | Severidad | Lectura |
|---|---|---|---|
| R1 | Ticket **en revisión** sin PR abierto | 🔴 | Alguien lo movió a revisión pero no hay nada que revisar (o el PR no tiene la key). |
| R2 | PR **mergeado** con ticket que no está en Done | 🟠 | El board atrasa: el trabajo está hecho pero no se reporta. |
| R3 | Ticket **Done** con PR todavía abierto (y ninguno mergeado) | 🔴 | Se reporta como hecho algo que no llegó a `main`. |
| R4 | PR abierto con ticket **sin empezar** (statusCategory To Do) | 🟠 | El ticket no se movió cuando se empezó a trabajar. |
| R5 | PR con flag `sin_key_jira` | 🟡 | Trabajo sin trazabilidad. Si el título sugiere un ticket, proponé cuál. |
| R6 | PR abierto con flag `viejo` o `cambios_pedidos` | 🟠 | Se está trabando la revisión. Nombrá a quién le toca moverse (autor o reviewer). |
| R7 | PR abierto con flag `sin_reviewer` | 🟡 | Nadie va a revisarlo si no se asigna. |
| R8 | Ticket **en curso** sin PR y con due date en ≤ 2 días | 🟡 | Riesgo de no llegar: a días del vencimiento sin nada para revisar. |
| R9 | Key mencionada en un PR que no existe en Jira | 🟡 | Key mal escrita o ticket eliminado. |

Si una misma issue dispara varias reglas, listala una sola vez con todas las reglas juntas.

## Output

Un reporte en Markdown en el chat, con esta estructura:

1. Título: `🔗 **PR ↔ Jira — <proyecto> — DD/MM**` y una línea con los conteos (`N PRs abiertos · M mergeados en X días · K tickets activos`).
2. **Veredicto** en una línea: `✅ Board y código alineados` si no saltó ninguna regla 🔴/🟠, o `⚠️ N inconsistencias` en otro caso.
3. **🔴 Inconsistencias que hay que corregir** — R1, R3.
4. **🟠 Board desactualizado / revisiones trabadas** — R2, R4, R6.
5. **🟡 Higiene** — R5, R7, R8, R9.
6. **Acciones sugeridas** — una por hallazgo, concreta y con dueño: "mover KEY-104 a Done (PR #88 mergeado el 27/10)", "@autor: pedir review del PR #93". Sin acciones genéricas.

Cada hallazgo con: key de Jira (link), estado en Jira, PR (#número con link), estado del PR y la regla. Omití las secciones vacías salvo el veredicto.

Ver `example-output.md` en esta carpeta.

## Qué no hacer

- No muevas tickets en Jira ni comentes en GitHub. Esta skill diagnostica; si el usuario pide aplicar alguna acción en Jira (por ejemplo, transicionar un ticket a Done), hacelo ticket por ticket con confirmación explícita.
- No inventes PRs ni estados: si un dato no vino del script o de Jira, no está.
- No mandes el reporte a Discord salvo que el usuario lo pida. Si lo pide: resolvé el webhook con la variable de entorno cuyo nombre figura en `config.md` (o la línea "Discord webhook URL" de `config.local.md` en esta carpeta), armá `payload.json` con `{"content": "<reporte>"}` (partido por sección si pasa los ~2000 caracteres) y enviá con `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`. Nunca imprimas la URL.

## Ejemplo de uso

**Pedido:** Cruzá los PRs con Jira antes de la reunión del jueves.

**Resultado:** Corre pr_snapshot.py para sacar el estado de los PRs, consulta los tickets activos y cerrados en Jira, aplica las reglas R1 a R9 y devuelve un reporte por severidad con una acción concreta y con dueño por cada inconsistencia. No mueve tickets ni comenta en GitHub.
