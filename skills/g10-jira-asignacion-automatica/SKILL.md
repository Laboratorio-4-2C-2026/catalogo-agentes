---
name: g10-jira-asignacion-automatica
description: "Guía para configurar y verificar una automatización programada de Jira que asigna tickets desde el campo Dev planificado y los mueve de Backlog a Por hacer cuando llega su fecha de inicio."
metadata:
  tipo: skill
  area: [gestion]
  fase: [planificacion, desarrollo]
  tecnologias: [agnostico]
  metodologia: [kanban]
  herramientas: [otra]
  requiere: [jira]
  grupo: "10"
  autor:
    nombre: Azul Garber
    github: amgarber
  responsables: [amgarber]
  madurez: usado-en-proyecto
  relacionados: []
---
# Asignación automática de tickets desde Backlog

## Objetivo

Documentar y permitir reproducir la automatización utilizada en el proyecto Conexia para asignar tickets a sus desarrolladores y moverlos automáticamente desde Backlog a Por hacer cuando llega la fecha de inicio planificada.

Esta skill funciona como guía de configuración y verificación. La automatización real se ejecuta mediante Jira Automation, sin intervención de un agente de IA.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Tipo: automatización programada.
- Nombre original: Automation from backlog.
- Frecuencia: todos los días a las 13:30.
- Campo personalizado utilizado: Dev planificado.
- Estado inicial: Backlog.
- Estado destino: Por hacer.

## Disparador

La regla utiliza el trigger `Scheduled`, configurado para ejecutarse diariamente a las 13:30.

La consulta JQL asociada es:

```jql
status = "Backlog" AND "Start date" <= startOfDay()
```

Esta consulta selecciona tickets que:

1. Se encuentran en estado Backlog.
2. Tienen una fecha de inicio igual o anterior al día actual.

Los tickets con fecha de inicio futura no cumplen la condición.

## Acciones

### 1. Asignar el ticket

La acción `Assign the work item to` utiliza el campo personalizado `Dev planificado`.

Valor configurado en Jira:

```text
{{issue.Dev planificado.accountId}}
```

Esto permite asignar el ticket al desarrollador seleccionado previamente durante la planificación.

### 2. Cambiar el estado

La acción `Transition the work item to` mueve el ticket al estado:

```text
Por hacer
```

## Cómo reproducir la automatización

1. Abrir Jira y acceder al proyecto correspondiente.
2. Entrar en Project settings > Automation.
3. Crear una regla con disparador Scheduled.
4. Configurar la ejecución diaria a las 13:30.
5. Habilitar la ejecución sobre tickets obtenidos mediante JQL.
6. Introducir la consulta JQL indicada.
7. Agregar la acción de asignación utilizando el accountId del campo Dev planificado.
8. Agregar la transición al estado Por hacer.
9. Guardar y activar la regla.
10. Revisar el Audit log para verificar las ejecuciones.

## Requisitos y consideraciones

- El proyecto debe disponer del campo personalizado Dev planificado.
- El campo debe contener un usuario válido de Jira.
- La automatización necesita permisos para asignar tickets y ejecutar la transición.
- La transición hacia Por hacer debe estar disponible en el workflow.
- La hora de ejecución debe verificarse según la zona horaria configurada en Jira.

## Verificación

Comprobar que:

- Los tickets con fecha de inicio futura permanecen en Backlog.
- Los tickets elegibles se asignan al desarrollador planificado.
- Los tickets procesados pasan a Por hacer.
- El Audit log permite identificar errores de asignación o transición.

## Ejemplo de uso

**Pedido:** Configurá una automatización de Jira para que los tickets de Conexia se asignen automáticamente al desarrollador planificado cuando llegue su fecha de inicio.

**Resultado:** La guía indica cómo configurar una regla diaria que filtra tickets de Backlog por fecha de inicio, obtiene el accountId de Dev planificado y los mueve a Por hacer. La ejecución automática queda a cargo de Jira.
