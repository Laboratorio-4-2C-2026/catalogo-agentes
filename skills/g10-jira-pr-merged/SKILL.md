---
name: g10-jira-pr-merged
description: "Guía para configurar una automatización de Jira que finaliza tickets en revisión cuando se fusiona un Pull Request vinculado."
metadata:
  tipo: skill
  area: [gestion, devops]
  fase: [revision, desarrollo]
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
  - g10-jira-branch-en-curso
---
# Finalización automática de tickets al fusionar un Pull Request

## Objetivo

Documentar y permitir reproducir la automatización utilizada en Conexia para actualizar el estado de los tickets de Jira cuando se fusiona un Pull Request asociado.

La regla funciona mediante Jira Automation y la integración con el repositorio de código. No requiere intervención de un agente de IA.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre original: PR Merged.
- Evento: Pull request merged.
- Estado de origen: En revisión.
- Estado de destino: Finalizado.

## Disparador

La automatización utiliza el trigger:

`Pull request merged`

Este evento se recibe cuando se fusiona un Pull Request asociado a un ticket de Jira.

## Condición

La regla verifica que el ticket esté en el estado:

`En revisión`

Si el ticket se encuentra en otro estado, la automatización no ejecuta la transición.

Esta condición evita modificar tickets que todavía no ingresaron a revisión o que ya están finalizados.

## Acción

La acción `Transition the work item to` cambia el estado del ticket a:

`Finalizado`

De esta manera, Jira refleja el cierre del trabajo asociado al Pull Request fusionado.

## Cómo reproducir la automatización

1. Abrir el proyecto en Jira Cloud.
2. Acceder a Project settings > Automation.
3. Crear una nueva regla.
4. Seleccionar el trigger Pull request merged.
5. Agregar una condición de estado.
6. Configurar la condición para que el estado sea En revisión.
7. Agregar la acción Transition the work item.
8. Seleccionar Finalizado como estado de destino.
9. Guardar y activar la regla.
10. Verificar la ejecución mediante el Audit log.

## Requisitos

- El repositorio de GitHub debe estar integrado con Jira.
- El Pull Request debe estar asociado al ticket correspondiente.
- El workflow debe permitir la transición de En revisión a Finalizado.
- La regla debe tener permisos para realizar la transición.

## Verificación

Comprobar que:

- Al fusionar un PR vinculado a un ticket en revisión, el ticket pasa a Finalizado.
- Los tickets en otros estados no cambian.
- Los PR que todavía están abiertos no disparan esta regla.
- La ejecución aparece en el Audit log.

## Ejemplo de uso

**Pedido:** Configurá Jira para que un ticket de Conexia pase automáticamente a Finalizado cuando se haga merge de su Pull Request y el ticket esté En revisión.

**Resultado:** La guía permite configurar el evento Pull request merged, la condición En revisión y la transición a Finalizado. Jira ejecuta la regla cuando recibe el evento de merge.
