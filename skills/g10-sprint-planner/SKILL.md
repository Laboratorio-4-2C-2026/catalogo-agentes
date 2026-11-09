---
name: g10-sprint-planner
description: "Proponer el alcance, las estimaciones, las subtareas y la distribución de un sprint de software a partir de Jira y la disponibilidad del equipo. Usar al planificar o replanificar; no para el monitoreo diario."
metadata:
  tipo: skill
  area: [gestion]
  fase: [planificacion]
  tecnologias: [agnostico]
  metodologia: scrum
  herramientas: [codex]
  requiere: [jira, github]
  grupo: "10"
  autor:
    nombre: Marcos Carrizo Aslanian
    github: MarcosCarrizoA
  responsables: [MarcosCarrizoA]
  madurez: experimental
  relacionados: []
---

# Sprint Planner

Preparar un plan viable que permita al PM decidir qué comprometer y qué dejar fuera del sprint.

## Contexto y permisos

Leer `context_path` si el usuario lo indicó; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Las decisiones explícitas del usuario prevalecen sobre ese archivo. Si falta, pedir solo los datos necesarios para este trabajo. Responder en el idioma del usuario y usar la zona horaria del proyecto.

Tomar sitio, repositorios, ramas, equipo, disponibilidad, calendarios, umbrales y rutas de salida de la tarea o de una configuración vinculada explícitamente al proyecto actual. No asumir datos de un proyecto anterior ni buscar por defecto un perfil de proyecto fijo. Las tareas programadas pueden proporcionar su configuración mediante `context_path`; sus instrucciones específicas pertenecen a esa programación, no a esta skill.

Los directorios `storage` del contexto, si existen, determinan dónde guardar informes y capturas; en otro caso, usar rutas relativas al proyecto actual cuando corresponda. Si no se puede escribir allí, entregar los resultados con la limitación, sin perder lo consultado.

El alcance debe identificar sitio y proyecto Jira, más un sprint nativo, una JQL acotada o un conjunto explícito de tickets. Si el tablero no admite sprints, usar el alcance equivalente confirmado por el usuario. No tratar todo el proyecto como el último sprint ni cambiar automáticamente a otro sprint.

Usar los conectores disponibles de Atlassian y GitHub. Descubrir operaciones y campos propios del sitio antes de usarlos; paginar hasta completar el alcance. En consultas JQL de estimaciones, usar la vista de evidencia o campos verificados. Un error de permisos o una consulta incompleta no significa cero resultados. Citar tickets y PR; separar hechos, inferencias y datos faltantes.

Lecturas y borradores están permitidos. Antes de crear, editar, asignar, comentar, mover o cerrar objetos externos, presentar los cambios concretos y obtener aprobación para ellos; reutilizar una aprobación explícita ya dada para esos mismos cambios. La instalación o invocación de la skill no aprueba escrituras externas. En ejecuciones automáticas, producir resultados para el PM sin modificar Jira, GitHub o Confluence ni enviar mensajes.

## Planificación

- Si el sprint todavía no tiene tickets asignados, consultar el backlog como candidatos y proponer un conjunto para aprobación. Los tickets de sprints anteriores pueden ser arrastre propuesto, pero no son miembros del nuevo sprint hasta confirmar el alcance.
- Obtener objetivo, fechas, backlog priorizado, dependencias y compromisos existentes. Para el último sprint, considerar integración, QA, correcciones, despliegue, documentación y demo cuando sean entregables acordados.
- Consultar la disponibilidad real de cada integrante y qué trabajo cubre el presupuesto. Si son horas netas para tickets de la app, no descontar nuevamente reuniones ni añadir horas de revisión o pruebas. Si son horas totales, descontar las obligaciones declaradas. Aplicar una reserva solo si fue acordada o mostrarla como escenario propuesto. No inventar dedicación, habilidades ni días laborables.
- Conservar estimaciones originales. Si faltan, proponer un rango de horas de trabajo con supuestos y confianza, separando implementación e integración de revisión y pruebas según el presupuesto acordado; pedir validación del equipo. No convertir puntos a horas ni asumir horas adicionales para trabajo fuera del presupuesto.
- Dividir trabajo grande o incierto en subtareas con resultado verificable, dependencia y rango de esfuerzo. Al sumar, elegir estimación del padre o de sus hijos, sin contabilizar ambos.
- Proponer responsables según disponibilidad y competencias conocidas. Comparar horas por persona y equipo; respetar la secuencia de dependencias y el tiempo para revisión. Con incertidumbre alta, presentar escenarios conservador y ampliado en vez de prometer una fecha.
- Separar alcance comprometible, opcional y diferido. Señalar conflictos de capacidad, dependencias externas y decisiones que debe tomar el PM.

