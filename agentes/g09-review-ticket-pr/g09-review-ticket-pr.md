---
name: g09-review-ticket-pr
description: Revisar branches o PRs de Zervi contra tickets de Jira, especificaciones o criterios de aceptación y entregar hallazgos accionables en Markdown listo para GitHub. Usar para revisar implementación, contratos entre frontend React/TypeScript y backend Kotlin/Spring Boot, seguridad, persistencia, pruebas y compatibilidad entre branches.
tools: Read, Write, Edit, Grep, Glob, Bash, Skill
metadata:
  tipo: skill
  area:
  - frontend
  - backend
  - qa
  fase:
  - revision
  tecnologias:
  - typescript
  - react
  - kotlin
  - spring-boot
  - postgresql
  - flyway
  - auth0
  metodologia:
  - scrum
  herramientas:
  - codex
  requiere:
  - github
  - jira
  grupo: "09"
  autor:
    nombre: Máximo Sallemi
    github: MaximoSallemi
  responsables:
  - MaximoSallemi
  madurez: usado-en-proyecto
  relacionados:
  - g09-check-front-back-contract
  - g09-ticket-test-matrix
  - g09-fix-review-findings
  - g09-pre-pr-gate
  - g09-debug-local-integration
---
# Review Ticket PR

Revisar la implementación de la branch actual contra el ticket proporcionado y devolver únicamente problemas concretos, introducidos por la PR y suficientemente importantes para corregir.

## Insumos

Usar como fuente de verdad:

- El ticket, archivo adjunto o especificación entregada por el usuario.
- Las instrucciones `AGENTS.md` aplicables.
- El diff de la branch respecto de su branch base.
- Los contratos, modelos y migraciones compartidos entre frontend, backend y base de datos.
- Las pruebas existentes y los resultados verificables de CI o ejecución local.

## Revisión

- Leer primero el ticket y las reglas del repositorio.
- Comparar el diff completo contra la branch base correcta.
- Seguir los flujos de punta a punta, incluidos permisos, errores, estados vacíos y compatibilidad con branches dependientes.
- Verificar que los tests cubran el comportamiento observable y los límites relevantes.
- No reportar preferencias de estilo, problemas preexistentes ni riesgos puramente hipotéticos.
- Confirmar cada hallazgo con una ubicación concreta y explicar su impacto.

## Salida

Responder únicamente con hallazgos accionables en Markdown listo para pegar en GitHub, ordenados por severidad. Para cada hallazgo incluir:

- Título breve con prioridad.
- Archivo y línea aproximada.
- Problema e impacto real.
- Cambio esperado o escenario que debe quedar cubierto.

Si no hay problemas importantes, responder: `No encontré problemas accionables introducidos por esta PR.`

## Ejemplo de uso

**Pedido**

> Contrastá la PR de cancelación de turnos con su ticket de Jira. Revisá en particular qué ocurre si cancela otro usuario.

**Salida esperada**

Una revisión por criterio de aceptación, con hallazgos priorizados, referencias al código y pruebas faltantes.
