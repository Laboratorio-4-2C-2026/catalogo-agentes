---
name: g07-role-handoff
description: "Arma el documento de traspaso de un rol del equipo (PM, TL, QA o PO) para quien lo asume, con el estado real de Jira (MCP) y GitHub, los bloqueos vivos, las rutinas del rol y los acuerdos, personas y accesos que solo conoce quien se va. Usar cuando los roles roten y alguien tenga que tomar la posta sin perder contexto."
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - planificacion
  - mantenimiento
  tecnologias:
  - agnostico
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
  madurez: experimental
  relacionados:
  - g07-pr-jira-sync
  - g07-sprint-status-report
  - g07-ready-check
---

# Role Handoff

Armá el documento de traspaso para cuando un rol del equipo cambia de manos. En muchos equipos (y en la materia) los roles (PM, TL, QA, PO) rotan, y lo que se pierde en cada rotación no es lo que está en Jira — es el contexto: qué está por vencer, qué está trabado y por qué, qué rutinas corren solas, qué se acordó de palabra. Esta skill junta lo verificable de Jira y GitHub, le pregunta a quien se va lo que no está escrito en ningún lado, y deja un documento que quien llega puede leer en cinco minutos y usar desde el primer día.

A diferencia de `g07-sprint-status-report` (foto del sprint para el equipo) o `g07-weekly-process-checklist` (evidencia para la cátedra), esto le habla a **una persona**: la que asume el rol.

## Cuándo usar esta skill

Cuando el usuario pida "armar el handoff", "pasarle el rol a X", "traspaso de PM/TL/QA/PO", "qué le tengo que dejar a quien me reemplaza", o cuando se acerque una rotación de roles.

## Setup (una sola vez)

