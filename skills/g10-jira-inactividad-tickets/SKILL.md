---
name: g10-jira-inactividad-tickets
description: Guía para configurar una automatización de Jira que detecta tickets En curso sin actualizaciones durante cinco días y registra una alerta de seguimiento.
metadata:
  tipo: skill
  grupo: "10"
tipo: skill
area:
- gestion
fase:
- desarrollo
- mantenimiento
tecnologias:
- agnostico
metodologia:
- kanban
herramientas:
- otra
requiere:
- jira
grupo: "10"
autor: null
nombre: Azul Garber
github: amgarber
responsables:
- amgarber
madurez: experimental
relacionados:
- g10-jira-branch-en-curso
---
# Detección automática de tickets sin actividad

## Objetivo

Identificar tickets que permanecen En curso sin registrar actualizaciones durante cinco días.

La automatización facilita el seguimiento de tareas potencialmente estancadas y permite detectar situaciones que requieren revisión del equipo.

La ausencia de actualizaciones en Jira no significa necesariamente que no exista trabajo realizado fuera de la plataforma.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre de la regla: Alerta de tareas sin actividad.
- Estado monitoreado: En curso.
- Umbral: cinco días sin actualizaciones.
- Frecuencia: diaria.
- Etiqueta de control: inactividad-detectada.

## Disparador

Utilizar:

`Scheduled`

Configurar una ejecución diaria a las 10:00.

### Filtro JQL

```jql
project = KAN AND status = "En curso" AND updated <= -5d AND (labels NOT IN ("inactividad-detectada") OR labels IS EMPTY)
```

La consulta selecciona tickets que:

1. Pertenecen al proyecto KAN.
2. Están En curso.
3. No registran actualizaciones durante al menos cinco días.
4. No tienen la etiqueta inactividad-detectada.

## Acciones

### 1. Registrar comentario

Utilizar:

`Comment on work item`

Comentario:

```text
⚠️ Alerta de inactividad

Este ticket permanece En curso y no registra actualizaciones desde hace al menos cinco días.

Responsable: {{issue.assignee.displayName}}
Última actualización: {{issue.updated.format("dd/MM/yyyy HH:mm")}}

Se recomienda revisar el avance y actualizar el ticket si corresponde.
```

### 2. Agregar etiqueta

Utilizar:

`Edit work item`

Agregar:

`inactividad-detectada`

Conservar las etiquetas existentes.

## Configuración en Jira

1. Abrir el proyecto Conexia.
2. Acceder a Project settings > Automation.
3. Crear una regla con el disparador Scheduled.
4. Configurar la ejecución diaria a las 10:00.
5. Habilitar la ejecución sobre tickets seleccionados mediante JQL.
6. Introducir el filtro JQL indicado.
7. Agregar la acción Comment on work item.
8. Configurar el mensaje de alerta.
9. Agregar la acción Edit work item.
10. Incorporar la etiqueta inactividad-detectada.
11. Guardar y activar la regla.

## Requisitos

- Permisos para consultar tickets.
- Permisos para agregar comentarios.
- Permisos para editar etiquetas.
- Campo Updated disponible en Jira.
- Workflow con estado En curso.

## Consideraciones

La automatización utiliza la fecha de última actualización del ticket como indicador de actividad.

La etiqueta evita generar comentarios repetidos mientras permanezca aplicada.

Para permitir futuras alertas después de una nueva etapa de actividad, se puede crear una regla complementaria que elimine la etiqueta cuando corresponda.

## Verificación

- Los tickets En curso sin actualizaciones durante cinco días son seleccionados.
- Los tickets actualizados recientemente quedan excluidos.
- Los tickets en otros estados no son seleccionados.
- Se registra el comentario de seguimiento.
- Se agrega la etiqueta inactividad-detectada.
- No se generan alertas diarias repetidas sobre tickets ya etiquetados.

## Ejemplo de uso

**Pedido:** Detectá tareas de Conexia que llevan cinco días En curso sin actualizaciones.

**Resultado:** Jira identifica los tickets mediante JQL, agrega un comentario de seguimiento y los marca con una etiqueta para evitar notificaciones repetidas.
