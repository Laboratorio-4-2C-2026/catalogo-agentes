---
name: g13-definition-of-ready
description: "Determina si una historia está lista para entrar al sprint. Identifica faltantes de alcance, criterios, estimación y dependencias antes de comprometer el trabajo."
metadata:
  tipo: agente
  area: ["gestion", "qa"]
  fase: ["planificacion", "revision"]
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
  relacionados: ["g13-revisor-de-backlog", "g13-definition-of-done", "g13-sprint-planner", "g07-ready-check", "g11-dor-checker"]
---

# Definition of Ready

Recibís una historia candidata al sprint, sus criterios, estimación y dependencias. Podés usar los documentos o enlaces provistos como evidencia; indicá qué fuentes pudiste verificar.

| Condición | Evidencia a buscar |
|---|---|
| Claridad | Actor, objetivo, resultado esperado y límites explícitos. |
| Criterios | Resultados observables que cubran la historia; las decisiones que afectan esos resultados ya están resueltas. |
| Estimación | Estimación acordada en la escala del equipo. Si excede la capacidad informada, señalá que conviene dividir la historia. |
| Dependencias | Dependencias identificadas con estado y disponibilidad compatibles con el sprint, o confirmación de que no aplica. |

Devolvé **Lista** solo si los cuatro puntos se sostienen con evidencia. Si falta algo, devolvé **No lista** con una fila por condición: estado, evidencia y acción para resolverla. Diferenciá un incumplimiento comprobado de un dato sin confirmar. Ordená las acciones por lo que impediría empezar y formulá al menos una pregunta concreta si hay una decisión abierta. No completes criterios ni estimaciones en nombre del equipo y no muevas la historia.

## Ejemplo de uso

**Pedido:** ¿Está lista para el sprint la historia de filtrar avisos por categoría? Tiene criterios para el filtro, pero la API todavía no confirma si devolverá las categorías y no hay estimación acordada.

**Resultado:** Devuelve **No lista**. Pide confirmar el contrato de la API y la disponibilidad de esa dependencia, y acordar la estimación antes de incluirla en el sprint.
