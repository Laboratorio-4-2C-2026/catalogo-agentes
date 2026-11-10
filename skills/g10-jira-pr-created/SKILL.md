---
name: g10-jira-pr-created
description: Guía para configurar y verificar una automatización de Jira que mueve un ticket a En revisión cuando se crea un Pull Request vinculado en GitHub.
metadata:
  tipo: skill
  grupo: "10"
tipo: skill
area:
- gestion
- devops
fase:
- desarrollo
- revision
tecnologias:
- git
metodologia:
- kanban
herramientas:
- otra
requiere:
- jira
- github
grupo: "10"
autor: null
nombre: Azul Garber
github: amgarber
responsables:
- amgarber
madurez: usado-en-proyecto
relacionados:
- g10-jira-branch-en-curso
- g10-jira-pr-merged
---
# Actualización automática del estado al crear un Pull Request

## Objetivo

Documentar y permitir reproducir la automatización utilizada en Conexia para actualizar el estado de los tickets de Jira cuando un desarrollador crea un Pull Request vinculado.

La automatización permite reflejar en el tablero que el trabajo fue enviado a revisión, sin necesidad de cambiar manualmente el estado del ticket.

Esta regla funciona mediante Jira Automation y la integración con GitHub. No utiliza un agente de IA.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre original: Pull Request Created.
- Evento: Pull request created.
- Estado de destino: En revisión.
- Integración: GitHub y Jira.

## Disparador

La regla utiliza el trigger:

`Pull request created`

Se ejecuta cuando Jira recibe el evento de creación de un Pull Request asociado a un ticket.

Para establecer la asociación, el Pull Request debe estar correctamente vinculado al ticket mediante la integración de desarrollo.

## Condiciones

La regla no tiene condiciones adicionales configuradas.

Por lo tanto, no verifica explícitamente el estado anterior del ticket antes de intentar la transición.

## Acción

La automatización utiliza:

`Transition the work item to`

Estado de destino:

`En revisión`

Esto permite que el tablero de Jira refleje el inicio de la etapa de revisión de código.

## Cómo reproducir la automatización

1. Abrir el proyecto en Jira Cloud.
2. Acceder a Project settings > Automation.
3. Crear una nueva regla.
4. Seleccionar el disparador Pull request created.
5. Agregar la acción Transition the work item.
6. Configurar En revisión como estado de destino.
7. Guardar y activar la automatización.
8. Crear un Pull Request vinculado a un ticket de prueba.
9. Revisar el estado del ticket y el Audit log.

## Requisitos

- El repositorio de GitHub debe estar conectado con Jira.
- El Pull Request debe estar vinculado al ticket correspondiente.
- El workflow debe permitir la transición hacia En revisión.
- La regla debe contar con permisos para modificar el estado del ticket.

## Verificación

Comprobar que:

- Crear un Pull Request vinculado dispara la automatización.
- El ticket pasa a En revisión cuando la transición está permitida.
- La regla no se dispara por la creación de una branch sin Pull Request.
- Los errores de integración o transición quedan registrados en el Audit log.

## Consideraciones

Como no existe una condición que limite el estado de origen, la automatización puede intentar mover tickets que todavía no están listos para revisión.

Si el workflow no permite la transición desde el estado actual, la ejecución puede fallar.

Una posible mejora futura sería agregar una condición para ejecutar la transición únicamente cuando el ticket esté En curso.

Esta mejora no forma parte de la configuración original documentada.

## Ejemplo de uso

**Pedido:** Configurá Jira para que los tickets de Conexia pasen automáticamente a En revisión cuando un desarrollador abra un Pull Request asociado.

**Resultado:** La guía indica cómo crear una regla con el disparador Pull request created y la acción de transición a En revisión. Jira ejecuta la transición cuando recibe el evento y el workflow lo permite.
