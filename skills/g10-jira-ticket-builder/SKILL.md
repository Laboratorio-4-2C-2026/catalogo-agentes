---
name: g10-jira-ticket-builder
description: "Convertir requisitos, ideas o bugs en borradores de tickets y subtareas de Jira con criterios de aceptación y dependencias. Crear o actualizar los borradores aprobados cuando el usuario lo autorice."
metadata:
  tipo: skill
  area: [gestion]
  fase: [analisis, planificacion]
  tecnologias: [agnostico]
  metodologia: agnostico
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

# Jira Ticket Builder

Convertir una necesidad concreta en tickets que el equipo pueda implementar y verificar.

## Contexto y permisos

Leer `context_path` si el usuario lo indicó; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Las decisiones explícitas del usuario prevalecen sobre ese archivo. Si falta, pedir solo los datos necesarios para este trabajo. Responder en el idioma del usuario y usar la zona horaria del proyecto.

Tomar sitio, repositorios, ramas, equipo, disponibilidad, calendarios, umbrales y rutas de salida de la tarea o de una configuración vinculada explícitamente al proyecto actual. No asumir datos de un proyecto anterior ni buscar por defecto un perfil de proyecto fijo. Las tareas programadas pueden proporcionar su configuración mediante `context_path`; sus instrucciones específicas pertenecen a esa programación, no a esta skill.

Los directorios `storage` del contexto, si existen, determinan dónde guardar informes y capturas; en otro caso, usar rutas relativas al proyecto actual cuando corresponda. Si no se puede escribir allí, entregar los resultados con la limitación, sin perder lo consultado.

El alcance debe identificar sitio y proyecto Jira, más un sprint nativo, una JQL acotada o un conjunto explícito de tickets. Si el tablero no admite sprints, usar el alcance equivalente confirmado por el usuario. No tratar todo el proyecto como el último sprint ni cambiar automáticamente a otro sprint.

Usar los conectores disponibles de Atlassian y GitHub. Descubrir operaciones y campos propios del sitio antes de usarlos; paginar hasta completar el alcance. En consultas JQL de estimaciones, usar la vista de evidencia o campos verificados. Un error de permisos o una consulta incompleta no significa cero resultados. Citar tickets y PR; separar hechos, inferencias y datos faltantes.

Lecturas y borradores están permitidos. Antes de crear, editar, asignar, comentar, mover o cerrar objetos externos, presentar los cambios concretos y obtener aprobación para ellos; reutilizar una aprobación explícita ya dada para esos mismos cambios. La instalación o invocación de la skill no aprueba escrituras externas. En ejecuciones automáticas, producir resultados para el PM sin modificar Jira, GitHub o Confluence ni enviar mensajes.

## Construcción

- Leer la fuente proporcionada y los tickets relacionados. Buscar duplicados antes de proponer un alta; distinguir una coincidencia por nombre de un requisito realmente cubierto.
- Preparar título, problema y valor esperado, alcance y exclusiones relevantes, criterios de aceptación observables, dependencias y evidencia fuente. Para bugs, incluir pasos de reproducción, esperado, observado y entorno si se conocen.
- Agrupar en un solo ticket el trabajo que entrega un mismo resultado verificable. Usar una lista de pasos técnicos dentro del ticket cuando ayude a implementarlo. Mantener precisos el alcance y los criterios de aceptación. Por ejemplo, «Exportar resultados filtrados a CSV» puede cubrir en un ticket qué filtros respeta el archivo, qué columnas incluye y cómo se descarga.
- Dividir cuando haya una razón concreta, como resultados que se pueden entregar por separado, responsables distintos, una dependencia entre entregas o un límite de capacidad. Usar subtareas si hace falta asignar o seguir por separado partes del mismo resultado. Identificar qué información falta sin inventar endpoints, decisiones de arquitectura o requisitos.
- Si backend y frontend tienen responsables o momentos de ejecución distintos, separar sus entregas en tickets o subtareas ejecutables con un solo responsable. Mantener un padre funcional si ayuda a agruparlas, sin usarlo para ocultar trabajo que espera por otro rol.
- Describir el contrato necesario y la evidencia de entrega de backend sin depender de frontend. Si la interfaz con mocks se entrega antes de la integración, indicar qué entrega previa del backend habilita la integración real.
- Usar los límites por persona y semana del contexto al dimensionar tickets. Si el trabajo excede la capacidad disponible, proponer entregas más pequeñas con resultados verificables y estimaciones identificadas como propuestas. No combinar las horas de dos roles para justificar un ticket que solo uno puede implementar.
- En cada ticket dependiente, indicar qué entrega habilita su inicio y cómo se comprueba. Si se aprueba crear vínculos en Jira, descubrir los tipos de enlace válidos y su dirección antes de aplicarlos.
- Respetar el presupuesto y las exclusiones del contexto: no agregar tickets de reuniones, revisión o pruebas que el usuario no pidió. Conservar criterios de aceptación existentes y señalar una brecha de capacidad si exigen trabajo adicional.
- Proponer tipo, prioridad, responsable, épica, estimación y sprint únicamente con respaldo o marcados como propuesta. No convertir puntos en horas.
- Al preparar una escritura, verificar tipos disponibles, campos obligatorios, usuarios asignables y jerarquía válida del proyecto. No adivinar accountIds, IDs de campos ni transiciones.
- Si se modifica un ticket, leer primero su contenido y mostrar el cambio. Preservar texto, listas y medios fuera de lo aprobado; los campos de lista suelen reemplazarse completos.

## Aplicación y resultado

Entregar primero los borradores y sus vínculos de dependencia. Obtener aprobación del contenido y de los destinos externos concretos antes de escribir.

Aplicar padres antes que hijos dependientes y registrar la clave creada en cada paso. Si una respuesta devuelve una clave pero falla la asignación al sprint, reparar solo la asignación aprobada: no repetir la creación. Ante un timeout o resultado ambiguo, buscar y comprobar el objeto antes de reintentar. Detener el lote ante una falla que requiera cambiar contenido o permisos; informar qué quedó aplicado y qué falta.

Entregar una tabla con borrador, clave/URL si se creó, cambios aplicados y pendientes. No declarar completado un lote parcial.

## Ejemplo de uso

**Pedido:** Convertí este requisito en tickets de Jira: exportar a CSV los resultados filtrados, con backend y frontend a cargo de personas distintas.
**Resultado:** Borradores con problema, alcance, criterios de aceptación y dependencias, separados si cada parte tiene otro responsable. No crea ni edita nada en Jira hasta que apruebes el contenido y el destino.
