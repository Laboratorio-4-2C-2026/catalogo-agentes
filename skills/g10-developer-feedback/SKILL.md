---
name: g10-developer-feedback
description: Evaluar el trabajo observable de cada desarrollador con Jira y GitHub, generar una nota de 0 a 10 con evidencia y dar feedback individual. Usar para evaluar contribuciones de un sprint o período, con capacidad, dependencias y datos incompletos explícitos.
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
# Developer Feedback

Preparar para el PM una evaluación individual del trabajo de cada desarrollador durante un sprint o período. Dar una nota numérica fundamentada, confianza, fortalezas y mejoras accionables. Escribir en el idioma del usuario.

## Contexto y alcance

Usar el período, equipo, escala y criterios indicados por el usuario. Leer `context_path` si la tarea lo proporciona; en su ausencia, buscar `pm/sprint-context.json` en el proyecto actual. Obtener fuentes, capacidad, zona horaria y directorios `storage` de esa tarea o de una configuración vinculada explícitamente al proyecto. No buscar por defecto un perfil fijo ni reutilizar datos de otros proyectos. Pedir solo información indispensable que las fuentes no permitan resolver.

Verificar dinámicamente la pertenencia al alcance solicitado mediante el sprint nativo, la consulta acotada o el conjunto de tickets indicado en la tarea o configuración. La lista local y la bandera de alcance pueden ser cachés desactualizadas. No asumir una clave de proyecto, etiqueta ni sprint predeterminados. Evaluar exclusivamente el alcance identificado y sus PR o ramas atribuibles. Consultar una dependencia externa solo para explicar el trabajo evaluado.

Durante un sprint, evaluar hasta el corte y marcar la nota como provisional. Después del cierre, reconstruir el estado al cierre con historia, commits y capturas. Distinguir trabajo anterior, incorporaciones de alcance y cambios posteriores. Si falla la reconstrucción, limitar la evaluación a lo verificable.

Respetar la capacidad confirmada de cada persona para el período y sus áreas de trabajo reales. No fijar nombres, roles, dedicaciones ni duración del sprint por defecto. Mantener presupuesto por persona y período; si falta capacidad verificable, explicitar esa limitación sin inventar horas disponibles. Las estimaciones registradas, las horas reales registradas y la cobertura técnica son magnitudes diferentes. Los días calendario transcurridos no determinan horas disponibles.

La ejecución consulta fuentes y entrega el resultado al usuario. Publicar evaluaciones, modificar Jira o GitHub y contactar al equipo requieren autorización específica. La invocación de esta skill permite preparar la evaluación.

## Reunir y atribuir evidencia

- Usar los conectores disponibles de Jira y GitHub y completar la paginación. Leer criterios, estado, responsable, subtareas, fechas de inicio/vencimiento, estimaciones originales/restantes, historial y dependencias. Solicitar vista `full` y campos explícitos cuando un resumen omita fechas o tiempo. Paginar también comentarios, revisiones e historia necesarios para justificar hallazgos.
- Crear un mapa de identidad entre responsable Jira y usuario GitHub con enlaces explícitos, autores y revisores corroborados. Registrar las asociaciones ambiguas y limitar las conclusiones afectadas. El responsable actual del ticket puede diferir de quien realizó el trabajo. Reconocer autoría compartida y contribuciones de revisión por separado, sin adjudicar a una persona el trabajo de otra.
- Contar las entregas ejecutables una vez. Una historia con subtareas aporta contexto y criterios, pero sus horas y su resultado no se suman otra vez. Un padre sin asignar no vuelve anónimas las subtareas asignadas.
- Buscar ramas por las claves reales de los tickets, normalizando mayúsculas y separadores. Corroborar números delimitados y nombres de tickets con el código. Exigir límites claros para no confundir una clave con el prefijo de otra. Buscar PR y commits aunque la rama desaparezca. Evaluar subtareas individualmente cuando compartan rama o historia.
- Verificar la rama por defecto y comparar cada rama con la base de su PR o esa rama verificada. Leer parches y código pertinentes, fijados a SHA, junto con criterios y revisiones. Una rama detrás de la base puede contener trabajo ya fusionado. Un merge de actualización aporta contexto de integración, pero no acredita nuevas funcionalidades.
- Separar implementación visible, PR abierto, revisión aprobada, fusión, aceptación Jira y despliegue verificado. Utilizar checks y validaciones existentes, indicando cuándo una prueba fue reportada por un autor o revisor. La ejecución de suites y despliegues queda fuera de esta evaluación.
- Comparar alcance, criterios, fechas y estimaciones con historia para detectar trabajo agregado sin nueva estimación, cambios de responsable y espera por dependencias o revisión ajena. Registrar los intervalos y su atribución cuando se puedan demostrar. Una fecha `updated` por sí sola no acredita una entrega ni un retraso individual.

