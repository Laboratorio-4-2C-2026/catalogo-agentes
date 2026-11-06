---
name: g02-pr-review-format
description: 'Formato fijo para publicar en un PR de Zest el resultado de una revisión automática: tabla de checks, hallazgos por severidad y pendientes. Usar al comentar revisiones de agentes.'
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Liz Lubelcyk
    github: lizlubelczyk
  responsables:
  - lizlubelczyk
  madurez: usado-en-proyecto
  relacionados:
  - g02-pr-reviewer
---
# Structure

One comment per run. Never several separate comments.

## 🤖 Automated review — <agent name>

**Summary:** <one line. What happened, and whether anything blocks the merge.>

### Checks

| Check | Result | Detail |
|---|---|---|
| Lint | ✅ / ⚠️ / ❌ | <errors and warnings, or "no issues"> |
| Build | ✅ / ❌ | <error message if it failed> |
| Health check | ✅ / ❌ | <status code> |
| Tests | ✅ / ❌ | <passing/failing counts> |
| Coverage | ✅ / ❌ | <percentage — minimum is 75%> |

Include only the rows for checks you actually ran.

### Findings

Ordered by severity. Omit any category with nothing in it.

#### 🔴 Blocking
Breaks functionality, fails an acceptance criterion, or drops coverage
below 75%.

#### 🟡 Important
Edge-case bugs, tests that don't actually assert anything, patterns that
depart from what the repo already does.

#### 🔵 Minor
Naming, formatting, style details.

Two or three lines per finding, maximum:
- what's wrong
- where: `file.ts:line`
- which acceptance criterion or convention it breaks

### Unresolved

Acceptance criteria too vague to verify, pending architectural decisions,
elements with no `data-testid`. List them without inventing an answer.

---
_First automated pass. Ine reviews after this._

# Rules

- Don't approve, don't reject, don't request changes. Comment only.
- No filler: if there are no findings, say so in one line.
- Don't praise the code. The comment exists to flag problems.
- Address the PR author in second person, respectfully. This is a
  teammate's work, not an audit subject.
- If you couldn't complete a check, say you didn't run it. Never report ✅
  for something you didn't execute.

## Ejemplo de uso
**Pedido:** Publicá el resultado de la revisión del PR 42 con el formato del equipo.
**Resultado:** Arma un único comentario con resumen, tabla de checks ejecutados, hallazgos ordenados por severidad y criterios sin resolver.
