---
name: g13-definition-of-done
description: "Verifica si una historia puede cerrarse con evidencia de entrega y cumplimiento de sus criterios. Usar después de integrar cambios y antes de cerrar el ticket."
metadata:
  tipo: agente
  area: ["gestion", "qa"]
  fase: ["revision"]
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
  relacionados: ["g13-definition-of-ready", "g13-matriz-de-trazabilidad", "g13-checklist-pre-deploy", "g02-done-evidence-check", "g11-dod-checker"]
---

# Definition of Done

Recibís la historia, sus criterios de aceptación, la definición de Done del equipo y las referencias de entrega. Inspeccioná la evidencia que esté accesible o que el usuario haya adjuntado. Reportá como pendiente una fuente que no puedas verificar.

1. Vinculá cada criterio con una evidencia de cumplimiento: prueba, verificación manual o aceptación registrada, según lo que exija el equipo.
2. Verificá que las PR necesarias estén integradas en la rama objetivo y que las pruebas requeridas correspondan a la revisión entregada. Un enlace a una PR abierta o un check de otro commit no alcanza.
3. Comprobá la documentación y el despliegue si el cambio o la definición del equipo los requiere. Registrá el entorno y la versión cuando haya despliegue. Usá **No aplica** solo con una razón verificable; si no se conoce la regla, preguntá.
4. Devolvé una tabla **control | estado | evidencia | acción pendiente** y un veredicto **Cumple** o **No se puede cerrar**. Reservá **Cumple** para cuando estén acreditados todos los controles aplicables.

Este control verifica la entrega completa de una historia; no aprueba PR ni cambia el estado del ticket.

## Ejemplo de uso

**Pedido:** ¿Podemos cerrar la historia de pausar un aviso? La PR está integrada y CI pasó. El equipo exige desplegar a staging, pero no tengo el registro.

**Resultado:** Devuelve **No se puede cerrar**. Registra la PR y CI como evidencia válida si corresponden al cambio y deja pendiente verificar el despliegue en staging.
