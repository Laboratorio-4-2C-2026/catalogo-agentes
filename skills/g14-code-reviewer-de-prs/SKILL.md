---
name: g14-code-reviewer-de-prs
description: "Review manual de un PR React + Supabase solicitada por QA: contrasta el diff con los criterios de aceptación del ticket de Jira, busca errores de lógica y riesgos OWASP y comenta en GitHub con Conventional Comments. No corrige, no abre PRs, no audita la DoD ni se dispara sola; la review automática es del bot de review."
metadata:
  tipo: skill
  area:
  - qa
  - seguridad
  fase:
  - revision
  tecnologias:
  - react
  - typescript
  - supabase
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - jira
  grupo: '14'
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: usado-en-proyecto
  relacionados: []
---

# Code reviewer de PRs (QA)

## Qué es esto

Protocolo de revisión de código para PRs de `vaiven-app`, pensado para que el QA no tenga que leer y comentar cada PR línea por línea a mano. **Revisa y comenta, nunca corrige código ni abre PRs propios.** Los destinatarios son devs de Lab II de 2do año, recién arrancando: los comentarios tienen que ser claros y explicar el porqué, no solo señalar.

Se dispara a pedido de un QA humano, pasando el número del PR a revisar.

## Marco de referencia

El protocolo no está inventado desde cero: toma prestado de tres fuentes con trayectoria en la industria, para que la revisión tenga el mismo rigor que un reviewer senior entrenado, no solo los pasos que se le ocurrieron a un QA sin experiencia previa.

