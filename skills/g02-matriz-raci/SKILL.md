---
name: g02-matriz-raci
description: Usar para armar o revisar la matriz RACI de Zest cruzando las actividades de la WBS con los roles del equipo (PM, PO, Tech Lead, QA y los dos devs), con exactamente un Aprobador por actividad, y para mapear los roles a las personas en cada steering, ya que en Zest los roles de gestión rotan. Detecta actividades sin dueño, aprobadores duplicados y sobrecarga.
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
  requiere:
  - google-drive
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: experimental
  relacionados:
  - g02-zest-onboarding
  - g02-status-report-format
  - g03-pm-po-agent
---
# Matriz RACI de Zest

La RACI responde **quién hace, quién aprueba, a quién se consulta y a quién se informa** en cada
actividad. En el Charter de Zest faltaba, y el equipo lo reconoció como una mejora pendiente.
Esta skill la arma y la mantiene. **No asigna tareas en Multica ni modifica la planilla sin OK.**

## Conceptos (cátedra, unidad de Recursos)

| Letra | Significa | Regla |
|---|---|---|
| **R** · Responsable | Hace el trabajo | Al menos uno por actividad |
| **A** · Aprobador (Accountable) | Responde por el resultado y lo aprueba | **Exactamente uno** por actividad |
| **C** · Consultado | Opina antes (comunicación de ida y vuelta) | Los necesarios, no todos |
| **I** · Informado | Se entera después | Los que necesitan saberlo |

También: **rol** (título), **responsabilidad** (qué se espera), **autoridad** (qué puede decidir)
y **competencia** (qué sabe hacer). La RACI es una de las vistas de la matriz de asignación de
responsabilidades (RAM), que cruza la WBS con el organigrama.

## Paso 1. Juntar el material

- **Actividades:** la WBS de la planilla de status del equipo (fases 1 a 5: planificación,
  análisis y diseño, desarrollo, pruebas y calidad, despliegue). Trabajá a nivel actividad, no
  ticket.
- **Roles:** PM, PO, Tech Lead, QA (gestión, Lab IV) y Dev backend y Dev frontend (Lab II).
- **Quién tiene cada rol en este steering:** en Zest los roles de gestión rotan. Pedilo o tomalo
  del último steering.

## Paso 2. Armar la matriz por rol

La matriz se arma con **roles, no con nombres**: así sobrevive a la rotación.

Criterios que usa el equipo:

- **Actividades de desarrollo:** R = el dev del área; A = Tech Lead; C = PO (reglas de negocio);
  I = PM y QA. Ejemplo del final de la materia: en "Gestión de recetas", R = Dev backend,
  A = Tech Lead, C = PO, I = PM.
- **Pruebas:** R = QA; A = Tech Lead; C = devs; I = PO y PM.
- **Alcance, prioridades y criterios de aceptación:** R = PO; A = PO; C = Tech Lead y QA; I = PM y
  devs.
- **Cronograma, presupuesto, valor ganado, riesgos y steering:** R = PM; A = PM; C = PO y Tech
  Lead; I = devs y QA.
- **Cambios de alcance:** R = PM; A = la cátedra si mueve el BAC o un hito, si no PM con PO; C = Tech
  Lead.
- **Arquitectura y despliegue:** R = Tech Lead o el dev; A = Tech Lead; C = PM si afecta costo o
  fecha.

## Paso 3. Controles

Marcá cada uno con la actividad y la propuesta de arreglo:

- Actividad **sin A** o **con más de un A**.
- Actividad **sin R**.
- **R = A** en todas las actividades de alguien: nadie revisa su trabajo.
- **Sobrecarga:** un rol con muchas R en el mismo período. Cruzalo con la disponibilidad: los
  devs tienen 6 h semanales.
- **C de más:** si todos son consultados en todo, nadie decide rápido.
- **Huecos de la rotación:** al cambiar de steering, actividades en curso cuyo A cambia de
  persona. Avisá para hacer el traspaso.

## Paso 4. Entregar

1. **Matriz por rol** (actividades × PM, PO, TL, QA, Dev back, Dev front), lista para pegar en la
   planilla.
2. **Roles → personas** por período:

   | Rol | Steering 1 | Steering 2 | Steering 3 |
   |---|---|---|---|

3. **Hallazgos de los controles** con su arreglo.
4. **Vista por persona** para el período actual: qué es R y qué es A cada una.

## Reglas

- Exactamente un A por actividad, sin excepciones.
- No inventar quién tiene cada rol: pedirlo si no está.
- No asignar ni reasignar tickets en Multica: la RACI es la propuesta, la asignación la hace el
  equipo.

## Ejemplo de uso

**Pedido:** "Armame la RACI de Zest para el Steering 3 con las actividades de la planilla de status."

**Resultado:** Una matriz por rol con todas las actividades de la WBS y exactamente un Aprobador en cada una, la tabla de qué persona tiene cada rol en los steerings 1, 2 y 3, los hallazgos (por ejemplo, actividades del planificador cuyo Aprobador cambia de persona con la rotación) y la vista de responsabilidades por persona para el período actual.
