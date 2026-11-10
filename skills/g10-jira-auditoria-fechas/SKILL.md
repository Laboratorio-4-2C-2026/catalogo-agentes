---
name: g10-jira-auditoria-fechas
description: "Guía para configurar una automatización de Jira que registra cambios en la fecha de vencimiento de los tickets y facilita la trazabilidad del cronograma."
metadata:
tipo: skill
area: [gestion]
fase: [planificacion, mantenimiento]
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
- g10-jira-asignacion-automatica
---

# Auditoría automática de cambios de fecha en Jira

## Objetivo

Establecer un mecanismo de auditoría de las modificaciones realizadas en las fechas de vencimiento de los tickets del proyecto Conexia.

La automatización permite conservar un registro de cambios del cronograma, identificar modificaciones durante la ejecución y facilitar el análisis de desvíos.

La regla utiliza Jira Automation y no requiere intervención de un agente de IA.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre de la regla: Auditoría de cambios de fecha.
- Campo monitoreado: Due date.
- Tipo: automatización basada en cambios de campo.

## Disparador

Utilizar el trigger:

`Field value changed`

Seleccionar el campo:

`Due date`

La regla se activa cuando cambia la fecha de vencimiento de un ticket.

## Acción

Agregar la acción:

`Comment on work item`

Configurar el siguiente comentario:

```text
📅 Cambio de fecha de vencimiento

Fecha anterior: {{fieldChange.fromString}}
Fecha nueva: {{fieldChange.toString}}
Modificado por: {{initiator.displayName}}

Registro automático para seguimiento del cronograma.
```

Las smart values permiten recuperar el valor anterior, el nuevo valor y el usuario que realizó el cambio.

## Configuración en Jira

1. Abrir el proyecto Conexia.
2. Acceder a Project settings > Automation.
3. Crear una regla con el disparador Field value changed.
4. Seleccionar el campo Due date.
5. Agregar la acción Comment on work item.
6. Introducir el comentario con las smart values.
7. Guardar y activar la regla.
8. Modificar la fecha de vencimiento de un ticket de prueba.
9. Revisar el comentario y el Audit log.

## Requisitos

- Campo Due date disponible.
- Permisos para agregar comentarios.
- Acceso a Jira Automation.
- Smart values compatibles con el evento de cambio de campo.

## Verificación

- Los cambios de fecha generan un comentario.
- Se registra la fecha anterior.
- Se registra la fecha nueva.
- Se identifica al usuario que realizó la modificación.
- Los cambios de otros campos no activan la regla.

## Ejemplo de uso

**Pedido:** Registrá automáticamente los cambios de fecha de vencimiento de los tickets de Conexia.

**Resultado:** La regla agrega un comentario al ticket con la fecha anterior, la nueva y el usuario que realizó el cambio, permitiendo mantener trazabilidad del cronograma.
