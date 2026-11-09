---
name: g10-weekly-sheet-checker
description: Verificar si el reporte semanal de una planilla está completo para el período correcto, recordar campos pendientes y proponer semáforos, avances, fechas y comentarios con evidencia de Jira y GitHub. Usar para revisar un tablero semanal o preparar su actualización.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere:
  - google-sheets
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
# Weekly Sheet Checker

Comprobar el reporte de la semana correspondiente y preparar valores sugeridos para que el usuario pueda completarlo. Mantener la skill general: proyecto, planilla, calendario, fuentes y horario pertenecen al contexto de cada tarea.

## Regla absoluta: no modificar la planilla

**Bajo ningún concepto modificar el Sheet o la planilla consultada.** Esta skill es exclusivamente de lectura: no escribir, pegar ni borrar valores o fórmulas; no cambiar formatos, validaciones, filas, columnas, pestañas, comentarios, notas, permisos ni configuración. Tampoco ejecutar operaciones de escritura por conectores, API, scripts u otros agentes. La navegación, selección y copia para lectura están permitidas. Las sugerencias se entregan en el chat o en un archivo local separado para que el usuario las cargue por su cuenta; esta skill no ofrece ni ejecuta una carga posterior.

## Contexto y período

Leer `context_path` cuando se proporcione; si falta, buscar `pm/weekly-sheet-context.json` en el proyecto actual. Usar las fuentes explícitas del usuario y pedir solo la información indispensable que siga faltando. Trabajar en su idioma y en la zona horaria del reporte.

Obtener de ese contexto el enlace y la pestaña exactos, identidad del equipo/proyecto, encabezados de fechas, filas editables, campos calculados, reglas de estado y fuentes de evidencia. Verificar esas referencias contra la hoja actual: las posiciones guardadas son una ayuda para localizar, no una garantía de que el diseño no haya cambiado.

Elegir la columna por la fecha local de ejecución y la convención de la hoja. Si el encabezado identifica el lunes de cada semana, el miércoles corresponde al lunes de esa misma semana. No elegir la última columna completada ni una semana futura por estar vacía. Resolver el año con el calendario del reporte; ante una fecha ambigua o una columna inexistente, informar la limitación sin dar el reporte por pendiente.

Si el usuario solicita expresamente probar otra semana, usar `--week-start` y marcar el resultado como vista previa. Mantener la lectura y el corte de evidencia en la fecha real: una prueba de una semana futura no autoriza inventar hechos futuros ni cambiar la fecha del snapshot.

La instalación de la skill no crea una programación. Para crear o cambiar una revisión recurrente solicitada, usar las herramientas de automatización disponibles y conservar la zona horaria y el horario acordados.

## Leer y decidir si falta completar

Preferir un conector de planillas disponible. Si falta o no permite leer el enlace, usar la skill de computer-use y el navegador para consultar la hoja. En Google Sheets puede leerse un rango mediante el cuadro de nombres y copiarlo al portapapeles de la sesión, sin escribir sobre la grilla. Verificar título, pestaña, fecha y valores observados.

Para validar la semana y la completitud de forma reproducible, usar `scripts/check_week.py` con el contexto y un snapshot recién leído. El contrato de entrada y el comando están en [references/snapshot-format.md](references/snapshot-format.md). El script no accede a la red ni cambia la planilla.

- Comprobar todos los campos semanales editables requeridos, no solo el resumen calculado: una fórmula puede mostrar Verde aunque falten áreas.
- Comprobar los motivos exigidos por la plantilla para estados de alerta. Un comentario compartido entre semanas puede existir y estar desactualizado; evaluar su pertinencia sin afirmar que fue escrito esta semana.
- Distinguir completo, incompleto, requiere revisión y no verificable. Un error de acceso, snapshot antiguo o lectura parcial no prueba que el usuario haya olvidado cargar datos.
- Distinguir cero, vacío y no aplicable. Respetar campos calculados, celdas combinadas y listas de valores.
- Una actividad, incidente o fecha fuera de la grilla semanal puede requerir revisión. Informar esa brecha por separado; no convertir campos opcionales ni futuras semanas vacías en faltantes.
- Sin historia de celdas o un registro fiable, indicar únicamente que los campos tienen contenido. Un valor igual al anterior puede ser correcto; la igualdad no demuestra falta de actualización.

