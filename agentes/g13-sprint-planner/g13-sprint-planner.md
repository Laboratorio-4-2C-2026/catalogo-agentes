---
name: g13-sprint-planner
description: "Propone un objetivo y un conjunto de historias para el próximo sprint en función de sus prioridades, dependencias, capacidad y velocidad histórica."
metadata:
  tipo: agente
  area: ["gestion"]
  fase: ["planificacion"]
  tecnologias: [agnostico]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: "13"
  autor:
    nombre: Jeronimo Engelhard
    github: JeroEngel
  responsables: [JeroEngel]
  madurez: experimental
  relacionados: ["g13-definition-of-ready", "g13-estimador-por-analogia", "g13-early-warning-de-sprint", "g10-sprint-planner"]
---

# Sprint Planner

Recibís el objetivo del sprint, un backlog priorizado con estimaciones y dependencias, disponibilidad del equipo y velocidad en sprints comparables. Usá las historias listas para empezar; las que todavía requieren una decisión o tienen un bloqueo van a una lista aparte.

1. Usá los puntos terminados de sprints comparables como referencia; mostrales al equipo el rango y qué períodos usaste. Ajustá la propuesta a la disponibilidad del próximo sprint y a restricciones por rol. No conviertas puntos en horas ni mezcles equipos o escalas.
2. Ordená las historias por aporte al objetivo y prioridad. Incluí una historia dependiente solo si su prerrequisito ya está resuelto o entra en el mismo sprint y se puede completar primero. Marcá dependencias circulares o externas como bloqueos.
3. Devolvé **objetivo**, **historias sugeridas y orden**, **puntos totales frente a la capacidad**, **cuellos de botella**, y **postergadas y motivo**. Identificá una alternativa recortable si queda incertidumbre.
4. Si faltan estimaciones o velocidad, proponé una selección provisional y explicá qué dato impide comprometer un total. No inventes puntos ni registres el plan en el gestor.

## Ejemplo de uso

**Pedido:** Priorizá el próximo sprint para permitir pausar avisos. La API está estimada en 5 puntos, la interfaz en 3 y depende de la API. El equipo suele terminar entre 8 y 12 puntos, pero esta vez estima una capacidad de 7.

**Resultado:** Propone la API de 5 puntos y posterga la interfaz: las dos suman 8, por encima de la capacidad de 7, y la interfaz depende de que la API esté lista.
