---
name: g14-planes-de-trabajo-de-direccion
description: "Descompone entregables del equipo de dirección (tickets, QA, documentación, automatización permitida) en un plan ejecutable antes de editar, que termina en especificación y criterios de aceptación. No distribuye capacidad ni tickets de desarrollo por semana, ni escribe código de producto."
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
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
  - g14-planificador-de-semana
  - g10-sprint-planner
  - g08-plan-with-user-input
---

# Planificar trabajo de dirección

Armá un plan ejecutable para el equipo de dirección o para los agentes autorizados. La planificación de producto termina en una especificación para los devs, criterios de aceptación y evidencia; no incluye código de implementación.

## Antes de descomponer

- Ubicá precedentes y dependencias con el grafo de conocimiento del repo (graphify) o, si no hay grafo, con el índice de documentos; después leé los documentos mínimos.
- Definí el resultado, destinatario, dueño, fecha o hito, dependencias y evidencia observable.
- Si es un ticket para Jira, respetá las seis secciones obligatorias del estándar del proyecto. Cada criterio de aceptación debe expresar una sola aserción comprobable.

## Plan mínimo útil

Dividí por entregables revisables, no por actividad genérica. Para cada uno indicá qué fuente cambia, qué no entra en alcance, cómo se verifica y quién debe decidir si aparece una excepción. Evitá tareas que presupongan acceso, credenciales o cambios en servicios externos sin autorización explícita.

Si el plan descubre un cambio durable de arquitectura o alcance, no lo escondas en el ticket: elevá una propuesta de ADR o charter antes de continuar.

## Ejemplo de uso

**Pedido:** Planificá la preparación de la demo del hito final.

**Resultado:** Devuelve un plan por pasos con entregables, responsables y la evidencia que cierra cada paso.
