---
name: g10-jira-control-reaperturas
description: "Guía para configurar una automatización de Jira que identifica tickets reabiertos después de su finalización y registra situaciones de retrabajo."
metadata:
  tipo: skill
  area: [gestion, qa]
  fase: [revision, mantenimiento]
  tecnologias: [agnostico]
  metodologia: [kanban]
  herramientas: [otra]
  requiere: [jira]
  grupo: "10"
  autor:
    nombre: Azul Garber
    github: amgarber
  responsables: [amgarber]
  madurez: experimental
  relacionados:
  - g10-jira-pr-merged
---
# Control automático de tickets reabiertos

## Objetivo

Identificar tickets que regresan a una etapa de trabajo después de haber alcanzado el estado Finalizado.

La automatización facilita el seguimiento de retrabajo, incidencias detectadas después del cierre y tareas que requieren una nueva intervención del equipo.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre de la regla: Control de tickets reabiertos.
- Estado de origen: Finalizado.
- Estados de destino: cualquier estado distinto de Finalizado.
- Etiqueta utilizada: reabierto.

## Disparador

Utilizar:

`Work item transitioned`

Configurar:

- From status: Finalizado.
- To status: Any status.

Agregar una condición que verifique que el estado actual sea distinto de Finalizado, si fuera necesario.

## Acciones

### 1. Agregar etiqueta

Utilizar:

`Edit work item`

Agregar la etiqueta:

`reabierto`

La acción debe conservar las etiquetas existentes.

### 2. Registrar la reapertura

Utilizar:

`Comment on work item`

Comentario:

```text
🔄 Ticket reabierto

Estado anterior: {{fieldChange.fromString}}
Estado nuevo: {{fieldChange.toString}}
Modificado por: {{initiator.displayName}}
Fecha: {{now.format("dd/MM/yyyy HH:mm")}}

Se registra la reapertura para seguimiento de retrabajo.
```

## Configuración en Jira

1. Abrir el proyecto Conexia.
2. Acceder a Project settings > Automation.
3. Crear una regla con el disparador Work item transitioned.
4. Configurar Finalizado como estado de origen.
5. Agregar una condición para excluir Finalizado como destino, si corresponde.
6. Agregar la acción Edit work item.
7. Incorporar la etiqueta reabierto sin reemplazar las existentes.
8. Agregar la acción Comment on work item.
9. Configurar el comentario de reapertura.
10. Guardar y activar la regla.

## Requisitos

- Workflow que permita reabrir tickets.
- Permisos para editar etiquetas.
- Permisos para agregar comentarios.
- Acceso al historial de automatizaciones.

## Verificación

- Los tickets reabiertos reciben la etiqueta reabierto.
- Las etiquetas anteriores se conservan.
- Se agrega un comentario con información de la transición.
- Las transiciones entre otros estados no activan la regla.
- La ejecución queda registrada en el Audit log.

## Ejemplo de uso

**Pedido:** Identificá automáticamente los tickets de Conexia que vuelven a abrirse después de haber sido finalizados.

**Resultado:** Jira agrega la etiqueta reabierto y registra un comentario con el estado anterior, el nuevo estado, el usuario y la fecha de reapertura.
