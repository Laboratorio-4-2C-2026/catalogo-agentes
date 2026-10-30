---
name: g07-delivery-digest
description: "Publica en Discord los avisos de un equipo que entrega por ciclos usando el Due date de Jira (MCP), en dos modos: el día de entrega (qué vence hoy y qué quedó asignado para la próxima) y a mitad de ciclo (cómo vienen las tareas de la próxima entrega, con su riesgo). Usar desde una rutina programada o cuando el PM quiera ver o probar los avisos fuera de horario."
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
  - g07-ready-check
---

# Delivery Digest

Generá y publicá en Discord los avisos de seguimiento de un equipo que entrega por ciclos fijos (por ejemplo, de jueves a jueves), usando el campo **Due date** de Jira como fuente de verdad. No depende de que el PM pegue nada: está pensada para correr sola desde una rutina programada y trabajar solo con lo que hay en Jira en ese momento.

Tiene dos modos:

- **Entrega** — el día de entrega: qué vence hoy (y qué no llegó) y qué quedó asignado para la entrega siguiente.
- **Mitad de ciclo** — unos días antes: cómo vienen las tareas que vencen en la próxima entrega, a tiempo para reaccionar si algo está frenado.

## Cuándo usar esta skill

- Automáticamente, desde una rutina programada el día de entrega (modo entrega) y el día de chequeo (modo mitad de ciclo).
- A pedido del PM, para ver o probar un aviso fuera de horario ("mostrame el aviso de entrega", "corré el chequeo de mitad de semana").

## Setup (una sola vez)

