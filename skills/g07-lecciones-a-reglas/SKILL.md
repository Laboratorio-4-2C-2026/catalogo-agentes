---
name: g07-lecciones-a-reglas
description: "Al cerrar un sprint de Study Arena, busca en Jira y GitHub los errores que se repitieron (bugs reabiertos, comentarios de review que aparecen en varios PRs, criterios de aceptación que fallaron en QA, CI roto) y los convierte en reglas accionables para que no vuelvan a pasar: líneas para CLAUDE.md o las convenciones del repo, items del checklist de PR o de la Definition of Ready, reglas de lint o tests de arquitectura. Usar al cerrar un sprint o cuando el equipo siente que comete siempre los mismos errores; no hace la retro ni señala personas."
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  - documentacion
  fase:
  - revision
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
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-sprint-retro
  - g07-code-review-tl
  - g07-ready-check
---

# De lecciones a reglas

Las retros terminan con "hay que acordarse de paginar los listados" y al sprint siguiente el mismo comentario aparece en otro PR. Las lecciones que dependen de la memoria se pierden; las que se convierten en **una regla en un lugar que se revisa solo** (un lint, un test, una línea en `CLAUDE.md` que la IA lee siempre, un item del template de PR) se mantienen.

Esta skill no hace la retro (para eso está `g07-sprint-retro`). Toma la evidencia de errores **repetidos** y la convierte en reglas concretas, cada una puesta en el lugar donde mejor se hace cumplir.

## Cuándo usar esta skill

"¿Qué errores repetimos?", "convertí las lecciones en reglas", "actualizá el CLAUDE.md con lo que aprendimos", "siempre nos marcan lo mismo en los PRs", al cerrar un sprint o una entrega.

## Paso 1: juntar la evidencia del período

Por defecto, el último sprint cerrado (o el período que diga el usuario).

1. **Comentarios de review en GitHub**: `gh pr list --state merged --search "merged:>=<fecha>" --json number,title` y, para cada PR, `gh api repos/{owner}/{repo}/pulls/<n>/comments` (comentarios en línea) y `gh pr view <n> --json reviews` (reviews con cambios pedidos). Es la fuente más rica.
2. **Jira** (tools MCP que terminen en `searchJiraIssuesUsingJql` y `getJiraIssue`):
   - bugs creados en el período y en qué ticket se originaron;
   - tickets **reabiertos** (volvieron de In Review o Done a In Progress) y su comentario de por qué;
   - comentarios de QA con criterios de aceptación que fallaron.
3. **CI**: `gh run list --status failure --created ">=<fecha>"` y el motivo del fallo (lint, tests, build) de cada uno.
4. **Las reglas que ya existen**: `CLAUDE.md`, `AGENTS.md`, `docs/guidelines*`, `CONTRIBUTING.md`, `.github/pull_request_template.md`, la configuración de lint (`eslint.config.*`, Checkstyle o Spotless en Gradle), los tests de arquitectura (ArchUnit) y la Definition of Ready o Done del equipo. Sirve para no duplicar y para detectar reglas que **existen pero no se cumplen**.

## Paso 2: agrupar en patrones

Agrupá la evidencia por **causa**, no por síntoma. Por ejemplo, "faltó validar el DTO", "el endpoint aceptó null" y "500 en lugar de 400" pueden ser el mismo patrón: falta de validación con `@Valid` en los controllers.

Un patrón entra si tiene **al menos 2 ocurrencias** en PRs, tickets o personas distintas, o 1 ocurrencia grave (un bug en una demo o un dato perdido). Lo que pasó una sola vez y es menor va a "observaciones", no a reglas.

Para cada patrón: un nombre corto, las ocurrencias con su link (PR #, comentario o ticket) y el costo estimado (retrabajo, reapertura, bug en demo).

## Paso 3: convertir cada patrón en una regla

Una regla tiene que ser **verificable**: alguien (o algo) puede decir sí o no. "Tener cuidado con los null" no es una regla. "Todo `@RequestBody` lleva `@Valid` y el DTO tiene constraints de Bean Validation" sí lo es.

Elegí el lugar más **automático** posible, en este orden de preferencia:

1. **Test o lint** que falla solo: una regla de ESLint, Checkstyle, un test de ArchUnit (por ejemplo, "los controllers no acceden a repositories") o un check en el CI.
2. **`CLAUDE.md` / `AGENTS.md`**: para lo que la IA del equipo tiene que aplicar siempre al escribir código. Corto, imperativo y con el porqué en media línea.
3. **Template de PR**: un item del checklist que el autor marca.
4. **Definition of Ready o de Done**: si el problema nace en cómo se escriben los tickets (por ejemplo, tickets FE sin contrato BE).
5. **Convenciones del repo** (`docs/guidelines`): para lo que necesita explicación o ejemplos.

Para cada regla, escribí **el texto exacto listo para pegar** en su destino (la línea de `CLAUDE.md`, el item del template, la configuración del lint o el esqueleto del test).

Si el patrón es una regla que **ya existe y no se cumple**, no la dupliques: proponé moverla a un lugar más automático o hacerla más concreta.

## Paso 4: priorizar

No más de **5 reglas nuevas por sprint**: un equipo no adopta 15 reglas de golpe. Ordená por (ocurrencias × costo) ÷ esfuerzo de implementarla. El resto queda como "candidatas" para el próximo sprint.

## Output

1. Período analizado y fuentes (cuántos PRs, comentarios, tickets y corridas de CI).
2. **Patrones encontrados**, ordenados por impacto: nombre, ocurrencias con links y costo.
3. **Reglas propuestas (máximo 5)**: el patrón que la origina, el destino, el texto exacto o el diff y cómo se va a verificar que se cumple.
4. **Reglas existentes que no se cumplen**, con la propuesta para endurecerlas.
5. Candidatas para más adelante y observaciones sueltas.

Ver `example-output.md` para una corrida real sobre Study Arena.

Con un "sí" del usuario, aplicá los cambios a los archivos del repo (`CLAUDE.md`, template de PR, guidelines) en una rama nueva, **sin commitear**, para que el equipo los revise. Los cambios de lint, CI o tests se proponen y se aplican solo si el usuario lo pide explícitamente.

## Qué no hacer

- No señales personas: los patrones son del equipo. No muestres quién cometió cada error, solo el PR o ticket.
- No conviertas en regla algo que pasó una vez y es menor.
- No escribas en Jira ni comentes en GitHub.
- No reemplaces la retro: si el usuario quiere la retro completa, sugerí `g07-sprint-retro`.

## Ejemplo de uso

**Pedido:** Cerramos el sprint 4. Fijate qué errores repetimos y convertilos en reglas.

**Resultado:** Lee los comentarios de review de los 14 PRs mergeados, los tickets reabiertos y los fallos de CI. Encuentra tres patrones: endpoints sin `@Valid` (5 PRs), listados sin paginar (3 PRs y un bug en la demo) y tickets FE sin contrato que se reabrieron. Propone una línea para `CLAUDE.md`, un test ArchUnit, un item del template de PR y un ajuste a la Definition of Ready, con el texto listo para pegar.
