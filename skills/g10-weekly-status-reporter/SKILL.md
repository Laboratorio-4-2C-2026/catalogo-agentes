---
name: g10-weekly-status-reporter
description: "Preparar un informe semanal de un sprint de software combinando Jira y GitHub con enlaces a avances, bloqueos, riesgos y próximos pasos. Usar para cortes o períodos semanales solicitados; publicar solo con aprobación."
metadata:
  tipo: skill
  area: [gestion]
  fase: [revision]
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

# Weekly Status Reporter

Preparar un reporte breve y verificable que el PM pueda revisar y compartir.

## Contexto y permisos

Leer `context_path` si el usuario lo indicó; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Las decisiones explícitas del usuario prevalecen sobre ese archivo. Si falta, pedir solo los datos necesarios para este trabajo. Responder en el idioma del usuario y usar la zona horaria del proyecto.

Tomar sitio, repositorios, ramas, equipo, disponibilidad, calendarios, umbrales y rutas de salida de la tarea o de una configuración vinculada explícitamente al proyecto actual. No asumir datos de un proyecto anterior ni buscar por defecto un perfil de proyecto fijo. Las tareas programadas pueden proporcionar su configuración mediante `context_path`; sus instrucciones específicas pertenecen a esa programación, no a esta skill.

Los directorios `storage` del contexto, si existen, determinan dónde guardar informes y capturas; en otro caso, usar rutas relativas al proyecto actual cuando corresponda. Si no se puede escribir allí, entregar los resultados con la limitación, sin perder lo consultado.

El alcance debe identificar sitio y proyecto Jira, más un sprint nativo, una JQL acotada o un conjunto explícito de tickets. Si el tablero no admite sprints, usar el alcance equivalente confirmado por el usuario. No tratar todo el proyecto como el último sprint ni cambiar automáticamente a otro sprint.

Antes de aceptar una bandera local de alcance pendiente, consultar la fuente de pertenencia configurada en Jira, por ejemplo una etiqueta explícita de sprint. La información local puede estar desactualizada. Si Jira identifica coherentemente sus tickets, usarlos y actualizar la copia local cuando se pueda; no pedir una confirmación manual duplicada para leerlos. Si falta evidencia o falla el acceso, entregar el reporte parcial y su limitación.

Usar los conectores disponibles de Atlassian y GitHub. Descubrir operaciones y campos propios del sitio antes de usarlos; paginar hasta completar el alcance. En consultas JQL de estimaciones, usar la vista de evidencia o campos verificados. Un error de permisos o una consulta incompleta no significa cero resultados. Citar tickets y PR; separar hechos, inferencias y datos faltantes.

Lecturas y borradores están permitidos. Antes de crear, editar, asignar, comentar, mover o cerrar objetos externos, presentar los cambios concretos y obtener aprobación para ellos; reutilizar una aprobación explícita ya dada para esos mismos cambios. La instalación o invocación de la skill no aprueba escrituras externas. En ejecuciones automáticas, producir resultados para el PM sin modificar Jira, GitHub o Confluence ni enviar mensajes.

## Preparación

- Definir fecha de corte y período en la zona horaria del proyecto. Respetar el período indicado en la tarea o configuración, sin fijar un día de reporte ni asumir un calendario laboral. Si no se definió el intervalo, explicitar el período propuesto para el informe. Si el contexto limita el seguimiento a un sprint, recortar ese período a la intersección con sus fechas: no incluir días anteriores al inicio ni posteriores al cierre.
- En un seguimiento exclusivo, mostrar primero el estado acumulado del sprint a la fecha de corte, y luego los cambios de la semana. Incluir únicamente sus tickets confirmados y sus PR vinculados. El arrastre desde otro sprint requiere inclusión explícita; su avance previo no se cuenta como resultado nuevo.
- Consultar todo el alcance confirmado y su actividad del período. Obtener historia cuando sea necesaria para saber qué terminó, cambió de alcance o se reabrió; el estado actual y la fecha updated no prueban que un ticket terminó esta semana.
- Si la vista de evidencia omite vencimientos o estimaciones, solicitar los campos explícitamente con vista full antes de considerarlos faltantes. El resumen de una respuesta no representa siempre todos los campos existentes en Jira.
- Consultar PR de los repositorios confirmados y vincularlos por claves o enlaces. Separar PR creados, fusionados y pendientes; un merge no equivale a despliegue ni a ticket aceptado.
- Comparar con el reporte anterior del mismo sprint cuando exista. Sin base previa, indicar que es el primer reporte y evitar afirmar tendencias.
- Sintetizar avance hacia el objetivo, entregables verificados, trabajo en curso, bloqueos confirmados, riesgos, decisiones del PM y próximos pasos. Dar responsable y fecha solo si son conocidos; marcar propuestas.
- Mantener conteos, horas y puntos separados y evitar duplicar padres con subtareas o un ticket por cada PR. No evaluar desempeño individual por cantidad de commits o tickets.
- Comparar trabajo restante y capacidad por persona, rol y semana cuando estén disponibles. Respetar qué trabajo cubren las horas declaradas, sin transferir capacidad entre roles ni sumar obligaciones no presupuestadas.
- Si alguna fuente falla, entregar el informe parcial indicando fuente, cobertura y lo que no puede concluirse. No presentar la ausencia de acceso como ausencia de actividad.

## Entrega y publicación

Entregar un resumen ejecutivo, avance del objetivo, resultados del período, bloqueos y riesgos, y próximos pasos con enlaces a evidencia. Incluir alcance y fecha de corte para que pueda leerse fuera del chat.

Si hay proyecto local disponible, guardar el reporte fechado en `pm/reports/` y una base mínima del mismo alcance en `pm/state/weekly-status-reporter.json`. En ejecución programada, entregar el reporte semanal solicitado aunque no haya novedades; diferenciar ausencia de cambios de ausencia de datos.

Si después de consultar la fuente de pertenencia en Jira sigue faltando el alcance, informar la limitación sin sustituirlo por el backlog general ni por reportes de otros sprints. Si no se puede guardar un archivo, entregar igualmente el informe en el chat. Después del cierre, reconstruir el balance a esa fecha mediante historia o capturas y respetar la política del contexto sobre un único reporte final. No presentar cambios posteriores como resultados del sprint.

No publicar en Confluence, comentar en Jira ni enviar por correo o mensajería sin aprobación del contenido y destino concretos.

## Ejemplo de uso

**Pedido:** Prepará el informe semanal de este sprint: avances, bloqueos, riesgos y próximos pasos, con enlaces a Jira y GitHub.
**Resultado:** Resumen con fecha de corte y evidencia. Queda en el chat o en un archivo local; no lo publica en Confluence ni lo envía sin aprobación.