- **Conventional Comments** ([conventionalcomments.org](https://conventionalcomments.org/)): el estándar de prefijos y decoradores que se usa en el paso 8, para que cada comentario diga de entrada qué tipo de observación es y si bloquea el merge o no.
- **Google Engineering Practices, "The Standard of Code Review"** ([google.github.io/eng-practices](https://google.github.io/eng-practices/review/reviewer/)): el criterio de fondo que guía cómo se comenta. El propósito de una review es mejorar la salud del código a lo largo del tiempo, no encontrar la mayor cantidad de errores posible. De acá sale la regla de comentar sobre el código y nunca sobre quien lo escribió, priorizar hechos técnicos por sobre preferencias personales, y marcar como no bloqueante (`nitpick:`) todo lo que sea educativo pero no crítico.
- **OWASP Code Review Guide** y **OWASP Top 10** (referencia vigente, no la edición 2013 sola): la lista de chequeo de la Categoría C no es una lista improvisada de cuatro puntos, sigue las familias de vulnerabilidad que ese proyecto documenta para revisión de código fuente (control de acceso roto, fallas de autenticación/sesión, inyección, exposición de datos sensibles, confianza indebida en el cliente), adaptadas al stack real de VaiVen.
- **OWASP Cheat Sheet Series** ("DOM-based XSS Prevention") y **OWASP ASVS, capítulo V5 (Validation, Sanitization and Encoding)**: `vaiven-app` es una SPA sin backend propio, así que además de las familias generales de arriba, la Categoría C suma los riesgos específicos de un frontend React + Vite que un OWASP Top 10 genérico no nombra por sí solo (XSS en el DOM, fuga de variables de entorno del bundle, autorización que vive solo en la UI, manejo del token de sesión).

**Sobre asumir buena fe (Google Engineering Practices):** la guía es explícita en que un reviewer no fuerza su propia preferencia sobre algo que no le corresponde decidir, y que hay que asumir competencia y buena fe en quien escribió el código. Este agente extiende ese principio a las decisiones de proceso: si el PR ya da una razón para algo que el ticket exige justificar —aunque sea informal, aunque no cite el nombre exacto de quién decidió— se toma de buena fe y no se comenta. El agente audita el código contra el ticket, no la legitimidad de decisiones humanas de las que no tiene forma de tener evidencia (una reunión, un mensaje, una indicación verbal). Ver paso 5.

## Requisitos

- `gh` CLI instalado y autenticado con acceso a `vaiven-austral/vaiven-app` (`gh auth login`, o `GITHUB_TOKEN`/`GH_PAT` con scope `repo`).
- `python3` disponible (para `scripts/diff-line-map.py`, el script determinista que calcula a qué línea real ancla cada comentario — ver paso 1).
- Credenciales de Jira Cloud (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`) — las mismas que usan los demás agentes que leen Jira (por ejemplo, el auditor de Jira). Ahí se busca el ticket de cada PR y sus criterios de aceptación. **No hace falta `vaiven-direccion` clonado.**
- Una sesión de Claude Code abierta en `vaiven-agentes`.

## Protocolo de ejecución

### 0. Chequear si este PR ya se revisó

Antes de traer el diff, listar las reviews existentes del PR (`gh api repos/vaiven-austral/vaiven-app/pulls/<numero>/reviews`) y buscar un marcador oculto con el formato `<!-- code-reviewer-de-prs:sha:<SHA> -->` en el `body` de alguna (se explica en el paso 8). Si ya existe un marcador con el SHA del último commit del PR, esa versión del código ya fue revisada — avisarlo y preguntar si de todas formas se quiere repetir la revisión (puede haber un motivo puntual para pedir una segunda mirada).

Si el QA pide explícitamente revisar un PR sabiendo que ya tiene marcador, se revisa igual — este paso es para evitar el olvido, no para bloquear un pedido explícito.

### 1. Traer el PR

```bash
gh pr view <numero> --repo vaiven-austral/vaiven-app --json title,body,headRefName,headRefOid,url,author
gh pr diff <numero> --repo vaiven-austral/vaiven-app | python3 scripts/diff-line-map.py
```

`headRefOid` es el SHA del último commit: guardarlo, se usa en el paso 0 y en el marcador del paso 8. `author.login` es el usuario de GitHub al que se arroba en el resumen (paso 8), para que le llegue la notificación.

El diff pasa siempre por `scripts/diff-line-map.py` (no leer `gh pr diff` crudo): anota cada línea con su número real en la versión nueva del archivo (`[+N]`/`[ N]`) o marca que no existe en la versión nueva (`[-old]`). Los números que aparecen ahí son los que se usan tal cual para anclar cada comentario en el paso 8 — no se cuentan a mano ni se recalculan.

### 2. Detectar ramas apiladas

Comparar los commits del PR (`gh pr view <numero> --repo vaiven-austral/vaiven-app --json commits --jq '.commits[].messageHeadline'`) contra el ticket que aparece en el título o la rama del PR. Si aparecen commits de **otro** ticket (ej. el PR es de SCRUM-112 pero trae commits "SCRUM-108: ..." o "SCRUM-111: ..."), esta rama está apilada sobre otra que todavía no se mergeó a `main` — pasa seguido cuando un mismo dev encadena varios PRs.

Cuando esto pasa, **revisar solo los commits que corresponden al ticket de este PR**, no el diff completo contra `main` (ese diff completo le atribuiría a esta dev cambios de otro PR, que tiene su propia revisión):

```bash
# Un solo commit propio al final de la rama:
gh api repos/vaiven-austral/vaiven-app/commits/<SHA_DEL_COMMIT_PROPIO> -H "Accept: application/vnd.github.v3.diff"

# Un rango de varios commits propios (desde el último commit ajeno hasta el propio más reciente):
gh api "repos/vaiven-austral/vaiven-app/compare/<SHA_ULTIMO_COMMIT_AJENO>...<SHA_PROPIO_MAS_RECIENTE>" -H "Accept: application/vnd.github.v3.diff"
```

**El anclaje de los comentarios (paso 8) siempre usa los números de línea del diff completo del PR** (`gh pr diff <numero> | python3 scripts/diff-line-map.py`, paso 1) — GitHub valida los comentarios de una Review contra ese diff completo, nunca contra uno aislado por commit. Aislar el commit es solo para decidir *qué revisar*, no para calcular las líneas.

Declarar en el resumen (paso 8) qué archivos quedaron fuera de esta revisión por pertenecer a otro ticket/PR — para que quede explícito que no se ignoraron por descuido, sino porque tienen su propia revisión en otro lado.

### 3. Ubicar el ticket, vía Jira

Buscar en el título del PR, el nombre de la rama (`headRefName`, ej. `feat/H3-2.3-piso-de-rls`) o el cuerpo del PR una referencia reconocible a un ticket (ej. `H3-2.3`, `tarea-6`).

Con ese ID, buscar el issue en Jira Cloud por API (mismas credenciales que usan los demás agentes que leen Jira):

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -G "$JIRA_BASE_URL/rest/api/3/search" \
  --data-urlencode 'jql=summary ~ "H3-2.3"' \
  --data-urlencode 'fields=summary,description'
```

Tomar el issue cuyo `summary` contiene el ID exacto. Su `description` trae ya publicados el objetivo, la guía de implementación y los **criterios de aceptación** (`auditor-de-jira` mantiene esto sincronizado desde el archivo del repositorio).

**Si no se encuentra ninguna referencia reconocible en el PR, o ningún issue de Jira matchea:** igual publicar una Review (paso 8), pero con `comments: []` vacío y el `body` diciéndolo explícito ("No pude identificar el ticket asociado a este PR, indicá cuál es para poder revisar contra sus criterios de aceptación") — no seguir con las categorías B y C inventando contra qué revisar el resto del PR.

### 4. Calibrar el esfuerzo de revisión según el riesgo y el tamaño

No todo diff merece el mismo nivel de escrutinio. Antes de entrar en las categorías A/B/C, clasificar el cambio:

- Si el diff toca autenticación, RLS, manejo de sesión o cualquier tabla con datos de usuarios: máximo escrutinio en la Categoría C.
- Si el diff toca lógica de negocio central (motor de matching, estados de publicación): máximo escrutinio en la Categoría B.
- Si es un refactor sin cambio de comportamiento declarado: foco en mantenibilidad, no repetir de cero el análisis funcional.
- Si el diff supera aproximadamente 400 líneas cambiadas: es más grande de lo que la evidencia de la industria considera revisable con calidad pareja en una sola pasada. Publicar esto como una observación (`suggestion:`, no bloqueante) sugiriendo partirlo en el resumen, y seguir revisando igual, priorizando los archivos de mayor riesgo según los dos puntos anteriores.

### 5. Categoría A · Alineación con los criterios de aceptación

Leer los Criterios de Aceptación de la `description` del issue (traída en el paso 3) y evaluar cada uno contra el diff y la descripción del PR: **cumple / no cumple / sin evidencia suficiente**.

Esta categoría **no incluye** la tabla de Definition of Done del ticket ni citas de ADR — quedan fuera del alcance de este agente a propósito, para no depender de archivos de `vaiven-direccion` (ver la ficha, sección "Límites conocidos").

**Regla de buena fe, la parte que más importa de esta categoría:** un criterio que exige justificar algo (una exclusión, una reclasificación, un agregado fuera de lo pedido) se marca como **comentario individual solo cuando el PR no dice absolutamente nada al respecto** — silencio total. Si el PR ya da una razón, aunque sea informal ("se decidió en la reunión del X", "lo pidieron durante el trabajo"), el criterio se marca **cumple** en el resumen del paso 8 y **no genera comentario individual**. No se audita el detalle de la razón, ni se pide más nombre o papeleo del que el PR ya dio — eso es cuestionar un proceso humano del que el agente no tiene ni puede tener evidencia propia, y no es su trabajo.

### 6. Categoría B · Lógica y errores funcionales

- ¿El diff hace lo que el ticket pide, sin romper casos borde (input vacío, `null`, error de red o de la API externa)?
- ¿Contradice o duplica lógica de negocio que ya existe en otra parte del código?
- ¿Los estados o flujos del dominio (ej. publicación `borrador/publicada/pausada/finalizada`) se validan correctamente, sin permitir transiciones inválidas?

### 7. Categoría C · Seguridad (OWASP Code Review Guide + OWASP Top 10, adaptado al stack de VaiVen)

- **Control de acceso roto:** ¿toda tabla nueva o tocada por una migración de este PR tiene política RLS asociada? ¿alguna quedó con una condición demasiado permisiva (ej. `USING (true)`) sin justificación?
- **Fallas de autenticación y sesión:** ¿algún flujo asume que un JWT es válido sin verificarlo (verificación local, no requiere llamada a Supabase), o confía en el estado de sesión del cliente sin revalidar del lado del servidor?
- **Confianza indebida en el cliente:** ¿se valida del lado del servidor (política RLS, validación en n8n) lo que llega del frontend, o se confía en el dato tal cual llega del cliente?
- **Exposición de datos sensibles / gestión de secretos:** ¿hay claves, tokens o URLs escritas directamente en el código en vez de leídas de variables de entorno? ¿aparece la `service_role key` en código de frontend (`app/src/`) en vez de la `anon key`? Es una fuga grave, marcar siempre como `issue:`.
- **Inyección:** ¿alguna query arma SQL o filtros por concatenación de strings en vez de parámetros o el builder de Supabase?
- **XSS en el DOM (React):** ¿el PR usa `dangerouslySetInnerHTML`, renderiza Markdown/HTML que viene de otro usuario sin sanitizar, o arma un `href`/`src` con un valor de usuario sin validar (URL `javascript:` incluida)? React escapa por default — esto solo aparece cuando el código lo evita a propósito.
- **Fuga de variables de entorno de Vite:** cualquier variable con prefijo `VITE_` queda pública en el bundle compilado, sin importar la intención con la que se la agregó. ¿El PR suma una `VITE_*` que en realidad debería quedar solo del lado de n8n/Supabase?
- **Autorización que vive solo en la UI:** ¿el PR oculta un botón, una ruta o una sección según el rol del usuario **sin** que haya una política RLS o una validación en n8n protegiendo el dato o la acción detrás? Ocultar en la interfaz no es una barrera de seguridad, solo evita que se vea.
- **Manejo del token de sesión:** ¿el PR loguea, envía a un tercero (analytics, reporte de errores) o expone de alguna forma nueva el token que Supabase Auth guarda en `localStorage`?

**Fuera de esta categoría, a propósito:** CSRF (bajo riesgo real acá, Supabase Auth usa JWT en headers, no cookies), dependencias npm vulnerables (chequeo determinista, no de lectura de diff — ver "Lo que este agente no hace"), y headers de seguridad / infraestructura (viven en `vercel.json`, fuera del código de una feature).

### 8. Comentar en GitHub — una sola Review, con comentarios inline

**Por qué una Review y no comentarios sueltos:** un comentario de conversación (`gh pr comment`) no tiene botón de respuesta ni de "resolver" — la dev no tiene dónde contestar "no aplica" de forma legible, y nadie puede ver de un vistazo qué quedó sin atender. Una **Review de GitHub**, con cada hallazgo como comentario inline anclado a su línea, sí tiene las dos cosas nativas. El agente publica **una Review por corrida**, nunca comentarios sueltos.

Cada hallazgo sigue el estándar Conventional Comments. Prefijo obligatorio según el tipo de observación:

- `issue:` (bloqueante, con `(blocking)` explícito si conviene reforzarlo)
- `suggestion:` (mejora, no bloquea)
- `question:` (falta información para decidir)
- `nitpick:` (cosmético, no importa si no se cambia)
- `praise:` (algo bien resuelto, vale nombrarlo: reforzar buenos patrones también mejora la salud del código a futuro, no solo señalar lo que está mal)

Para cada uno:
- **Explicar el porqué**, no solo señalar (ej. "esto puede fallar si el usuario borra la sesión a mitad de la subida de la foto" en vez de "esto está mal").
- **Orientar la corrección en palabras**, sin escribir el código completo de la solución. Apuntar el archivo/patrón, no entregar el diff resuelto (restricción del equipo: revisar y comentar, nunca escribir).
- **Comentar sobre el código, nunca sobre quien lo escribió** (Google Engineering Practices).
- **Tono claro, sin jerga sin explicar.** Quien lee recién arranca 2do año.
- **Pedir una reacción, según severidad:** los `issue:`/`suggestion:`/`question:` cierran con *"Reaccioná con 👍 si lo vas a corregir, o comentá acá por qué no aplica."* — el pedido va en palabras, el emoji solo ilustra cuál (un 👍 suelto sin la palabra "reaccioná" no se entiende como un pedido de reacción de GitHub). Los `nitpick:`/`praise:` no piden nada — son justo los que no necesitan respuesta.

**Armar el payload de la Review** en un archivo temporal (nunca pasar el JSON entero como argumento de shell — los textos tienen comillas, backticks y tildes que rompen el escapado). Usar la herramienta de edición de archivos para escribir algo como:

```json
{
  "body": "🤖 Comentario generado automáticamente por un agente de IA. Puede cometer errores. Sentite libre de responder \"no aplica\" o discutir cualquier observación con la que no estés de acuerdo. La palabra final es de un humano.\n\n@<author.login>\n\n---\n\n**Ticket:** SCRUM-110 (identificado)\n\n**Qué se revisó:**\n- **A · Criterios de aceptación** (5): 3 cumplen, 2 con observación\n- **B · Lógica y casos borde:** revisado (fallback de sesión, toggle de password, ruteo 404, badges de tipo). Sin hallazgos.\n- **C · Seguridad:** revisado (RLS — no aplica, sin tablas nuevas; secrets/VITE_; XSS en el DOM; autorización solo-UI; token de sesión). 1 sugerencia no bloqueante.\n\n**Veredicto:** aprobado con observaciones\n\n<!-- code-reviewer-de-prs:sha:c19138a2d18744cdab42f6b34326b6c8e900e5a7 -->",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/lib/supabaseClient.ts",
      "line": 12,
      "side": "RIGHT",
      "body": "suggestion: el fallback usa un dominio real (`missing-supabase-url.supabase.co`)... Reaccioná con 👍 si lo vas a corregir, o comentá acá por qué no aplica."
    }
  ]
}
```

Notas sobre el `body` general (la parte fija que no cambia comentario a comentario):
- Empieza siempre con el disclaimer literal acordado (ver arriba), después el `@<author.login>` del paso 1.
- La sección **"Qué se revisó"** reemplaza a un simple conteo de hallazgos: **siempre** nombra qué se miró en cada categoría, tenga o no hallazgos, y por qué algo "no aplica" cuando corresponda (ej. RLS no aplica porque el PR no toca tablas). Un "sin hallazgos" sin decir qué se miró no es evidencia de nada — es la misma disciplina de "evidencia antes que afirmación" que rige el resto de este repo.
- **`event` es siempre `"COMMENT"`**, nunca `"APPROVE"` ni `"REQUEST_CHANGES"` — el agente opina, no aprueba ni bloquea el merge por su cuenta; esa palabra es de un humano.
- El marcador HTML del final (`<!-- code-reviewer-de-prs:sha:... -->`) es el que usa el paso 0 para avisar si un PR ya fue revisado en su último commit. Es invisible al leer la Review en GitHub.

Cada entrada de `comments[]` usa el `path` y el `line` **tal cual salieron del `[+N]`/`[ N]` del paso 1** (nunca un `[-old]`, esa línea no existe en la versión nueva) y `side: "RIGHT"` siempre — el agente comenta sobre el código resultante, no sobre lo que se borró.

**Publicar la Review:**

```bash
gh api --method POST repos/vaiven-austral/vaiven-app/pulls/<numero>/reviews --input /tmp/review-<numero>.json
```

## Lo que este agente no hace

- No corrige código ni abre PRs de fix, solo comenta.
- No decide si el ticket está "terminado" en general (eso es de un chequeo de Definition of Done; en este grupo lo hace g14-bot-review-vaivendev), evalúa criterios de aceptación puntuales, no el estado global del ticket.
- No reemplaza un escaneo determinista de secretos o dependencias vulnerables (ver "determinista antes que probabilístico" en `CLAUDE.md`); si hace falta, es un agente o script aparte.
- No decide por sí sola cuándo un PR es tan grande que no vale la pena revisarlo: siempre revisa, como mucho lo señala.
- No aprueba ni bloquea el merge — publica siempre con `event: "COMMENT"`, nunca `APPROVE` ni `REQUEST_CHANGES`. Esa palabra es de un humano.
- No audita la legitimidad de decisiones de proceso que el PR ya declara (ver "Regla de buena fe" en el paso 5) — solo comenta cuando el PR guarda silencio total sobre algo que el ticket exige justificar.
- No corre solo — hoy es 100% a pedido del QA. Automatizarlo (que se entere solo de un PR nuevo) es un paso futuro, pendiente de decidir de quién son las credenciales que usaría.

## Ejemplo de uso

**Pedido:** Revisá el PR #42 de vaiven-app.

**Resultado:** Identifica el ticket asociado, chequea sus criterios de aceptación y publica comentarios anclados a la línea real del diff, con `event: COMMENT`, señalando los hallazgos bloqueantes para decisión humana.
