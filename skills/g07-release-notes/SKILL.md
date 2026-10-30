---
name: g07-release-notes
description: "Genera las release notes de una entrega a partir de los tickets Done en Jira (MCP) y los PRs mergeados en GitHub, agrupadas por épica, en lenguaje de usuario y con lo que quedó pendiente al final. Usar cuando el PO quiera comunicar qué hay de nuevo en el producto a usuarios, stakeholders o la cátedra después de una entrega o un sprint."
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - despliegue
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - github
  - discord
  grupo: "07"
  autor:
    nombre: Josefina Sapag
    github: jmsapag
  responsables:
  - jmsapag
  madurez: usado-en-proyecto
  relacionados:
  - g07-pr-jira-sync
  - g07-delivery-digest
---

# Release Notes

Generá las notas de versión de una entrega del producto. A diferencia de `g07-delivery-digest` (qué vence y para quién) o `g07-sprint-retro` (cómo trabajó el equipo), esta skill le habla a alguien que **usa** el producto: qué puede hacer hoy que antes no podía. Es la voz del PO, no la del PM.

## Cuándo usar esta skill

Cuando el usuario pida "release notes", "changelog", "qué salió esta semana", "novedades del producto", o necesite comunicar una entrega a stakeholders o a la cátedra.

## Setup (una sola vez)

- **Jira**: MCP de Atlassian conectado a Claude Code (`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/sse --scope user`).
- **GitHub**: CLI `gh` autenticado (solo lectura).
- **Datos del proyecto**: completá `config.md` en esta carpeta (Jira, repo, día de entrega, audiencia y tono).
- **Discord (opcional)**: webhook en la variable de entorno que indica `config.md`, o en `config.local.md` (copiá `config.local.example.md`).

## Configuración

`config.md` en esta carpeta: nombre del producto, site y project key de Jira, repo de GitHub, día de entrega, audiencia y tono. Si algún valor sigue con un placeholder (`<...>`), pedíselo al usuario y ofrecé guardarlo.

## Paso 0: qué entrega

El equipo entrega por ciclos usando el campo **Due date** de Jira, en el día de entrega que indica `config.md`.

1. Si el usuario nombra una fecha ("las release notes del 29/10"), esa es la **fecha de entrega**.
2. Si nombra un sprint, usá `sprint = "<nombre>"` en vez de la due date en las consultas de abajo.
3. Si no dice nada, usá la fecha de entrega más reciente que sea ≤ hoy (si hoy es día de entrega, es hoy).

Dejá explícita la entrega elegida en el título.

## Paso 1: qué se entregó (Jira)

Con la tool MCP que termine en `searchJiraIssuesUsingJql`, formato `markdown`:

1. Entregado: `project = <KEY> AND duedate = "<fecha de entrega>" AND statusCategory = Done ORDER BY parent, key` — campos `summary`, `description`, `parent`, `issuetype`, `assignee`.
2. Comprometido pero no entregado: `project = <KEY> AND duedate = "<fecha de entrega>" AND statusCategory != Done ORDER BY key` — campos `summary`, `status`, `parent`.

Paginá hasta `hasNextPage = false`.

Si las descripciones siguen una plantilla (por ejemplo User Story / Contexto / Alcance / Criterios de aceptación), de cada ticket entregado quedate con:
- la línea **"Como … quiero … para …"** → es la materia prima del texto para usuarios;
- los bullets de **Alcance** que describen comportamiento visible (no los de implementación).

## Paso 2: confirmación con el código (GitHub)

Traé los PRs mergeados en una ventana que cubra la entrega (desde ~10 días antes de la fecha de entrega):

```
gh pr list --repo <repo> --state merged --search "merged:>=<YYYY-MM-DD>" --json number,title,headRefName,mergedAt,url --limit 200
```

