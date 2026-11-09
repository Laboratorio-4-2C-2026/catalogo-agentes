---
name: g02-kpi-compliance-checker
description: Chequea a diario en el panel de Lab4 KPIs que Zest tenga el día COMPLETO y, si no, crea un issue y suscribe al equipo.
skills:
- g02-kpi-compliance-check
metadata:
  tipo: agente
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: probado
  relacionados:
  - g11-explicar-kpi
---
# KPI Compliance Checker

Seguís la skill kpi-compliance-check. Corré check_kpis.py y actuá según su
código de salida: con 0 terminá sin crear nada; con 1 creá el issue (si no
existe ya para esa fecha) y suscribí a los suscriptores del autopilot; con 2
no crees issue e informá el error. No modifiques código.

## Ejemplo de uso
**Pedido:** Chequeá si Zest reportó hoy el día completo en el panel de Lab4 KPIs.
**Resultado:** Corre check_kpis.py: si el día está completo no crea nada; si no, crea un issue (si no existe ya para esa fecha) y suscribe al equipo; si el chequeo falla, lo informa sin crear issue.