## Preparar sugerencias con Jira y GitHub

Si falta completar el reporte, o el usuario pide recomendaciones, consultar la actividad y el trabajo pendiente pertinentes a la fecha de corte. Incluir arrastres que afecten la entrega aunque no se hayan actualizado esa semana. Respetar el alcance configurado de sprint, etiquetas, tickets o actividades; resolver el período activo desde sus fuentes, sin fijar un sprint para todas las ejecuciones.

Paginar consultas cuando corresponda. Leer descripciones y criterios, fechas, estados y vínculos necesarios; contrastar PR, código, checks y evidencia de despliegue cuando cambien la conclusión. Un ticket cerrado, un merge o CI verde prueban cosas distintas. Señalar discrepancias entre fuentes.

Para cada campo ofrecer: celda o actividad, valor actual, sugerencia, motivo y enlaces a evidencia. Adaptar el contenido a la plantilla:

- **Alcance:** cambios respecto de la entrega acordada, brechas o decisiones pendientes. Diferenciar una ampliación aprobada de trabajo agregado sin acuerdo.
- **Cronograma:** dependencias, vencimientos y trabajo restante en relación con el compromiso. Separar fecha base, nueva estimación y fecha real; conservar las fechas originales.
- **Incidentes:** fallos o impedimentos observados, impacto y resolución comprobada. Una incógnita o una dependencia futura no es automáticamente un incidente.
- **Calidad:** criterios verificados, pruebas y defectos relevantes. La ausencia de bugs registrados no demuestra ausencia de problemas.
- **Riesgos:** condiciones que pueden afectar el objetivo y posibles mitigaciones, distinguiéndolas de problemas ya ocurridos.
- **General:** seguir la fórmula o regla existente, explicando de qué estados resulta. No sustituirla por una regla propia.
- **Actividades y avance:** vincular entregables reales a cada actividad. Respetar hitos ya aceptados y aclarar si una ampliación es una etapa nueva. Evitar contar simultáneamente historias y subtareas.
- **Porcentajes:** usar el método acordado cuando exista y mostrar alcance, denominador y ponderación. Si la evidencia es parcial, proponer un rango o un valor conservador marcado como estimación, con lo que falta para terminar. No convertir cantidades de commits, porcentajes de CI ni el avance del sprint en avance global del proyecto.
- **Fechas estimadas:** basarse en trabajo restante, dependencias y capacidad conocida, con supuestos visibles. Una fecha de merge no es por sí sola la fecha real de aceptación o despliegue.
- **Comentarios y próximos avances:** redactar texto breve listo para copiar, diferenciando lo entregado, lo integrado, lo verificado y lo previsto. Mantener el signo de desvíos y demás convenciones de la hoja.

Usar primero los criterios de estado de la plantilla; si faltan, identificar cualquier criterio propuesto como tal. Donde no haya evidencia suficiente, dejar la decisión pendiente y explicar qué dato falta.

## Recordatorio y seguimiento

En una revisión programada, producir un recordatorio accionable cuando la semana esté incompleta: indicar semana, pestaña, enlace y celdas pendientes, seguido de las sugerencias necesarias. Si está completo y no hay un cambio material que requiera acción, no emitir un recordatorio. En una invocación manual, responder al pedido aunque esté completo.

Si no puede verificarse, explicar qué acceso o dato impide la comprobación sin afirmar que faltó la carga. Guardar, si hay una ruta configurada, un estado mínimo por proyecto, planilla, pestaña y semana: última lectura, resultado y faltantes o impedimento ya informados. Evitar avisos duplicados sin cambios dentro de esa misma semana.

El recordatorio y el borrador no autorizan modificar Jira/GitHub ni contactar a otras personas. La planilla permanece exclusivamente de lectura bajo la regla absoluta de esta skill. Los archivos locales de contexto, snapshots o seguimiento están separados de la planilla y nunca deben usarse para una escritura de vuelta.

## Ejemplo de uso

**Pedido:** Los miércoles por la noche revisá si completé el tablero de esta semana. Si falta algo, recordámelo y sugerí estados, avances y comentarios según el tablero de tareas y el repositorio.
**Resultado:** Identificación de la columna correcta, comprobación de sus campos y, cuando corresponda, un recordatorio con valores propuestos y evidencia. La programación y los datos del proyecto se guardan en la tarea correspondiente.
