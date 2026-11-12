---
name: g07-explicar-mi-pr
description: "Convierte un PR propio de GitHub (diff, commits y ticket STUDY de Jira) en un guion para contarlo en voz alta: versión de 60 segundos para el standup, versión de 3 minutos para la clase o el steering, cómo probarlo en vivo y las preguntas que probablemente te hagan con su respuesta. Usar antes de un standup, una demo o una corrección en clase; no revisa la calidad del código ni comenta en GitHub."
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - revision
  - desarrollo
  tecnologias:
  - agnostico
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - jira
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-preguntas-de-la-catedra
  - g07-code-review-tl
  - g07-release-notes
---

# Explicar mi PR

Hiciste el PR, funciona, pero en el standup o en clase te piden "contá qué hiciste" y terminás leyendo nombres de archivos. Esta skill arma lo que tenés que **decir**: qué problema resolviste, qué decisión tomaste y por qué, y cómo se ve funcionando.

No es un code review: no juzga el código. Lo explica desde el punto de vista de quien lo escribió.

## Cuándo usar esta skill

"Explicame mi PR", "qué digo en el standup", "tengo que mostrar esto en clase", "armame el guion del PR #N", "no sé cómo contar lo que hice".

## Paso 1: juntar el material

1. **PR**: si te dan un número o una URL, `gh pr view <n> --json title,body,headRefName,baseRefName,commits,files,additions,deletions,url` y `gh pr diff <n>`. Si no hay PR todavía, usá la rama actual: `git log --oneline <base>..HEAD` y `git diff <base>...HEAD`.
2. **Ticket**: buscá la key `STUDY-<n>` en el título, la rama o los commits y traela de Jira (tool MCP que termine en `getJiraIssue`): objetivo y criterios de aceptación. Si no hay Jira, pedí que peguen el ticket o seguí sin él y avisá.
3. **Contexto del autor**: preguntá en una sola línea, y solo si no se deduce del diff: "¿Hubo algo que te costó o que decidiste distinto de lo obvio?". Esa respuesta suele ser lo más interesante para contar.

## Paso 2: entender el cambio

Armá internamente (no se lo muestres al usuario tal cual):
- **El antes y el después**, en términos de lo que ve o puede hacer un usuario (o, si el cambio es interno, lo que ahora es posible o más seguro).
- **Capas que toca**: migración, entidad, service, controller, front (página, hook, componente), tests.
- **La decisión principal**: la elección no obvia (por ejemplo, calcular los puntos en el back y no en el front, paginar, usar un enum, agregar un índice).
- **Qué quedó afuera** del alcance y por qué.
- **Riesgos**: lo que podría romper o lo que no se testeó.

Separá el ruido: formateo, renombres masivos y archivos generados no se cuentan.

## Paso 3: escribir el guion

Escribilo **para hablar**, no para leer: frases cortas, en primera persona, sin nombres de clases salvo que sean la clave. Español rioplatense y natural.

### 🎤 Versión standup (≈60 segundos, 100–140 palabras)
1. Qué ticket y qué cambia para el usuario (1 oración).
2. Cómo lo resolví, en una idea (1–2 oraciones).
3. Estado: listo para review, falta X o estoy bloqueado por Y.

### 🧑‍🏫 Versión clase o steering (≈3 minutos)
1. **Problema**: por qué importaba.
2. **Solución**: el recorrido por capas, de afuera hacia adentro (lo que ve el usuario → API → lógica → datos).
3. **La decisión**: qué alternativa había y por qué elegiste esta.
4. **Cómo sé que anda**: tests y criterios de aceptación cubiertos.
5. **Qué sigue** o qué quedó afuera.

### 🖥️ Demo en vivo
- Pasos exactos para mostrarlo (URL local, usuario de prueba, qué clic hacer), sacados del ticket y del diff.
- Si hay API, un `curl` listo para pegar.
- Un **plan B** si la demo falla (por ejemplo, mostrar el test que pasa o una captura).

### ❓ Preguntas probables
Entre 4 y 6 preguntas que haría un profesor o un compañero mirando este diff, con una respuesta corta y honesta para cada una. Priorizá:
- "¿Por qué así y no de esta otra forma?" sobre la decisión principal.
- "¿Qué pasa si…?" sobre casos borde que el diff no cubre.
- "¿Cómo lo testeaste?"
- Si hay algo débil (por ejemplo, un caso sin test), incluí la pregunta igual y una respuesta que lo admita y diga qué harías.

## Output

Ver `example-output.md` para una corrida real sobre Study Arena.

Las cuatro secciones de arriba, en ese orden, más una línea con el link al PR y al ticket. Nada más: ni resumen de archivos ni estadísticas de líneas.

## Qué no hacer

- No inventes motivos de decisiones: si no surgen del diff, del ticket o de lo que dijo el usuario, presentalos como pregunta ("¿Lo hiciste así por X?").
- No exageres lo que hace el PR ni digas que cubre criterios que el diff no cubre.
- No comentes en GitHub ni en Jira.

## Ejemplo de uso

**Pedido:** En el steering me pueden preguntar por el envío de KPIs. Explicame el PR #69 para poder contarlo.

**Resultado:** Lee el diff del PR #69 y el ticket STUDY-85, y devuelve un guion de standup de 60 segundos, uno de 3 minutos con la decisión de mandar siempre los 10 KPIs (0 si no hay dato, el último valor si hubo error), los pasos para mostrarlo con el endpoint manual, un plan B y seis preguntas probables con su respuesta.
