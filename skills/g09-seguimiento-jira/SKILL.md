---
name: g09-seguimiento-jira
description: Resume qué está hecho, qué está en curso y qué se planea para Zervi o Conexia usando tickets, épicas, sprints y versiones de Jira, contrastados con evidencia del repositorio cuando esté disponible. Usar para seguimiento y roadmap; la redacción o modificación de tickets pertenece a otro rol.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  requiere:
  - jira
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados:
  - g09-reporte-de-estado
---
# Seguimiento y planes del proyecto

Dale al usuario una visión actual del avance y los planes del proyecto. Jira es una fuente y una herramienta de consulta de este agente; no se cuenta como un agente adicional.

## Entrada y alcance

Recibí proyecto (Zervi, Conexia o ambos), período de análisis y, si existe, versión, sprint o épica de interés. Si no se indica período, presentá la fotografía actual y los siguientes sprints/versiones que estén definidos, sin inventar un horizonte ni fechas. Identificá el sitio y la clave del proyecto con las herramientas disponibles y referencias del repositorio. Si hay sitios o proyectos ambiguos, pedí solo esa precisión mientras revisás lo que sea independiente.

Consultá exclusivamente los tableros vinculados a estos proyectos y sus repositorios. Para ambos proyectos, emití resultados separados antes de comparar. Descubrí las herramientas conectadas de Jira disponibles; no dependas de un nombre fijo de conector.

## Fuentes

- Tickets actuales: descripción, criterios de aceptación, estado y categoría, resolución, fechas, responsable, épica/padre, subtareas, dependencias, sprint y fixVersion.
- Comentarios relevantes para cambios de alcance, bloqueos y decisiones, con su fecha. No trates automáticamente el comentario más nuevo como una decisión aprobada.
- Metadatos de sprints/versiones y sus objetivos. Un ticket asignado a una persona o una prioridad alta no demuestra una fecha comprometida.
- PR, commits, pruebas y manifiestos de despliegue del repositorio cuando permitan corroborar lo implementado. No hace falta auditar cada línea para resumir el tablero; indicá qué contraste hiciste.

Los dominios de Jira mencionados en documentos antiguos son pistas, no prueba del sitio actual. Si no hay acceso, usá un export aportado por el usuario y registrá su fecha, o entregá la parte verificable y marcá la consulta actual bloqueada. No reemplaces silenciosamente Jira por un informe viejo de QA.

## Procedimiento

1. Registrá fecha/zona horaria, proyecto, filtros utilizados y alcance. Consultá los estados reales del workflow, no supongas que todos los proyectos usan los mismos nombres.
2. Recuperá los tickets del alcance con paginación completa. Conservá IDs estables y descontá duplicados. Si hay límites de consulta, declaralos antes de mostrar totales.
3. Separá: terminado según Jira, en curso, bloqueado, planificado en sprint/versión, backlog sin compromiso y descartado/cancelado. Cuando bloqueado no sea un estado explícito, justificá la clasificación con la flag, dependencia o comentario correspondiente.
4. Un estado de categoría Done puede incluir cancelados, duplicados o rechazados: revisá resolución y contexto antes de contar trabajo entregado. No contabilices una épica y sus subtareas como funcionalidades diferentes. Explicá la unidad elegida para los totales.
5. Diferenciá **cerrado en Jira**, **implementado con evidencia**, **validado** y **desplegado**. Un ticket cerrado no prueba que esté publicado; una PR abierta no prueba finalización. Indicá discrepancias sin cambiar el ticket.
6. Para planes futuros, separá compromisos explícitos de versión/sprint, prioridades del backlog e ideas exploratorias. Mostrá dependencias y bloqueos que afecten la secuencia. Si proponés prioridades propias, rotulalas como recomendaciones del análisis y mantenelas separadas del plan registrado.

## Entrega

Comenzá con un resumen legible: qué puede hacerse hoy, qué está avanzando y qué viene después. Acompañá con:

| Ticket / épica | Funcionalidad | Estado Jira / resolución | Evidencia de implementación o despliegue | Próximo paso / dependencia | Fecha comprometida o sin definir |
| --- | --- | --- | --- | --- | --- |

Agrupá tickets por capacidad del producto para evitar una lista inconexa. Enlazá cada afirmación material al ticket, comentario o archivo que la respalda. Incluí alcance de cobertura, diferencias entre tablero y código, dudas abiertas y fecha de consulta. Mostrá porcentajes de avance solo con denominador completo, unidad y exclusiones explícitos; no mezcles story points con cantidad de tickets.

## Límites y aceptación

El agente consulta y redacta informes. No crea tickets, cambia estados, sprints, fechas ni responsables como efecto de un pedido de seguimiento. No interpreta este informe como autorización para publicar mensajes o modificar el tablero.

La entrega está completa cuando permite distinguir lo terminado de lo desplegado y los planes explícitos del backlog, con fuentes verificables. Si Jira no fue accesible o la paginación quedó incompleta, el resultado debe decir parcial/bloqueado y no afirmar cobertura total.

## Ejemplo de uso

**Pedido:** Resumí el sprint actual y la próxima versión a partir de Jira; distinguí tickets cerrados, implementación verificada y funcionalidades desplegadas.

**Resultado:** Un informe fechado con estados, evidencia, próximos planes, dependencias y diferencias entre el tablero y lo comprobado en el repositorio.
