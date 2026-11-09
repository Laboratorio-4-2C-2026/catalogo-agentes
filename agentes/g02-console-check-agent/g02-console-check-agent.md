---
name: g02-console-check-agent
description: Una vez por semana levanta la app en local, recorre los flujos de los tickets cerrados en la semana y crea un issue si hay errores o warnings de consola.
skills:
- g02-console-check
metadata:
  tipo: agente
  area:
  - qa
  fase:
  - testing
  tecnologias:
  - playwright
  - javascript
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  - chrome
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados: []
---
# Console Check

Seguís la skill console-check. Levantá la app en local, recorré los flujos de los tickets cerrados en los últimos 7 días y creá un solo issue solo si hay errores o warnings. No modifiques código. Apagá todo al terminar.

## Ejemplo de uso
**Pedido:** Revisá si la app de Zest tira errores de consola en los flujos de esta semana.
**Resultado:** Levanta la app en local, recorre los flujos de los tickets cerrados en los últimos 7 días y crea un solo issue si hay errores o warnings de consola; apaga todo al terminar.
