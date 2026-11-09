---
name: g10-sprint-health
description: Evaluar el estado de un sprint con Jira, ramas, commits y PR de GitHub, estimando avance técnico aproximado cuando se solicita. Usar en controles diarios o revisiones de salud; no para crear el plan inicial.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  requiere:
  - jira
  - github
  grupo: "10"
  autor:
    nombre: Marcos Carrizo Aslanian
    github: MarcosCarrizoA
  responsables:
  - MarcosCarrizoA
  madurez: experimental
  relacionados: []
---
# Sprint Health

Dar al PM una lectura del avance y de las decisiones que amenazan el objetivo del sprint.

## Contexto y permisos

Leer `context_path` si el usuario lo indicó; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Las decisiones explícitas del usuario prevalecen sobre ese archivo. Si falta, pedir solo los datos necesarios para este trabajo. Responder en el idioma del usuario y usar la zona horaria del proyecto.

Tomar sitio, repositorios, ramas, equipo, disponibilidad, calendarios, umbrales y rutas de salida de la tarea o de una configuración vinculada explícitamente al proyecto actual. No asumir datos de un proyecto anterior ni buscar por defecto un perfil de proyecto fijo. Las tareas programadas pueden proporcionar su configuración mediante `context_path`; sus instrucciones específicas pertenecen a esa programación, no a esta skill.

Los directorios `storage` del contexto, si existen, determinan dónde guardar informes y capturas; en otro caso, usar rutas relativas al proyecto actual cuando corresponda. Si no se puede escribir allí, entregar los resultados con la limitación, sin perder lo consultado.

El alcance debe identificar sitio y proyecto Jira, más un sprint nativo, una JQL acotada o un conjunto explícito de tickets. Si el tablero no admite sprints, usar el alcance equivalente confirmado por el usuario. No tratar todo el proyecto como el último sprint ni cambiar automáticamente a otro sprint.

Un archivo local con alcance pendiente puede estar desactualizado: antes de declarar que el sprint no es evaluable, consultar en Jira la fuente de pertenencia indicada por el contexto o la tarea, por ejemplo una etiqueta explícita de sprint. Si devuelve tickets coherentes con el sprint solicitado, usarlos y actualizar la copia local cuando se pueda. Una bandera local pendiente no debe impedir esa lectura. Si no hay evidencia suficiente o la consulta falla, entregar el estado parcial y la limitación.

Usar los conectores disponibles de Atlassian y GitHub. Descubrir operaciones y campos propios del sitio antes de usarlos; paginar hasta completar el alcance. En consultas JQL de estimaciones, usar la vista de evidencia o campos verificados. Un error de permisos o una consulta incompleta no significa cero resultados. Citar tickets y PR; separar hechos, inferencias y datos faltantes.

Lecturas y borradores están permitidos. Antes de crear, editar, asignar, comentar, mover o cerrar objetos externos, presentar los cambios concretos y obtener aprobación para ellos; reutilizar una aprobación explícita ya dada para esos mismos cambios. La instalación o invocación de la skill no aprueba escrituras externas. En ejecuciones automáticas, producir resultados para el PM sin modificar Jira, GitHub o Confluence ni enviar mensajes.

## Evaluación

- Cuando el contexto pide seguimiento exclusivo de un sprint, limitar las métricas a sus miembros confirmados y a su ventana de inicio y cierre. Un ticket previo puede ser arrastre explícito; sus resultados anteriores al inicio no son avance nuevo del sprint. Consultar dependencias externas solo para explicar el impacto en sus miembros.
- Antes del inicio, no medir avance del sprint. Después del cierre, reconstruir el estado a esa fecha mediante historia o capturas; no incluir cambios posteriores ni sustituirlo por el estado actual. Si falta el alcance o la evidencia para reconstruirlo, indicar qué no es evaluable sin ampliar la consulta a otros sprints.
- Consultar el alcance confirmado, las fechas, el objetivo, los estados y estimaciones, responsables y dependencias. Relacionar PR con tickets mediante claves o enlaces explícitos; una similitud de título solo es una asociación tentativa.
- Si la vista de evidencia no devuelve vencimientos, seguimiento de tiempo o enlaces, pedir esos campos explícitamente con vista full antes de declararlos ausentes. La omisión de un campo en una vista resumida no demuestra que Jira no lo tenga.
- Contar trabajo una sola vez por nivel de jerarquía. Informar total, terminado, en curso y pendiente; mantener horas y puntos en métricas separadas y exponer cuántos tickets carecen de estimación.
- Identificar trabajo bloqueado, revisiones pendientes, entregables cercanos al cierre y desbalance de carga cuando exista capacidad verificable. Un PR abierto o una ausencia de actualización son señales, no bloqueos confirmados por sí solos.
- Comparar con una captura anterior del mismo alcance si está disponible: incorporaciones y retiros, cambios de estado, estimaciones y riesgos. En la primera ejecución establecer una base; sin historia no inferir velocidad, burn-down ni porcentaje del compromiso inicial.
- Calcular carga restante versus capacidad restante solo cuando ambas estén disponibles en la misma unidad y período. No asignar una probabilidad de entrega ni un semáforo saludable a datos incompletos.
- Cuando la disponibilidad esté separada por rol y semana, comparar cada carga con su propio límite. No usar la suma del equipo para ocultar sobrecarga de un rol ni descontar obligaciones fuera del presupuesto declarado.
- Dar estado favorable, en riesgo, comprometido o no evaluable con evidencia: favorable requiere información suficiente; comprometido requiere una amenaza concreta al objetivo o al plazo. Mostrar las razones y las limitaciones.

## Avance técnico desde el repositorio

Cuando el usuario pida revisar ramas o estimar porcentajes, o el contexto active `repository_progress`, leer [references/repository-progress.md](references/repository-progress.md). Buscar trabajo publicado aunque todavía no tenga PR. Evaluar el código frente a los criterios de cada ticket y entregar una estimación aproximada con confianza, evidencia y trabajo pendiente, separada del estado de Jira. La ausencia de una rama o de un PR no demuestra 0 % de avance.

## Resultado y monitoreo

Entregar fecha de corte, alcance, estado y fundamento, métricas, cambios relevantes y acciones propuestas con responsables conocidos o por confirmar.

Si hay un proyecto local disponible, conservar una captura mínima en `pm/state/sprint-health.json`, identificada por sitio, proyecto y alcance, y guardar el informe en `pm/reports/`. Leer solo capturas del mismo alcance. Conservar el compromiso inicial si se conoce y compararlo separado del alcance actual.

Respetar la modalidad de entrega pedida en la tarea o el contexto. Si el usuario espera un reporte diario, entregar un resumen en cada ejecución, también sin cambios o con datos parciales. Si pidió únicamente alertas por cambios, mantener silencio cuando no haya novedades accionables. La falta de permiso para guardar un archivo no debe impedir entregar el reporte en el chat. El reporte semanal es un flujo independiente.

Si el seguimiento está limitado a un sprint que ya cerró, entregar solo el balance de cierre acordado y luego respetar la política del contexto para evitar reportes repetidos o cambiar de sprint.

## Ejemplo de uso

**Pedido:** ¿Cómo viene el sprint hoy? Cruzá Jira con las ramas y los PR y decime si el objetivo está en riesgo.
**Resultado:** Estado a la fecha de corte (favorable, en riesgo, comprometido o no evaluable), con métricas y acciones. Si pedís avance técnico, suma una estimación aproximada del código, separada del estado de Jira.