- **Jira**: MCP de Atlassian conectado a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`).
- **GitHub** (para TL, PM y QA): CLI `gh` autenticado (solo lectura).
- **Datos del proyecto**: completá `config.md` en esta carpeta, incluida la lista de herramientas y rutinas de cada rol.

## Configuración

`config.md` en esta carpeta: site y project key de Jira, repo de GitHub, día de entrega, y qué herramientas y rutinas usa cada rol. Si algún valor sigue con un placeholder (`<...>`), pedíselo al usuario y ofrecé guardarlo.

## Paso 0: qué traspaso

Necesitás tres datos. Si el usuario no los dio, preguntalos en un solo mensaje:

1. **Rol** que se traspasa: PM, TL, QA o PO (puede ser más de uno si la persona tenía dos).
2. **Quién se va y quién llega** (nombres; el de quien llega es para dirigirle el documento).
3. **Fecha del traspaso** (por defecto, hoy).

Con la fecha calculá las dos próximas entregas: el equipo entrega por ciclos usando el campo **Due date** de Jira, en el día de entrega que indica `config.md`. Si la fecha del traspaso cae en día de entrega, ese día cuenta como la primera entrega.

## Paso 1: lo verificable (Jira y GitHub)

Usá la tool MCP cuyo nombre termine en `searchJiraIssuesUsingJql` (el prefijo cambia según el entorno: `mcp__atlassian__*` local, `mcp__claude_ai_Atlassian_Rovo__*` en la nube). Pedí solo los campos que necesitás (`summary`, `status`, `assignee`, `duedate`, `issuetype`, `parent`, `issuelinks`, `updated`) — las descripciones suelen ser largas y acá no hacen falta. Paginá cada consulta hasta que `hasNextPage` sea `false`.

Consultas comunes a todos los roles:

1. Próximas dos entregas: `project = <KEY> AND duedate in ("<entrega 1>", "<entrega 2>") ORDER BY duedate, status`.
2. Trabajo activo: `project = <KEY> AND status in (<estados "en curso" y "en revisión" de config.md>) ORDER BY status`.
3. Señales de riesgo: `project = <KEY> AND statusCategory != Done AND (Flagged = Impediment OR issueLinkType = "is blocked by")`, pidiendo también `issuelinks`. **Esta consulta trae falsos positivos**: matchea cualquier link "is blocked by", aunque el ticket que bloquea ya esté Done. Un ticket solo es un bloqueo vivo si está Flagged o si alguno de sus `inwardIssue` de tipo "Blocks" tiene `statusCategory` distinto de Done; descartá el resto. Si el bloqueante sigue en To Do, remarcalo: es el riesgo más serio, porque ni siquiera arrancó lo que hace falta.

Consultas según el rol (solo las del rol que se traspasa):

- **QA**: bugs abiertos `project = <KEY> AND issuetype = Bug AND statusCategory != Done ORDER BY priority`, y tickets esperando validación (los que están en el estado "en revisión" en la consulta 2).
- **PO**: épicas abiertas `project = <KEY> AND issuetype = Epic AND statusCategory != Done`, y para cada una cuántos hijos hay Done vs. no Done (`parent = <EPIC>`). Tickets sin due date ni asignado: `project = <KEY> AND statusCategory = "To Do" AND (duedate is EMPTY OR assignee is EMPTY)`.
- **PM** y **TL**: no necesitan consultas extra de Jira; su parte específica sale de las comunes y de GitHub.

GitHub (para TL, PM y QA; opcional para PO): traé los PRs abiertos.

```
gh pr list --repo <repo> --state open --json number,title,headRefName,isDraft,reviewRequests,latestReviews,updatedAt,url
```

Sacá las keys de Jira de cada PR buscando `<KEY>-<número>` en el título y en la branch. Marcá como **draft** los que tengan `isDraft`, **sin reviewer** los que no tengan `reviewRequests` ni `latestReviews`, y **viejo** los que lleven 3 días o más sin `updatedAt`. Si tenés instalada la skill `g07-pr-jira-sync`, podés usar su `pr_snapshot.py` en su lugar: calcula esos mismos flags. Si `gh` falla, seguí solo con Jira y decilo en "Lo que no se pudo verificar".

Si no hay conexión a Jira, avisale al usuario en una línea y pedile el estado del board pegado a mano. No inventes tickets, PRs, estados ni asignados.

## Paso 2: lo que no está escrito (preguntarle a quien se va)

Esto es la mitad del valor del documento y no se puede sacar de ninguna herramienta. Preguntá, en un solo mensaje y sin bloquear el resto si algo no llega:

1. **Acuerdos de palabra**: decisiones o compromisos que no quedaron en Jira (con el equipo, con la cátedra, con otro rol).
2. **Lo que tenías en la cabeza**: qué ibas a hacer la semana que viene, qué estabas siguiendo de cerca y por qué.
3. **Personas**: a quién recurrir para qué (quién sabe del backend, quién destraba deploys, quién responde en la cátedra).
4. **Accesos**: qué herramientas, canales o configuraciones necesita quien llega (MCP de Jira, webhook de Discord, documentos compartidos, permisos en GitHub). **Solo el nombre de cada acceso y dónde se configura — nunca el valor.** Si el usuario pega un secreto (URL de webhook, token, contraseña), no lo copies al documento: avisale y reemplazalo por "pedírselo a <quien se va>".
5. **Lo que harías distinto**: un consejo concreto para quien llega (opcional).

Si algo de esto no llega, en el documento va marcado como "sin información de quien se va", no se completa con suposiciones.

## Qué hacer con el input

- Para cada ticket de las próximas entregas, marcá si está en riesgo: no arrancado a menos de 3 días de su due date, bloqueado, o sin asignado.
- Cruzá Jira con los PRs igual que `g07-pr-jira-sync` (ticket en revisión sin PR, PR mergeado con ticket abierto, PR viejo o sin reviewer), pero quedate solo con lo que quien llega tiene que mover — no repitas el reporte completo.
- Marcá aparte los tickets **en revisión con el PR en draft**: el board dice que están para revisar, pero el código todavía no. Es la trampa más común para quien llega, porque mirando solo Jira parece que hay trabajo esperándolo.
- Ordená los pendientes por urgencia: primero lo que vence o se traba esta semana.
- Todo lo que viene de Jira o GitHub lleva su key o número de PR con link. Todo lo que viene de quien se va va atribuido ("según <nombre>").

## Output

Un documento en Markdown, en español, dirigido a quien llega, con esta estructura:

1. `🔁 **Handoff de <rol> — de <quien se va> a <quien llega> — DD/MM**`
2. **⚡ Lo primero que tenés que hacer** — de 3 a 5 acciones concretas para la primera semana, cada una atada a un ticket, PR o fecha. Es la sección más importante: si quien llega solo lee esto, tiene que poder arrancar.
3. **📅 Próximas entregas** — las dos próximas fechas de entrega, con sus tickets agrupados por developer y la marca de riesgo.
4. **🚧 Riesgos y bloqueos vivos** — cada uno con su ticket, por qué es un riesgo y qué se estaba haciendo al respecto.
5. **🔀 PRs y revisión** (TL, PM, QA) — PRs abiertos que necesitan acción, con a quién le toca moverse.
6. **Sección propia del rol**:
   - **PM**: rutinas automáticas que corren solas y cuándo (ver `config.md`), carga por developer, tareas sin asignar.
   - **TL**: convenciones de branches y PRs, estado del CI, decisiones técnicas recientes.
   - **QA**: tickets esperando validación, bugs abiertos por severidad, flujos de regresión que conviene repetir.
   - **PO**: avance por épica (N de M tickets Done), tickets sin due date o sin dueño, qué quedó pendiente para las release notes.
7. **🤝 Acuerdos, personas y accesos** — lo del Paso 2, atribuido a quien se va.
8. **🧰 Herramientas del rol** — qué skills y rutinas del repo usa este rol y para qué (de `config.md`), en una línea cada una.
9. **❓ Lo que no se pudo verificar** — consultas que fallaron, información que quien se va no pasó, supuestos.

Usá Markdown simple (headers, listas, negritas), sin tablas, para que se pueda pegar en Discord o en un Google Doc sin romperse. Omití las secciones vacías salvo la 2 y la 9.

Ver `example-output.md` en esta carpeta para un ejemplo del formato.

## Qué no hacer

- No muevas tickets, no reasignes, no comentes en Jira ni en GitHub. Esta skill documenta; si el usuario pide reasignar los tickets de quien se va, hacelo ticket por ticket con confirmación explícita.
- No copies secretos al documento, aunque el usuario los pegue.
- No inventes acuerdos, contactos ni decisiones: si no vinieron de quien se va, no están.
- No mandes el documento a Discord salvo que el usuario lo pida, y con confirmación antes de enviar: puede tener información que quien se va no quiere en el canal general. Si lo pide: resolvé el webhook con la variable de entorno cuyo nombre figura en `config.md` (o la línea "Discord webhook URL" de `config.local.md` en esta carpeta; si no existe, que copie `config.local.example.md`), armá `payload.json` con `{"content": "<documento>"}` (un POST por sección si pasa los ~2000 caracteres) y enviá con `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`. Nunca imprimas la URL.

## Ejemplo de uso

**Pedido:** Armá el handoff de TL: me voy yo (Marco) y lo asume Denise desde hoy.

**Resultado:** Trae de Jira las dos próximas entregas y los bloqueos vivos, cruza los tickets con los PRs abiertos y te pregunta los acuerdos, las personas y los accesos que no están escritos. Devuelve un documento dirigido a Denise con lo primero que tiene que hacer, las entregas con su riesgo, los PRs que necesitan acción, lo propio del rol y lo que no se pudo verificar. No mueve tickets ni comenta en GitHub.
