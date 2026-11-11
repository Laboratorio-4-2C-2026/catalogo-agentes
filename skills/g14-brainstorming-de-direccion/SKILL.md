---
name: g14-brainstorming-de-direccion
description: Convierte una idea de dirección (decisión, cambio de alcance, agente o automatización) en una propuesta con opciones y trade-offs que el equipo pueda evaluar, sin escribir código de producto. Adaptación de brainstorming de Superpowers para equipos de Dirección de Proyectos.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: experimental
  relacionados:
  - g08-plan-with-user-input
  - g14-planes-de-trabajo-de-direccion
---

# Diseñar antes de decidir

Convertí una idea de dirección en una propuesta que los cuatro puedan evaluar. Esta adaptación conserva la intención de brainstorming de Superpowers, pero respeta que este repositorio dirige el producto: no escribe su código.

1. Consultá primero el grafo de conocimiento del repo (graphify) si existe; si no hay grafo, usá el índice de documentos. Leé sólo las fuentes que la propuesta toque. Revisá `docs/bitacora/` si el cambio se parece a un problema ya resuelto.
2. Separá hecho verificado, supuesto y pregunta abierta. No escondas una decisión material dentro de una mejora técnica.
3. Para una decisión con alternativas reales, presentá opciones breves con trade-offs y una recomendación. Si toca alcance, fechas, KPI, arquitectura sin spike o la prohibición de escribir código de producto, frená antes de resolverla: es decisión humana.
4. Cuando haya acuerdo, dejá la decisión durable donde corresponde: ADR y propagación al charter; estado y próximo paso en `docs/PLANNING-STATE.md`; aprendizaje operativo en bitácora.

La salida buscada es una decisión o propuesta verificable, no un documento largo ni una implementación de producto.

## Ejemplo de uso

**Pedido:** Quiero proponer un agente que audite los PRs automáticamente, ayudame a pensarlo.

**Resultado:** Hace preguntas para acotar la idea y devuelve una propuesta con alternativas, trade-offs y lo que queda a decisión humana.