1. **Jira**: conectá el MCP de Atlassian a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`), o el conector de Atlassian si corre en una rutina en la nube.
2. **Datos del proyecto y del ciclo**: completá `config.md` en esta carpeta (project key, día de entrega, día del chequeo de mitad de ciclo).
3. **Discord**: webhook en la variable de entorno que indica `config.md` (así se configura en una rutina en la nube, donde no hay archivos locales) o en `config.local.md` (copiá `config.local.example.md`) para probar a mano.
4. **Rutinas (opcional)**: programá dos rutinas que invoquen esta skill, una el día de entrega con "modo entrega" y otra el día de chequeo con "modo mitad de ciclo".

## Configuración

Leé `config.md` de esta carpeta. Si el project key sigue con un placeholder (`<...>`), avisale al usuario y no sigas: sin project key no hay forma de calcular esto.

## Paso 0: modo y fechas de referencia

**Modo.** Si quien invoca lo dice (la rutina o el PM: "modo entrega", "aviso de los jueves", "chequeo de mitad de ciclo", "status de los lunes"), usá ese. Si no lo dice: si hoy es el día de entrega, modo entrega; si hoy es el día de chequeo, modo mitad de ciclo; si no es ninguno, preguntá cuál.

**Fechas** (con el día de entrega y el día de chequeo de `config.md`):

- **Modo entrega.** Si hoy es el día de entrega, hoy es la **entrega de referencia**. Si no (el PM está probando a mano), usá la próxima fecha que caiga en el día de entrega y dejalo explícito en el mensaje ("⚠️ generado fuera de horario, usando el DD/MM como referencia") en vez de simular que hoy es día de entrega. La **entrega siguiente** es la de referencia + la duración del ciclo.
- **Modo mitad de ciclo.** Si hoy es el día de chequeo, hoy es el **día de referencia**; si no, el próximo día de chequeo, con el mismo aviso de "fuera de horario". La **entrega objetivo** es la primera fecha de entrega posterior al día de referencia.

## Origen de datos: Jira

Necesitás la tool MCP que ejecuta JQL. **El nombre completo cambia según dónde corre la skill — no asumas uno fijo:** local suele ser `mcp__atlassian__searchJiraIssuesUsingJql`; en una rutina en la nube, el prefijo del conector (por ejemplo `mcp__claude_ai_Atlassian_Rovo__searchJiraIssuesUsingJql`). Buscá cualquier tool cuyo nombre termine en `searchJiraIssuesUsingJql` y usala. Solo si no hay ninguna, tratalo como "sin conexión a Jira".

Consultas:

- **Modo entrega**:
  1. `project = <KEY> AND duedate = "<entrega de referencia, YYYY-MM-DD>" ORDER BY status`
  2. `project = <KEY> AND duedate = "<entrega siguiente, YYYY-MM-DD>" ORDER BY status`
- **Modo mitad de ciclo**:
  1. `project = <KEY> AND duedate = "<entrega objetivo, YYYY-MM-DD>" ORDER BY status`

En todas:

1. **Paginá hasta agotar los resultados.** Si `pageInfo.hasNextPage` es `true`, repetí la consulta pasando `pageInfo.endCursor` como `nextPageToken` y acumulá, hasta que sea `false`. Nunca uses solo la primera página: es la causa más común de que falten tickets sin que la corrida marque error.
2. Para cada issue: key, resumen, estado, asignado.
3. Antes de armar el mensaje, contá cuántas issues juntaste por sección y dejá esa cuenta en tu razonamiento (no hace falta mostrarla): es tu chequeo de que no truncaste nada.
4. Si una consulta falla (error real, no "0 resultados") o no hay tool de Jira, **no envíes nada a Discord**: mostrá en el chat que no se pudo generar el aviso y por qué.
5. Si una consulta no trae issues (sin error), decilo en esa sección del mensaje ("no hay tareas con entrega hoy", "todavía no hay nada asignado para la próxima entrega") en vez de omitirla.

No inventes tareas, asignados ni estados. No envíes el mensaje si sospechás que alguna sección quedó parcial (por ejemplo, paginación cortada): tratalo como el punto 4.

## Qué hacer con el input

Agrupá las issues por developer asignado (las que no tienen asignado, aparte como "Sin asignar").

- **Modo entrega**
  - En **vencen hoy**: marcá ✅ las que están en un estado terminado (Done o equivalente) y ⚠️ las que no — son las que arriesgan no llegar a la entrega.
  - En **próxima entrega**: son tareas recién asignadas, sin juicio de riesgo — solo qué es y para quién.
- **Modo mitad de ciclo** — marcá cada issue según su estado, con criterio de chequeo a mitad de ciclo:
  - ✅ Done o equivalente.
  - 🔧 In Progress, In Review o equivalente ("viene bien" si no hay señales de bloqueo).
  - ⚠️ To Do, Backlog o cualquier estado sin arrancar: a esta altura del ciclo es riesgo real.
  - 🚫 Blocked o equivalente, si Jira lo distingue: es la señal más urgente.

  No compares contra el aviso anterior ni infieras tendencias: el chequeo es sobre el estado actual.

## Output

Un mensaje en Markdown simple (sin tablas), listo para Discord. El nombre del proyecto sale de `config.md`.

**Modo entrega**

1. `📋 **Aviso de entrega <proyecto> — <día> DD/MM**`
2. **📅 Vencen hoy (DD/MM)** — por developer, con ✅/⚠️.
3. **🆕 Para la próxima entrega (DD/MM)** — por developer, o "nada asignado todavía".
4. Un cierre de una línea, con onda y algún emoji (ver abajo).

**Modo mitad de ciclo**

1. `📊 **Status de mitad de ciclo <proyecto> — hacia el DD/MM**`
2. **🗂️ Estado de las tareas** — por developer, cada issue con su marca, o "todavía no hay tareas asignadas para esta entrega".
3. Si hay issues en ⚠️ o 🚫, una línea aparte con cuántas y de quién, para que salte a la vista.
4. Un cierre de una línea, con onda y algún emoji.

**El cierre**: una frase alentadora para el equipo, no un resumen de datos. Distinta cada vez, en tono casual y ajustada a lo que muestra el aviso (si hay varias tareas en riesgo, más "dale que se puede"; si todo está en verde, más festejo). No la repitas igual de una semana a otra.

Ver `example-output.md` en esta carpeta (tiene un ejemplo de cada modo).

## Envío a Discord

El aviso se manda automáticamente apenas se genera (si corre desde una rutina, no hay nadie mirando). Mostralo igual en el chat si hay una sesión interactiva.

1. **Resolvé la URL del webhook**, en este orden: la variable de entorno cuyo nombre figura en `config.md` (así se configura en la nube, donde no existe `config.local.md`); la línea "Discord webhook URL" de `config.local.md` en esta carpeta (para probar a mano). Si no hay ninguna, avisá en una línea y quedate con el mensaje en el chat — no envíes nada.
2. Armá el JSON en un archivo temporal `payload.json` en el directorio de trabajo (no interpoles el mensaje en la línea de comando).
3. Hasta ~2000 caracteres por mensaje: si entra, un POST con `{"content": "<mensaje>"}`; si no, un POST por sección (`## `), en orden, sin cortar ninguna.
4. Enviá con exactamente esta forma, con la URL literal al final — nunca a través de una variable de shell, porque los permisos preaprobados de Claude Code matchean sobre el texto literal: `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`.
5. Nunca imprimas la URL en tu respuesta ni en ningún archivo: es una contraseña del canal, venga de donde venga.
6. Confirmá si salió bien (Discord responde 204 sin contenido) o mostrá el error tal cual, sin reintentar en loop.

## Notas

Si el equipo deja de usar el Due date para las entregas (por ejemplo, vuelve a sprints), esta skill, `g07-sprint-status-report` y `g07-sprint-retro` deberían actualizarse juntas para no quedar inconsistentes.

## Ejemplo de uso

**Pedido:** Corré el g07-delivery-digest en modo mitad de ciclo.

**Resultado:** Calcula la próxima fecha de entrega, trae de Jira las tareas que vencen ese día (paginando hasta el final), las lista por developer con su marca de estado (✅/🔧/⚠️/🚫), resume en una línea cuántas están en riesgo y de quién, y publica el mensaje en Discord.
