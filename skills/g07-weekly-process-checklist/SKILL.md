---
name: g07-weekly-process-checklist
description: "Mantiene un único Google Doc que responde semana a semana las preguntas de proceso que pide la cátedra (organización del trabajo, avance visible, decisiones, riesgos y seguimiento semanal), usando Jira en vivo (MCP) para lo verificable y pidiéndole al PM las decisiones de la semana. Usar cuando el PM tenga que preparar o actualizar la evidencia de proceso para la clase o la entrega."
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
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
  - google-drive
  grupo: "07"
  autor:
    nombre: Josefina Sapag
    github: jmsapag
  responsables:
  - jmsapag
  madurez: usado-en-proyecto
  relacionados:
  - g07-sprint-status-report
  - g07-sprint-retro
---

# Weekly Process Checklist

Mantené un documento único en Google Drive que responde literalmente las preguntas de proceso que pide la cátedra de Laboratorio 4 (los cinco bloques de abajo; si tu materia usa otra rúbrica, reemplazá esos bloques), y que crece semana a semana en vez de reescribirse. A diferencia de `g07-sprint-status-report` o `g07-sprint-retro` (un reporte puntual centrado en el sprint, que va a Discord), esta skill está organizada alrededor de la rúbrica de la cátedra, no del sprint, y su destino es un documento vivo que la cátedra puede leer.

## Cuándo usar esta skill

Cuando el PM (usuario) necesite preparar la evidencia de proceso antes de una clase o entrega, o actualizar el documento después de algo que cambió (una decisión nueva, un riesgo detectado, el cierre de la semana).

## Setup (una sola vez)

