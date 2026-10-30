---
name: g07-sprint-status-report
description: "Genera el reporte de estado del sprint en curso a partir de Jira en vivo (MCP) y las novedades del equipo que pegue el PM (standups, bloqueos de Discord), detectando bloqueos, tareas estancadas o sin asignar y desbalance de carga, y lo envía al canal de Discord del equipo. Usar cuando el PM necesite un panorama del avance antes de una reunión, un standup o una entrega."
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
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
  - g07-sprint-retro
  - g07-delivery-digest
  - g07-weekly-process-checklist
---

# Sprint Status Report

Generá un reporte de estado del sprint en curso. El estado del board sale de Jira en vivo (vía MCP); las novedades del equipo (standups, bloqueos reportados en Discord) y el objetivo del sprint los pasa el PM a mano, porque no hay forma de leer Discord automáticamente. El reporte terminado se envía al canal de Discord del equipo apenas se genera (ver "Envío a Discord") — no hace falta pedirlo aparte.

## Cuándo usar esta skill

Cuando el PM (usuario) pida un "reporte de estado", "estado del sprint", "cómo viene el equipo", o quiera detectar bloqueos o tareas estancadas antes de una reunión, standup o entrega.

## Setup (una sola vez)

1. **Jira**: conectá el MCP de Atlassian a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`; si la URL cambió, buscá "Atlassian Remote MCP Server" en la documentación de Atlassian). Con permisos de lectura alcanza.
2. **Datos del proyecto**: completá `config.md` en esta carpeta (site de Jira, project key, board, nombre del proyecto).
3. **Discord (opcional)**: creá un webhook en el canal del equipo y dejalo en la variable de entorno que indica `config.md`, o copiá `config.local.example.md` como `config.local.md` y pegalo ahí. `config.local.md` tiene que estar en el `.gitignore`.

## Configuración

Leé `config.md` de esta carpeta antes de consultar Jira. Si algún valor sigue con un placeholder (`<...>`), avisale al usuario, pedíselo y ofrecé guardarlo en `config.md`; mientras tanto, seguí con el fallback manual.

## Origen de datos: Jira

**Si tenés herramientas MCP de Atlassian en esta sesión** (buscá una tool cuyo nombre termine en `searchJiraIssuesUsingJql`; el prefijo cambia según el entorno):

1. Usá el project key y, si está definido, el board de `config.md`.
2. Consultá las issues del sprint activo: `project = <KEY> AND sprint in openSprints() ORDER BY status`.
3. Traé para cada issue: key, resumen, estado, asignado, y los comentarios recientes que mencionen bloqueos (sirven para la sección de bloqueos). Paginá hasta que `hasNextPage` sea `false`.
4. Si la consulta falla o no hay tools de Jira, avisale al usuario en una línea ("no pude conectar con Jira, ¿tenés el MCP de Atlassian conectado? sigo con lo que me pases a mano") y seguí con el fallback manual.
5. **Si `sprint in openSprints()` no devuelve ninguna issue (sin error), no asumas que el sprint está vacío.** Puede que todavía no se haya iniciado ningún sprint. Verificá con `project = <KEY> AND sprint in futureSprints() ORDER BY status`:
   - Si trae issues, decíselo al PM en el **Resumen general**: no hay sprint activo, el board tiene N issues en el sprint "X" que todavía no se inició, y ofrecé esas issues como contexto de lo planificado, no como "en curso".
   - Si tampoco hay nada, decí que no se encontró actividad de sprint (activo, futuro o backlog asignado) y preguntá si el sprint corresponde a otro board o si todavía no se planificó.
   - Nunca generes las secciones del reporte como si hubiera un sprint en curso cuando no lo hay.

**Fallback manual** (sin MCP, o si el usuario prefiere pegar los datos): pedile el estado del board pegado como texto (issues con estado y asignado). No inventes issues ni estados — si falta info, decilo.

## Otro input, siempre manual

Además de Jira, pedile al usuario (en el mismo mensaje, sin bloquear el reporte si falta algo):

1. **Novedades del equipo**: standups recientes, mensajes de bloqueo, lo que hayan reportado los developers y no esté en Jira.
2. **Objetivo y deadline del sprint**, si no vienen en el nombre o las fechas del sprint de Jira.

Trabajá con lo que haya y marcá qué información falta, en vez de inventarla.

## Qué hacer con el input

Identificá:

- **Tareas estancadas**: mismo estado hace mucho, o sin updates recientes.
- **Bloqueos**: explícitos ("estoy bloqueado por X") o implícitos (depende de una tarea que no avanza, espera de otro equipo o servicio).
- **Desbalance de carga**: developers con muchas tareas en curso vs. otros con pocas o ninguna.
- **Tareas sin asignar**.

No inventes tareas, developers ni estados. Si el input no alcanza para alguna sección, decilo en esa sección.

## Output

Un reporte en Markdown con estas cinco secciones, en este orden:

1. **Resumen general** — progreso del sprint en una o dos líneas, con semáforo (🟢 en curso normal / 🟡 atención / 🔴 riesgo de no llegar) y por qué.
2. **Estado por developer** — tareas en curso, hechas y bloqueadas de cada uno.
3. **Bloqueos y riesgos detectados** — cada uno con su tarea y developer.
4. **Tareas sin asignar o estancadas**.
5. **Recomendaciones para el PM** — acciones concretas atadas a datos del input (reasignar tal tarea, seguir de cerca a tal developer, escalar tal bloqueo). Nada genérico tipo "mejorar la comunicación".

Markdown simple (headers, listas, negritas), sin tablas, para que se lea bien en Discord y sirva de base para un comentario en Jira.

Ver `example-output.md` en esta carpeta.

## Envío a Discord

El reporte se manda siempre, apenas se genera, además de mostrarlo en el chat.

1. **Resolvé la URL del webhook**, en este orden:
   1. la variable de entorno cuyo nombre figura en `config.md` ("Variable de entorno del webhook");
   2. la línea "Discord webhook URL" de `config.local.md` en esta carpeta.

   Si no hay ninguna (o sigue el placeholder), avisale al PM en una línea, indicale que copie `config.local.example.md` como `config.local.md`, y quedate con el reporte en el chat. No pidas la URL para pegarla en la conversación: es un secreto.
2. Armá el JSON en un archivo temporal `payload.json` en el directorio de trabajo (no interpoles el reporte en la línea de comando, por el escaping).
3. Discord acepta hasta ~2000 caracteres por mensaje. Si entra, un solo POST con `{"content": "<reporte>"}`. Si no, un POST por sección (cada bloque que arranca en `## `), en orden, sin cortar ninguna a la mitad.
4. Enviá con exactamente esta forma, con la URL literal al final (si tenés este comando preaprobado en los permisos de Claude Code, el permiso matchea sobre el texto literal): `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`.
5. Nunca imprimas la URL en tu respuesta ni la escribas en un archivo versionado.
6. Confirmá si salió bien (Discord responde 204 sin contenido) o mostrá el error tal cual, sin reintentar en loop.

## Ejemplo de uso

**Pedido:** Armame el reporte de estado del sprint. Novedades del standup: Marco está bloqueado esperando el endpoint de login.

**Resultado:** Trae el sprint activo de Jira, arma el reporte en cinco secciones (resumen con semáforo, estado por developer, bloqueos, tareas sin asignar o estancadas y recomendaciones atadas a issues concretas), lo muestra en el chat y lo envía al canal de Discord si hay webhook configurado.