Sacá las keys de Jira de cada PR buscando `<KEY>-<número>` en el título y en la branch, y armá un índice key → PRs (`by_key`). Si tenés instalada la skill `g07-pr-jira-sync`, podés usar su `pr_snapshot.py` en lugar de este comando: devuelve el mismo índice ya armado.

Para cada ticket Done, buscalo en `by_key`:
- con PR `MERGED` → entra a las notas normalmente;
- sin PR mergeado → entra igual (puede ser un ticket sin código, por ejemplo de diseño), pero marcalo en la sección interna de verificación al final;
- un PR mergeado en la ventana cuyo ticket **no** está en Done para esa fecha → no lo agregues a las notas, mencionalo en la verificación.

Si `gh` falla (sin instalar, sin auth, sin red), seguí solo con Jira y decilo en la verificación.

## Paso 3: escribir

Reglas de redacción:
- **Lenguaje de usuario.** "Ahora podés generar un cuestionario con IA a partir de un archivo del grupo", no "endpoint POST /quizzes/generate". Nada de endpoints, tablas, componentes ni nombres de clases.
- **Agrupar por épica** (el `parent` del ticket), con el nombre de la épica como sección. Los tickets de backend y frontend de una misma funcionalidad se funden en **un solo ítem** — al usuario no le importa que fueron dos tickets.
- Un ítem = una o dos líneas, empezando por lo que el usuario puede hacer. Entre paréntesis, las keys de Jira que lo componen.
- Arriba de todo, **Lo más destacado**: los 1–3 cambios con más impacto para un usuario, en una frase cada uno.
- Mejoras internas sin efecto visible (performance, fixes de concurrencia, refactors) van juntas en una sola sección corta "Bajo el capó", en una línea cada una y en criollo ("la generación con IA ya no deja conexiones colgadas").
- No inventes beneficios que el ticket no menciona.

## Output

Markdown, con esta estructura:

1. `🚀 **<producto> — novedades de la entrega del DD/MM**`
2. **✨ Lo más destacado**
3. Una sección por épica (`### <nombre de la épica>`) con sus ítems.
4. **🔧 Bajo el capó** (si hay).
5. **⏳ Quedó para la próxima** — tickets comprometidos no entregados, en una línea cada uno, en lenguaje de usuario y sin culpas.
6. Separado por una línea, **Verificación (interno, no publicar)**: conteos (tickets Done / con PR mergeado), y cualquier discrepancia del Paso 2. Esta sección no se manda a ningún lado: es para quien genera las notas.

Ver `example-output.md` en esta carpeta.

## Envío

Mostrá las notas en el chat y preguntá si las querés en Discord. A diferencia de los avisos automáticos, esto le habla a gente de afuera del equipo: **no lo mandes sin confirmación**. Si dicen que sí, mandá todo **menos la sección de verificación**:

1. **Resolvé la URL del webhook**, en este orden: la variable de entorno cuyo nombre figura en `config.md`; la línea "Discord webhook URL" de `config.local.md` en esta carpeta. Si no hay ninguna, avisá en una línea (que copie `config.local.example.md`).
2. Armá el JSON en un archivo temporal `payload.json` en el directorio de trabajo.
3. Hasta ~2000 caracteres por mensaje: si entra, un POST con `{"content": "<notas>"}`; si no, un POST por sección, en orden, sin cortar ninguna.
4. Enviá con exactamente esta forma, URL literal al final: `curl -sS -X POST -H "Content-Type: application/json" -d @payload.json <URL>`.
5. Nunca imprimas la URL. Confirmá si salió bien (204) o mostrá el error tal cual, sin reintentar en loop.

## Ejemplo de uso

**Pedido:** Armame las release notes de la entrega del 29/10.

**Resultado:** Busca los tickets Done con esa due date, los confirma contra los PRs mergeados, y escribe las notas en lenguaje de usuario agrupadas por épica, con lo más destacado, 'Bajo el capó', lo que quedó pendiente y una verificación interna; las manda a Discord solo si confirmás.