## Dependencias y distribución semanal

- Planificar por persona, rol y semana. Respetar el límite individual del contexto: la capacidad total del equipo no permite sobrecargar frontend con horas disponibles de backend ni trasladar horas entre roles sin acuerdo.
- Separar trabajo de backend, frontend e integración cuando tengan responsables o condiciones de inicio distintos. Puede haber un padre funcional que agrupe el resultado, pero cada ticket o subtarea ejecutable debe tener un responsable, un entregable verificable y un límite claro; no dejar todo abierto en un único ticket hasta que ambos terminen.
- Definir primero el contrato mínimo que comparten las partes: datos, operaciones o eventos, errores y condiciones relevantes. Frontend puede avanzar con mocks compatibles cuando eso sea útil; distinguir explícitamente la interfaz con mocks de la integración con el servicio real.
- Hacer que backend pueda demostrar su entrega mediante evidencia propia, sin depender de una pantalla de frontend. La integración real de frontend empieza después de que el contrato y la capacidad de backend necesaria estén disponibles y verificados. Si falta una forma de verificarlo, señalarla antes de comprometer la integración; no dar backend por terminado por una fecha prometida.
- Para dependencias entre entregas, definir la secuencia según disponibilidad y coordinación reales. UI con un contrato acordado puede avanzar en paralelo al backend; la integración necesita una entrega previa verificable. Si la secuencia no cabe en el período, separar las entregas o ajustar el alcance, sin imponer una distribución semanal fija ni suponer coordinación no confirmada.
- Evitar dependencias circulares y detectar tickets cuyo inicio quedaría bloqueado. Proponer una tarea independiente útil para el rol que espera, o reducir el alcance antes de dejar capacidad ociosa planificada. No asegurar que desaparecerán los imprevistos externos.
- Priorizar dependencias críticas, complejidad e incertidumbre al comienzo. Mantener el cierre para integración ya habilitada, ajustes pequeños y entregables finales acordados. Si lo pesado no cabe antes del cierre, presentar un recorte de alcance; no acumular funciones grandes en la última semana.
- Dividir tickets que excedan la capacidad semanal individual en entregas menores estimadas. Cuando una integración exige trabajo de ambos, registrar por separado las horas de cada persona, sin duplicar un total ni ocultar esfuerzo.
- Respetar exclusiones de presupuesto del usuario: no agregar reuniones, revisión o suites de pruebas como tickets obligatorios si se acordó solo trabajo en la app. Si un criterio de aceptación existente exige ese trabajo y no tiene capacidad asignada, informar la brecha para una decisión del PM.

Adaptar la división al resultado y a la arquitectura del proyecto. No prescribir tecnología, agrupación de tickets o estrategia de integración a partir de ejemplos de otros trabajos.

## Entrega

Presentar objetivo y fechas; capacidad y supuestos; una tabla semanal de ticket, prioridad, responsable y rol, entregable, horas, dependencias y evidencia que habilita el inicio. Mostrar horas asignadas y disponibles por persona cada semana, indicando posibles esperas y la alternativa propuesta. Diferenciar estimaciones existentes de propuestas. Si falta información crítica, entregar un plan preliminar sin afirmar que es viable.

Si se solicita aplicar el plan, preparar el detalle exacto de asignaciones, campos y movimientos para aprobación. Ejecutar únicamente ese paquete aprobado y comprobar el resultado; ante respuesta incierta, consultar lo aplicado antes de reintentar.

## Ejemplo de uso

**Pedido:** Proponé el alcance del próximo sprint con el backlog de Jira y la disponibilidad del equipo: qué entra, quién lo hace y en qué semana.
**Resultado:** Plan con capacidad, tabla semanal de ticket, responsable, horas y dependencias, y alcance comprometible, opcional y diferido. No mueve tickets hasta que apruebes ese paquete.