1. **Jira**: conectá el MCP de Atlassian a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`).
2. **Google Drive**: conectá el conector de Google Drive (en claude.ai → Conectores, o el MCP de Google Drive en Claude Code).
3. **Datos del proyecto**: completá en `config.md` el nombre del proyecto, el site y el project key de Jira. El **Google Doc ID** dejalo con el placeholder: la primera corrida crea el documento y lo guarda solo.

## Configuración

Leé `config.md` de esta carpeta. Ahí están los datos de Jira, el nombre del proyecto y el **Google Doc ID** del documento vivo. El ID no es un secreto (no sirve sin acceso OAuth a Drive), por eso vive en `config.md` versionado.

Si el Google Doc ID sigue con el placeholder, es la primera corrida: creá el documento (Paso 0) y guardá el ID devuelto en `config.md` con Edit, para que las próximas corridas lo reusen.

Herramientas de Google Drive: buscá `mcp__claude_ai_Google_Drive__*` o `mcp__*_Google_Drive__*` entre tus tools (puede pedir aprobación la primera vez, es esperable). Si no hay ninguna conectada, avisale al PM en una línea y no sigas — no hay forma de generar el documento sin eso.

## Estructura del documento

El documento tiene dos partes, porque el criterio de la cátedra es "primero ordenar el proceso, después ajustar el contenido":

1. **Proceso de seguimiento** (arriba de todo, se escribe una sola vez en la primera corrida). Responde el bloque 5 de preguntas (cómo van a saber si hubo avance, qué van a reportar siempre, qué evidencia mínima, qué formato, qué no puede faltar). Solo se reescribe si el PM avisa que el proceso cambió.
2. **Entradas semanales** (debajo, en orden cronológico, la más nueva al final). Cada corrida agrega una entrada con fecha que responde los bloques 1 a 4 (organización, avance, decisiones, riesgos). Nunca se borra ni se reescribe una entrada anterior — es el historial que la cátedra quiere ver.

## Paso 0: documento nuevo vs. documento existente

- Si `config.md` ya tiene un Google Doc ID real: leé el contenido actual con la tool de lectura de Google Drive (`read_file_content` o `download_file_content`) antes de escribir nada. Necesitás el contenido completo, no solo metadata: para no pisar el historial y para comparar con la última entrada (Paso 2).
- Si no existe: creá el documento (`create_file`) con el título `<proyecto> — Seguimiento de proceso`, escribí la sección "Proceso de seguimiento" preguntándole al PM las 5 preguntas del bloque 5 en el chat (no las inventes — son decisiones de equipo, no datos de Jira), y guardá el ID devuelto en `config.md`.

## Paso 1: lo verificable de Jira

**Si tenés tools MCP de Atlassian** (una tool cuyo nombre termine en `searchJiraIssuesUsingJql`):

1. Sprint activo: `project = <KEY> AND sprint in openSprints() ORDER BY status`. Traé key, resumen, estado, asignado e `issuelinks`. Paginá hasta `hasNextPage = false`.
2. Señales de riesgo: primero `Flagged = Impediment`; después links "Blocks" / "is blocked by" sobre issues no terminadas **cuyo bloqueante tampoco esté Done** (un link a una issue ya terminada no es un riesgo vivo). No inventes riesgos sin una de estas dos señales o sin que te los pase el PM.
3. Si no hay sprint activo, chequeá `sprint in futureSprints()` y decí explícitamente que no hay sprint en curso, en vez de simular avance.
4. Si la consulta falla o no hay tools de Jira, avisale al PM en una línea y pedile el estado del board pegado a mano.

No inventes tareas, asignados, estados ni bloqueos.

## Paso 2: qué cambió desde la última clase

Comparando con la última entrada semanal del documento:

- Qué issues cambiaron de estado desde esa fecha.
- Qué issues aparecieron y cuáles se completaron.
- Si es la primera entrada, decilo: es la línea de base, no hay con qué comparar.

## Paso 3: input manual del PM (siempre)

Pedile al PM, en el mismo mensaje:

1. **Decisiones de la semana**: qué se decidió, por qué, quién participó, qué alternativa se descartó. Es 100% input del PM. Si no hubo decisiones relevantes, escribilo así ("no se registraron decisiones de producto/proceso esta semana") en vez de inventar una.
2. **Riesgos u oportunidades que no estén en Jira** (opcional).
3. **Evidencia adicional** (opcional): capturas, demo, PRs, lo que el PM quiera sumar al link del board.

No bloquees el documento esperando todo: si algo no llega, marcalo como no disponible esa semana.

## Qué responder en cada bloque

Respondé cada pregunta de forma literal y específica, atada a datos concretos (issue keys, nombres, fechas) — nunca con una frase genérica que serviría para cualquier semana o equipo.

**1. Organizar su trabajo**
- ¿Cómo van a ordenar el trabajo para no perder foco? (metodología: sprints, board, etc. — no cambia seguido)
- ¿Quién se hace cargo de cada tarea? (asignados de Jira)
- ¿Cuál es el objetivo inmediato del equipo para esta semana? (goal del sprint si Jira lo expone; si no, pedíselo al PM)
- ¿Qué tareas concretas deben hacerse primero y por qué? (prioridad del board + razón del PM)
- ¿Qué dependencias existen entre las tareas? (issuelinks)

**2. Hacer visible el avance**
- ¿Cómo van a mostrar el progreso de forma simple? (link al board + este documento)
- ¿Qué avance concreto pueden mostrar hoy? (issues Done desde la última entrada)
- ¿Qué cambió desde la última clase? (Paso 2)
- ¿Qué parte está terminada, en curso o pendiente? (desglose por estado)
- ¿Qué evidencia respalda este avance? (issue keys + evidencia del Paso 3)

**3. Registrar decisiones**
- Las 5 preguntas del bloque salen del input del Paso 3 (qué, por qué, quién, dónde queda registrada — la respuesta a "dónde" es este documento — y qué alternativa se descartó).

**4. Identificar riesgos y oportunidades**
- ¿Qué puede salir mal o bien en el corto plazo? (señales de Jira + input del PM)
- ¿Quién se hace responsable de seguirlo? (si el PM lo dice; si no, "pendiente de asignar")
- ¿Qué bloqueo, dependencia o problema podría frenar al equipo? (Flagged + issuelinks)
- ¿Qué riesgo es más urgente y por qué? (el que bloquea más issues o el que marque el PM)
- ¿Qué acción concreta van a tomar? (del PM; si no la da, queda como pregunta abierta)

**5. Sostener seguimiento semanal con evidencias**
- Se responde una sola vez, en "Proceso de seguimiento" (Paso 0).

## Output

Un bloque en Markdown por entrada semanal, con fecha en el título (`## Semana del DD/MM`) y cuatro subsecciones: **Organización**, **Avance**, **Decisiones**, **Riesgos y oportunidades** — en texto corrido o listas cortas, no como cuestionario con la pregunta repetida.

Mostrale al PM la entrada completa en el chat antes de subirla.

Ver `example-output.md` en esta carpeta (incluye la sección fija de "Proceso de seguimiento").

## Cómo se sube a Google Drive

1. Tomá el contenido completo que leíste en el Paso 0 (todo el historial).
2. Agregá la entrada nueva al final, sin tocar ni reordenar nada anterior.
3. Escribí el documento completo con la tool de escritura (`update_file`), no solo la entrada nueva: la API reemplaza el contenido entero, y si mandás solo lo nuevo se pierde el historial.
4. Confirmale al PM si salió bien, con el link (`https://docs.google.com/document/d/<ID>`).
5. No compartas el documento (`share_file`) salvo que el PM lo pida explícitamente en ese mensaje: es una acción visible para terceros.

## Ejemplo de uso

**Pedido:** Actualizá el documento de proceso de esta semana. Decisión: usamos JWT en vez de sesiones; participaron Franco y Valentina.

**Resultado:** Lee el Google Doc existente, trae de Jira el sprint activo y los riesgos vivos, agrega al final una entrada 'Semana del DD/MM' con Organización, Avance, Decisiones y Riesgos, te la muestra y reescribe el documento completo sin tocar las semanas anteriores.
