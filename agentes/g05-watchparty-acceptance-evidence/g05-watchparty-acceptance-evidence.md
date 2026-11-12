---
name: g05-watchparty-acceptance-evidence
description: "Contrasta los criterios de aceptación de los tickets de una versión de WatchParty con evidencia de la candidata desplegada. Usar cuando haya que cerrar la validación de QA de una release."
metadata:
  tipo: agente
  area: ["qa","gestion"]
  fase: ["revision","testing"]
  tecnologias: ["agnostico"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g15-regression-matrix-keeper", "g15-release-criteria-evidence-checker","g05-watchparty-qa-test-designer","g05-watchparty-release-readiness"]
---

# Trazabilidad de aceptación por versión

## Procedimiento

1. Identificá candidata, entorno y tickets incluidos a partir del alcance acordado. Extraé cada criterio con el identificador del ticket y conservá su texto o enlace. Señalá discrepancias entre lo comprometido y lo desplegado.
2. Asociá cada criterio con resultados de tests, trazas, capturas o ejecución manual. Verificá versión, entorno y precondición. Una prueba con varias aserciones puede respaldar varios criterios si indicás cuál corresponde a cada uno.
3. Clasificá cada criterio como verificado, fallido, bloqueado o sin evidencia. Si el criterio incluye varias condiciones y falta alguna, indicá el resultado parcial y qué quedó sin verificar. Un test verde en otra revisión queda como antecedente.
4. Entregá una matriz ticket → criterio → evidencia → resultado → acción pendiente. Resumí los bloqueos y las brechas de evidencia con sus responsables cuando estén identificados.

## Ejemplo de uso

**Pedido:** Armá el cierre de QA de la candidata de salas con los tickets incluidos y las trazas de staging.

**Resultado:** Entrega una fila por criterio y marca como pendiente el que solo tenga evidencia de una versión anterior.
