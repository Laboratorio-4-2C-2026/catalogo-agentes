---
name: g10-jira-notificaciones
description: Guía para configurar una automatización de Jira que envía recordatorios por correo sobre tickets asignados que vencen al día siguiente y todavía no están finalizados.
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
madurez: usado-en-proyecto
relacionados:
- g10-jira-asignacion-automatica
---
# Recordatorios automáticos de vencimiento en Jira

## Objetivo

Documentar y permitir reproducir la automatización utilizada en Conexia para enviar recordatorios de tickets que vencen al día siguiente y aún no están finalizados.

La regla funciona mediante Jira Automation, sin intervención de un agente de IA.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre original: Notifications.
- Tipo: automatización programada.
- Frecuencia: todos los días a las 13:00.
- Canal de notificación: correo electrónico.

## Disparador

La automatización utiliza el trigger `Scheduled`, configurado para ejecutarse diariamente a las 13:00.

La consulta JQL asociada es:

```jql
duedate = startOfDay("+1d") AND status != "Finalizado" AND assignee IS NOT EMPTY
```

### Condiciones del filtro

La consulta selecciona tickets que cumplen simultáneamente:

1. Su fecha de vencimiento es mañana.
2. Su estado es distinto de Finalizado.
3. Tienen un responsable asignado.

Los tickets que no cumplen estas condiciones quedan fuera de la ejecución.

## Acción

La automatización utiliza la acción `Send email`.

El destinatario es una dirección de correo fija configurada en la regla.

### Asunto

`⏰ Recordatorio: {{issue.key}} vence mañana`

La expresión `{{issue.key}}` es una smart value de Jira que se reemplaza por la clave del ticket procesado.

El contenido completo del cuerpo del correo depende de la configuración de la acción.

## Cómo reproducir la automatización

1. Abrir el proyecto en Jira Cloud.
2. Acceder a Project settings > Automation.
3. Crear una regla con el trigger Scheduled.
4. Configurar su ejecución diaria a las 13:00.
5. Habilitar la ejecución sobre tickets seleccionados mediante JQL.
6. Introducir la consulta JQL indicada.
7. Agregar la acción Send email.
8. Configurar el destinatario y el asunto con la smart value del ticket.
9. Completar el cuerpo del correo según las necesidades del proyecto.
10. Guardar, activar y verificar la regla mediante el Audit log.

## Requisitos y consideraciones

- Los tickets deben tener una fecha de vencimiento configurada.
- La consulta utiliza el estado Finalizado como referencia.
- Jira debe disponer de permisos y configuración para enviar correos.
- El horario de ejecución depende de la zona horaria configurada.
- El destinatario actual es fijo; no se obtiene automáticamente del campo Assignee.

## Verificación

Comprobar que:

- Un ticket que vence mañana y no está finalizado es seleccionado.
- Un ticket finalizado queda excluido.
- Un ticket sin responsable queda excluido.
- Un ticket con vencimiento en otra fecha no es seleccionado.
- El correo contiene la clave correcta del ticket.
- La ejecución queda registrada en el Audit log.

## Ejemplo de uso

**Pedido:** Configurá un recordatorio automático en Jira para detectar tickets de Conexia que vencen mañana y todavía no están finalizados.

**Resultado:** La guía permite configurar una ejecución diaria a las 13:00 que filtra los tickets por vencimiento, estado y responsable, y envía un correo con la clave de cada ticket seleccionado.
