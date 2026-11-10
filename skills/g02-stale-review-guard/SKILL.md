---
name: g02-stale-review-guard
description: Detecta si la rama de una PR de Zest quedó atrás de dev y contrasta cada hallazgo de una revisión contra el código actual, descartando los que ya no aplican. Usar después de una revisión automática y antes de publicarla.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Luz Laura
    github: luzlaura
  responsables:
  - luzlaura
  madurez: experimental
  relacionados:
  - g02-bug-origin-check
  - g02-stacked-pr-guard
---
# Stale Review Guard

Una revisión automática lee la rama tal como está. Si la rama quedó atrás de `dev`, puede afirmar cosas falsas. En la PR 54 dijo que el front no mandaba `coverImageUrl`, y en dev sí lo mandaba.

## Pasos

1. Corré `git fetch origin` y obtené la base real de la PR con `gh pr view N --json baseRefName,headRefName`.
2. Medí el atraso: `git rev-list --count origin/<rama>..origin/<base>`.
3. Si el atraso es 0, avisá que la revisión está al día y terminá.
4. Listá qué cambió en la base desde que salió la rama: `git diff --name-only <merge-base> origin/<base>`.
5. Simulá el resultado del merge sin tocar nada: `git merge-tree --write-tree --name-only origin/<base> origin/<rama>`. Anotá si hay conflictos.
6. Para cada hallazgo de la revisión:
   - Si sus archivos no aparecen en el paso 4, sigue vigente salvo que dependa de otro archivo que sí cambió.
   - Si aparecen, leé la versión actual con `git show origin/<base>:<archivo>` y volvé a evaluarlo.

## Resultado

| Hallazgo | Archivos cambiados en la base | Estado | Evidencia |
|---|---|---|---|
| ... | Sí o No | Sigue vigente, Ya no aplica o Revisar a mano | Archivo y línea en la base |

Terminá indicando cuántos commits de atraso hay y si conviene pedirle al autor que actualice la rama antes de seguir revisando.

## Reglas

- No hagas rebase, merge ni push.
- Si dudás, usá "Revisar a mano": no descartes un hallazgo sin evidencia.

## Ejemplo de uso
**Pedido:** Tengo estos 4 hallazgos del code review de la PR 72, ¿siguen valiendo?
**Resultado:** Informa cuántos commits está atrás la rama y devuelve una tabla que marca cada hallazgo como vigente, ya no aplica o a revisar, con evidencia.