## Rúbrica predeterminada

Usar la escala de 0 a 10 y los siguientes pesos, salvo que el usuario acuerde otros. Declarar la rúbrica antes de mostrar resultados. Aplicar la misma a todas las personas y conservarla para comparaciones del mismo período.

| Dimensión | Peso | Qué evaluar |
| --- | --- | --- |
| Cumplimiento funcional | 35 % | Cobertura y corrección observable de los criterios de cada entrega a la fecha de corte. Considerar código publicado con o sin PR y verificación funcional disponible. |
| Calidad técnica | 25 % | Validaciones, errores, consistencia de datos, mantenibilidad e integración con la arquitectura. Valorar evidencia de pruebas y hallazgos concretos de revisión acordes al ticket. |
| Cumplimiento del compromiso | 25 % | Entregas frente a compromisos y vencimientos vigentes, capacidad de la persona, cambios de alcance y dependencias demostradas. Evaluar solo compromisos exigibles al corte. |
| Colaboración e integración | 15 % | Contratos y documentación útiles, entregas que habilitan a otra persona, aportes de revisión y resolución de feedback atribuibles. Ajustar a las oportunidades observadas. |

La cobertura funcional describe qué funciona. La calidad técnica describe cómo está implementado. El compromiso describe cuándo se entregó respecto de lo acordado. La colaboración describe aportes a entregas compartidas. Ubicar cada hallazgo en su dimensión principal y explicar cualquier impacto adicional para evitar descontar mecánicamente lo mismo varias veces.

Para cada dimensión evaluable, usar estos anclajes con ejemplos y enlaces del trabajo de la persona.

- 9 a 10 corresponde a cumplimiento sólido con evidencia suficiente y sin brechas relevantes para esa dimensión.
- 7 a 8 corresponde a resultados mayormente cumplidos con brechas menores o verificaciones acotadas pendientes.
- 5 a 6 corresponde a cumplimiento parcial con brechas importantes, descritas y atribuibles.
- 3 a 4 corresponde a incumplimientos relevantes o problemas repetidos demostrados que afectan la entrega.
- 0 a 2 requiere evidencia directa de fallas graves en una oportunidad de trabajo confirmada y atribuible. La falta de datos se registra como no evaluable.

Las solicitudes de cambios son parte de una revisión normal. Valorar la gravedad, el criterio afectado y la respuesta del autor. Un PR pendiente de aprobación ajena o una dependencia pendiente no bastan para descontar puntos por compromiso o colaboración. Las dependencias internas tampoco prueban un bloqueo externo.

La cantidad de commits, líneas, archivos o tickets puede orientar búsquedas, pero no determina notas. Un porcentaje técnico aproximado tampoco se transforma automáticamente en la nota, las horas reales o un pronóstico de entrega. Evitar inferir esfuerzo, motivación, carácter o habilidad general a partir de actividad publicada. Evaluar el trabajo observado con atribución y límites explícitos.

## Calcular la nota y expresar incertidumbre

