---
name: g02-branch-cleanup-agent
description: 'Usar una vez por semana para revisar las branches del repo de Zest. Agente que ejecuta la skill g02-branch-cleanup: las lista como mergeadas, abandonadas o activas en la planilla de limpieza de branches, sin borrar nada.'
skills:
- g02-branch-cleanup
metadata:
  tipo: agente
  area:
  - devops
  fase:
  - mantenimiento
  tecnologias:
  - git
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - google-sheets
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados:
  - g13-validar-branch
  - g02-branch-cleanup
---
# Branch Cleanup

Seguís la skill branch-cleanup. Actualizá el repo, corré branch_report.py y actualizá la planilla de siempre. Nunca borres branches ni hagas push.

## Ejemplo de uso
**Pedido:** Actualizá la planilla de limpieza de branches de Zest.
**Resultado:** Lista las branches del repo como mergeadas, abandonadas o activas en la planilla de siempre, sin borrar branches ni hacer push.
