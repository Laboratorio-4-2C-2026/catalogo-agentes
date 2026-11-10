---
name: g10-jira-branch-en-curso
description: "Guía para configurar una automatización de Jira que mueve un ticket de Por hacer a En curso al crear una branch."
metadata:
tipo: skill
area: [gestion, devops]
fase: [desarrollo]
tecnologias: [git]
metodologia: [kanban]
herramientas: [otra]
requiere: [jira, github]
grupo: "10"
autor:
nombre: Azul Garber
github: amgarber
responsables: [amgarber]
madurez: usado-en-proyecto
relacionados:
- g10-jira-asignacion-automatica
---

# Branch created → En curso

# Actualización automática del estado al crear una branch

## Objetivo

Documentar y permitir reproducir la automatización de Jira utilizada en Conexia para actualizar el estado de un ticket cuando comienza su desarrollo mediante la creación de una rama vinculada.

La regla se ejecuta de forma nativa en Jira Automation. Esta skill describe su configuración y verificación; no ejecuta cambios por sí misma.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Integración: repositorio Git conectado a Jira.
- Nombre original: Branch created → En curso.
- Estado de origen: Por hacer.
- Estado de destino: En curso.

## Disparador

La automatización utiliza el trigger:

`Branch created`

Se activa cuando Jira recibe un evento de creación de rama asociado a un ticket.

## Condición

La regla comprueba que el ticket se encuentre en el estado:

`Por hacer`

Si el ticket está en otro estado, la transición no se ejecuta.

Esta condición evita modificar tickets que ya están en curso, en revisión o finalizados.

## Acción

La acción `Transition the work item to` cambia el estado del ticket a:

`En curso`

Esto permite reflejar el inicio del desarrollo en el tablero de Jira.

## Cómo reproducir la automatización

1. Abrir Jira y acceder al proyecto.
2. Entrar en Project settings > Automation.
3. Crear una nueva regla.
4. Seleccionar el disparador Branch created.
5. Agregar una condición de estado.
6. Configurar la condición para que el estado sea Por hacer.
7. Agregar la acción Transition the work item.
8. Seleccionar En curso como estado de destino.
9. Guardar y activar la regla.
10. Verificar su funcionamiento mediante el Audit log.

## Requisitos

- El repositorio de código debe estar conectado con Jira.
- La rama creada debe estar vinculada al ticket correspondiente.
- El workflow debe permitir la transición de Por hacer a En curso.
- La regla debe disponer de los permisos necesarios.

## Verificación

Comprobar que:

- Crear una rama vinculada a un ticket en Por hacer provoca la transición a En curso.
- Los tickets en otros estados no se modifican.
- La ejecución queda registrada en el Audit log.
- Si la integración o transición falla, el error puede identificarse en el historial.

## Ejemplo de uso

**Pedido:** Configurá Jira para que un ticket pase automáticamente a En curso cuando un desarrollador cree una branch asociada a ese ticket.

**Resultado:** La guía indica cómo configurar el disparador Branch created, restringir la ejecución a tickets en Por hacer y realizar la transición a En curso. Jira ejecuta la automatización cuando recibe el evento correspondiente.
