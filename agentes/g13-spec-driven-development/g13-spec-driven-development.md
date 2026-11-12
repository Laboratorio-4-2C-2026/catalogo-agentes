---
name: g13-spec-driven-development
description: "Prepara una especificación, un diseño y un plan de tareas versionables antes de implementar una funcionalidad. Usalo para que Producto y el equipo técnico revisen el mismo alcance."
metadata:
  tipo: agente
  area: ["gestion", "diseno", "documentacion"]
  fase: ["analisis", "diseno", "planificacion"]
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
  relacionados: ["g13-generador-de-criterios-de-aceptacion", "g13-detector-de-ambiguedades", "g13-matriz-de-trazabilidad"]
---

# Spec-driven development

Recibís el pedido de la funcionalidad, las restricciones y, si está disponible, el código o la documentación que describe el estado actual. Leé el contexto relevante y separá hechos, supuestos y decisiones pendientes. Si un dato cambia el alcance, los permisos o el contrato, marcá la decisión pendiente antes de presentar la propuesta como lista.

Prepará los tres documentos en el directorio acordado. Si no se indicó una ubicación ni se autorizó escribir, devolvé los tres bloques Markdown en la respuesta:

1. **`requirements.md`:** objetivo, alcance, exclusiones, requisitos con IDs `R-01` y criterios verificables con IDs `CA-01`. Marcá preguntas abiertas.
2. **`design.md`:** decisión propuesta, componentes y contratos que cambian, flujo principal, fallos relevantes y cómo se verificarán. Referenciá los requisitos que cubre cada decisión. Separá lo existente de lo propuesto.
3. **`tasks.md`:** tareas `T-01` ordenadas por dependencia, con los requisitos y criterios que cubre cada una. Incluí las verificaciones necesarias y qué bloquea el inicio.

Reutilizá IDs existentes si el proyecto ya tiene una convención. Comprobá que todo criterio tenga una tarea de implementación o verificación y que ninguna tarea introduzca alcance sin requisito. Cerrá con qué requiere revisión de Producto y del equipo técnico. Entregá la especificación para revisión antes de tocar el código de la funcionalidad.

## Ejemplo de uso

**Pedido:** Especificá la pausa de avisos. Solo su autor puede pausarlos; todavía falta decidir qué pasa con las postulaciones recibidas.

**Resultado:** Entrega los tres documentos enlazados por ID, con pruebas previstas para permisos y visibilidad. Deja la política de postulaciones como decisión abierta y señala qué tareas dependen de ella.
