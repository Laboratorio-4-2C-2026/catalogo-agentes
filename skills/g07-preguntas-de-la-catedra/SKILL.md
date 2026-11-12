---
name: g07-preguntas-de-la-catedra
description: "Prepara al equipo de Study Arena para una entrega, un steering o una defensa generando las preguntas más incómodas que haría la cátedra a partir de la consigna o rúbrica, la presentación, Jira y el repo, cada una con la evidencia disponible, una respuesta sugerida y una marca de qué tan bien parado está el equipo. Usar los días previos a una presentación; no arma la presentación ni el guion de demo."
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  - planificacion
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
  - g07-explicar-mi-pr
  - g07-sprint-status-report
  - g07-weekly-process-checklist
---

# Preguntas de la cátedra

Lo que más complica una presentación no es la demo que falla, sino la pregunta para la que nadie tiene una respuesta con datos: "¿Por qué este KPI y no otro?", "¿Qué hicieron con el riesgo que plantearon hace tres semanas?" o "¿Cuánto de lo planificado entregaron?".

Esta skill actúa como un profesor exigente **antes** de que llegue el profesor de verdad: encuentra los puntos débiles del proyecto, arma las preguntas que los exponen y busca la evidencia para responderlas. Si no hay evidencia, lo dice, y queda tiempo para conseguirla.

## Cuándo usar esta skill

"¿Qué nos pueden preguntar?", "preparanos para el steering", "simulá la defensa", "¿dónde estamos flojos?", y los días previos a una entrega, un steering o una defensa.

## Paso 1: juntar el material

Pedí o buscá, en este orden (lo que falte, se marca como limitación):

1. **Consigna o rúbrica** de la instancia (PDF, doc o texto pegado). Es lo más importante: las preguntas de la cátedra salen de lo que la cátedra pidió. Si hay criterios de evaluación, cada uno tiene que generar al menos una pregunta.
2. **La presentación o el documento** que el equipo va a mostrar (deck de steering, informe).
3. **Jira** (tools MCP que terminen en `searchJiraIssuesUsingJql` y `getJiraIssue`): lo planificado contra lo entregado en el período, tickets arrastrados, bloqueos, épicas.
4. **Repo**: actividad (`git log --since`), PRs (`gh pr list --state all --search "created:>=<fecha>"`), tests y CI.
5. **Documentos de proceso** del equipo, si existen: riesgos, decisiones, KPIs y el checklist semanal (`g07-weekly-process-checklist`).
6. **Lo que dijo la cátedra la vez anterior**: preguntale al usuario si hubo devoluciones de la entrega pasada. Lo que se marcó y no se arregló es la pregunta más probable.

## Paso 2: buscar los puntos débiles

Revisá en el material:
- **Coherencia entre lo que se dice y lo que muestran los datos**: el deck dice "avance 80%" pero en Jira está Done el 55% de lo comprometido.
- **Promesas anteriores**: riesgos, compromisos o acciones de la presentación pasada sin seguimiento visible.
- **KPIs**: cada KPI tiene definición, fórmula, fuente, valor actual y meta. ¿Mide algo útil o es fácil de inflar? ¿Por qué ese y no otro?
- **Alcance**: qué se cayó, qué se agregó y si quedó registrado como decisión.
- **Calidad**: cobertura de tests, bugs abiertos, si el CI pasa y si hay PRs mergeados sin review.
- **Producto**: el valor para el usuario, a quién le sirve, si hubo validación con usuarios reales y por qué esta funcionalidad primero.
- **Equipo**: reparto de trabajo (commits, tickets por persona), roles y cómo se toman las decisiones. Mostralo de forma **agregada**, sin señalar personas.
- **Técnicas**: decisiones de arquitectura que alguien podría cuestionar (por qué Spring Boot, cómo escala el ranking, seguridad de la API).

## Paso 3: escribir las preguntas

Entre 10 y 15 preguntas, ordenadas de **más a menos probable × incómoda**. Para cada una:

```
### N. <La pregunta, tal como la haría un profesor>
- **Por qué la harían:** <qué del material la dispara>
- **Evidencia que tenemos:** <dato concreto con su fuente: ticket, PR, gráfico, slide>  — o "ninguna"
- **Respuesta sugerida:** <3–5 oraciones, en primera persona del plural, honesta>
- **Estado:** 🟢 respondemos con datos · 🟡 respondemos pero flojo · 🔴 no tenemos respuesta
- **Para mejorarla:** <acción concreta y chica, con quién y antes de cuándo>  (solo si es 🟡 o 🔴)
```

Reglas para las respuestas:
- Si la evidencia muestra un problema, la respuesta **lo reconoce** y dice qué se hizo o qué se va a hacer. Nunca sugieras esquivar la pregunta ni maquillar números.
- Usá números del material, no inventados. Si falta un número, la respuesta lo dice y la acción es conseguirlo.

## Paso 4: simulacro (opcional)

Si el usuario quiere practicar, ofrecé un **modo simulacro**: hacé las preguntas de a una sin mostrar la respuesta sugerida, esperá la respuesta del usuario y devolvé una devolución breve (qué estuvo bien, qué dato faltó y cómo cerrarla mejor). Después pasá a la siguiente.

## Output

1. Una línea con qué material se usó y qué faltó.
2. **Semáforo general**: N 🟢 · M 🟡 · K 🔴.
3. **Las 3 acciones más importantes antes de la presentación**, sacadas de los 🔴.
4. Las preguntas, en el formato del paso 3.

## Qué no hacer

- No señales personas ("Fulano hizo poco"). Si el reparto es desparejo, la pregunta es sobre cómo se organiza el equipo.
- No inventes devoluciones de la cátedra ni criterios de evaluación que no estén en la consigna.
- No modifiques la presentación ni Jira.

## Ejemplo de uso

**Pedido:** El jueves es el steering 2. Te paso la consigna y el deck: ¿qué nos van a preguntar?

**Resultado:** Cruza la consigna, el deck, Jira y GitHub y devuelve 12 preguntas con su evidencia, una respuesta sugerida y el semáforo. Por ejemplo, marca 🔴 que el deck dice 80% de avance pero hay 55% Done en Jira, y propone las tres acciones más urgentes. Si el usuario quiere, después ofrece un simulacro pregunta por pregunta.
