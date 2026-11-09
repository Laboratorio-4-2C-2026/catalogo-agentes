---
name: g02-bug-origin-check
description: Determina si un bug encontrado al revisar una PR de Zest lo introdujo esa PR o ya existía en dev, comparando código e historial. Usar antes de pedirle a un autor que corrija algo en su PR.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  - testing
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
  - g02-stale-review-guard
---
# Bug Origin Check

Un bug visible durante la revisión de una PR no siempre es culpa de esa PR. Esta skill evita pedirle al autor algo que no le corresponde, y evita dejar pasar lo que sí rompió.

## Pasos

1. Anotá el síntoma, el archivo y las líneas sospechosas.
2. Actualizá las referencias con `git fetch origin` y buscá la base real de la PR: puede no ser `dev` si está apilada.
3. Calculá el punto de partida: `git merge-base origin/<base> origin/<rama>`.
4. Mirá si la PR tocó ese código: `git diff <merge-base>...origin/<rama> -- <archivo>`.
5. Mirá si el mismo patrón existe en dev: `git show origin/dev:<archivo>`. Buscá también el patrón en otros archivos, porque puede estar copiado.
6. Si el patrón existe, rastreá cuándo entró con `git log -S'<texto>' --oneline origin/dev -- <archivo>`.
7. Si el código no alcanza para decidir, reproducí el bug en dev y en la rama usando `g02-pr-sandbox`.

## Veredicto

Usá exactamente uno:

| Veredicto | Qué significa | Qué hacer |
|---|---|---|
| **Lo introdujo la PR** | El código nuevo lo causa y dev no lo tiene | Pedir la corrección en la review |
| **Lo empeoró la PR** | Ya existía, pero ahora afecta más casos | Pedir la corrección de lo agravado |
| **Ya estaba en dev** | La PR no lo toca o solo lo hereda | No bloquear; proponer ticket aparte |
| **No se puede determinar** | Falta reproducir o falta información | Decir qué falta |

Mostrá la evidencia: archivo, línea y commit. Si no reprodujiste el bug, decilo.

## Reglas

- No modifiques ramas ni hagas commits.
- No crees tickets ni publiques comentarios sin OK explícito.

## Ejemplo de uso
**Pedido:** En la PR 79 la búsqueda ignora mayúsculas pero no los acentos, ¿es de esta PR?
**Resultado:** Compara el diff con el código de dev, indica el commit donde apareció el patrón y da un veredicto con la acción a seguir.
