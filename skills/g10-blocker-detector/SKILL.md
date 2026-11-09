---
name: g10-blocker-detector
description: Encontrar bloqueos y dependencias que detienen tickets de un sprint usando Jira, comentarios y PR de GitHub. Usar para revisar impedimentos o vigilar bloqueos; distinguir bloqueos confirmados de señales de riesgo.
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
# Blocker Detector

Identificar qué impide avanzar, qué evidencia lo confirma y qué decisión puede destrabarlo.

## Contexto y permisos

Leer `context_path` si el usuario lo indicó; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Las decisiones explícitas del usuario prevalecen sobre ese archivo. Si falta, pedir solo los datos necesarios para este trabajo. Responder en el idioma del usuario y usar la zona horaria del proyecto.

Tomar sitio, repositorios, ramas, equipo, disponibilidad, calendarios, umbrales y rutas de salida de la tarea o de una configuración vinculada explícitamente al proyecto actual. No asumir datos de un proyecto anterior ni buscar por defecto un perfil de proyecto fijo. Las tareas programadas pueden proporcionar su configuración mediante `context_path`; sus instrucciones específicas pertenecen a esa programación, no a esta skill.

Los directorios `storage` del contexto, si existen, determinan dónde guardar informes y capturas; en otro caso, usar rutas relativas al proyecto actual cuando corresponda. Si no se puede escribir allí, entregar los resultados con la limitación, sin perder lo consultado.

El alcance debe identificar sitio y proyecto Jira, más un sprint nativo, una JQL acotada o un conjunto explícito de tickets. Si el tablero no admite sprints, usar el alcance equivalente confirmado por el usuario. No tratar todo el proyecto como el último sprint ni cambiar automáticamente a otro sprint.

Usar los conectores disponibles de Atlassian y GitHub. Descubrir operaciones y campos propios del sitio antes de usarlos; paginar hasta completar el alcance. En consultas JQL de estimaciones, usar la vista de evidencia o campos verificados. Un error de permisos o una consulta incompleta no significa cero resultados. Citar tickets y PR; separar hechos, inferencias y datos faltantes.

Lecturas y borradores están permitidos. Antes de crear, editar, asignar, comentar, mover o cerrar objetos externos, presentar los cambios concretos y obtener aprobación para ellos; reutilizar una aprobación explícita ya dada para esos mismos cambios. La instalación o invocación de la skill no aprueba escrituras externas. En ejecuciones automáticas, producir resultados para el PM sin modificar Jira, GitHub o Confluence ni enviar mensajes.

## Detección

- Buscar estados o marcas de bloqueo, enlaces de dependencia pendientes y comentarios que documenten un impedimento. Leer comentarios relevantes y las dependencias fuera del alcance cuando sean necesarias para explicar un ticket dentro de él.
- Revisar PR vinculados: cambios solicitados, revisiones pendientes, conflictos y checks del último commit. Distinguir un check fallido vigente de uno superado por una nueva ejecución.
- Clasificar como bloqueo confirmado cuando exista impedimento explícito o una dependencia necesaria sin resolver; como posible bloqueo cuando solo haya antigüedad, falta de responsable o señales indirectas.
- Medir espera en días laborables solo con calendario conocido y timestamps pertinentes. Una edición reciente del ticket no prueba avance. Usar umbrales acordados en el contexto; si faltan, proponerlos sin convertirlos en reglas aprobadas.
- Priorizar por impacto sobre el objetivo, fecha límite y cantidad de tickets dependientes, con evidencia. No inferir responsabilidad personal a partir de una demora.
- Para cada hallazgo, indicar ticket, bloqueo, fuente, momento observado, impacto, responsable conocido o por confirmar y acción sugerida. Separar una recomendación del PM de una decisión del equipo.

## Resultado y monitoreo

Entregar una tabla de bloqueos confirmados y señales por validar, ordenada por impacto, seguida de las decisiones necesarias.

Si hay almacenamiento local, comparar y conservar hallazgos mínimos del mismo alcance en `pm/state/blocker-detector.json`. Un error de consulta no resuelve hallazgos anteriores: marcarlos como sin verificar.

En ejecución automática, notificar bloqueos nuevos, cambios de impacto, resolución relevante o pérdida de acceso; mantener silencio si no cambió nada accionable. No comentar ni etiquetar tickets ni contactar integrantes automáticamente.

## Ejemplo de uso

**Pedido:** Revisá el sprint y separá los tickets frenados de verdad de las señales que todavía hay que validar.
**Resultado:** Tabla de bloqueos confirmados y señales, con evidencia, impacto y la decisión que podría destrabarlos. No comenta tickets ni avisa al equipo.