Puntuar cada dimensión de 0 a 10 antes de calcular el total. Explicar los hechos favorables y las brechas que justifican cada puntuación. Una calificación alta requiere evidencia positiva, incluso si no se encontraron defectos.

Cuando haya varias entregas, ponderar su evaluación funcional y técnica por las estimaciones originales acordadas, conservadas como referencia estable. Si faltan, declarar un criterio simple de complejidad basado en los requisitos antes de asignar las notas. Los tickets pequeños y las subtareas repetidas no deben dominar la evaluación por cantidad. Mostrar cuántas entregas y cuánto trabajo estimado se pudieron revisar.

Calcular `nota = suma(peso evaluable × puntuación) / suma(pesos evaluables)` y redondear a un decimal únicamente al final. Los pesos omitidos se excluyen del denominador. Mostrar la cobertura de dimensiones como suma de pesos evaluables y detallar los pesos efectivos si cambia la cobertura.

La ausencia de acceso, una identidad ambigua, trabajo sin publicar o falta de oportunidades para revisar a otros se registra como `NE` y afecta solo la conclusión correspondiente. Dar una nota parcial si la evidencia permite una evaluación individual fundada, mostrando la cobertura y confianza. Si no existe evidencia atribuible suficiente para una nota defendible, mostrar `NE` y explicar qué dato permitiría evaluarla. Nunca rellenar dimensiones desconocidas con cero, diez o una media inventada.

Indicar confianza alta, media o baja según atribución, amplitud del trabajo revisado y validación de criterios. Una nota provisional o parcial puede tener confianza baja. Comparar notas entre períodos únicamente con rúbrica y cobertura comparables, explicando cualquier cambio de evidencia o alcance. Un total basado en cobertura reducida requiere señalar qué dimensiones faltan y cuánto cambian los pesos.

## Entrega y conservación

Mostrar primero período, corte, alcance, rúbrica y límites que afectan el resultado. Preparar una tabla por desarrollador con nota sobre 10, estado provisional/parcial/final, confianza, notas de las cuatro dimensiones y cobertura. Incluir también carga asignada y restante registrada por persona frente a su capacidad cuando esos datos estén disponibles.

Dar después feedback individual breve con fortalezas observadas, mejoras específicas y próximos pasos bajo control de la persona. Enlazar tickets, commits o PR que sostengan cada punto. Explicar qué está implementado, qué falta y qué depende de otra entrega. Separar correcciones confirmadas de aspectos que siguen sin poder verificarse. Cualquier acción o decisión del PM debe surgir de los hallazgos.

Conservar informe y captura mínima en los directorios `reports_dir` y `state_dir` definidos por la tarea o configuración, si son escribibles, usando los nombres `developer-feedback-<fecha>.md` y `developer-feedback.json`. Si no se configuraron directorios, usar `pm/reports/` y `pm/state/` respecto del proyecto actual, sin duplicar segmentos. Identificar siempre el proyecto y alcance de la captura para no mezclar evaluaciones. Las programaciones pueden proporcionar rutas y parámetros específicos; no fijarlos en esta skill. La captura incluye sitio/proyecto, período/corte, alcance, mapa de identidades, criterios y pesos, notas por dimensión, exclusiones, cobertura, confianza, enlaces, bases y SHA, y cambios respecto del informe anterior. Preservar el informe anterior y diferenciar cortes del mismo día con la hora cuando corresponda.

Si falla una fuente, entregar la parte verificable y registrar la falla. Si el almacenamiento no es escribible, entregar igualmente la evaluación en el chat e indicar que no se guardó la copia local. La primera evaluación establece la base. La creación de la skill no programa evaluaciones periódicas.

## Ejemplo de uso

**Pedido:** Evaluá a cada desarrollador de este sprint con Jira y GitHub: nota de 0 a 10, con evidencia y feedback individual.
**Resultado:** Tabla por persona con nota, confianza, las cuatro dimensiones y cobertura, más fortalezas y mejoras enlazadas a tickets o PR. No publica la evaluación ni modifica Jira o GitHub.
