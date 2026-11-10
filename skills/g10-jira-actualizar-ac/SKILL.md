---
name: g10-jira-actualizar-ac
description: "Guía para configurar una automatización de Jira que envía horas registradas y estimaciones de subtareas a Google Apps Script mediante una solicitud HTTP POST para apoyar el análisis de valor ganado."
metadata:
tipo: skill
area: [gestion, datos]
fase: [analisis, mantenimiento]
tecnologias: [agnostico]
metodologia: [kanban]
herramientas: [otra]
requiere: [jira, google-sheets]
grupo: "10"
autor:
nombre: Azul Garber
github: amgarber
responsables: [amgarber]
madurez: experimental
relacionados:
- g10-jira-asignacion-automatica
---

# Envío automático de horas trabajadas para valor ganado

## Objetivo

Documentar y permitir reproducir la automatización utilizada en Conexia para enviar información de tiempos registrados en Jira a un endpoint de Google Apps Script.

Esta integración está orientada a facilitar el análisis de valor ganado (VAN), especialmente el seguimiento del esfuerzo real registrado en las subtareas.

La regla se ejecuta mediante Jira Automation y no utiliza un agente de IA.

## Contexto

- Proyecto: Conexia.
- Clave del proyecto: KAN.
- Plataforma: Jira Cloud.
- Nombre original: [VAN] Actualizar AC desde Time Spent.
- Frecuencia: diariamente a las 12:30.
- Método HTTP: POST.
- Destino: endpoint de Google Apps Script.
- Steering configurado: 3.

## Disparador

La regla utiliza `Scheduled` y se ejecuta diariamente a las 12:30.

### Filtro JQL

```jql
project = KAN AND issuetype = Subtask AND "Start date" >= "2026-10-16"
```

La consulta selecciona las subtareas del proyecto KAN cuya fecha de inicio sea igual o posterior al 16 de octubre de 2026.

## Acción

La regla utiliza `Send web request` con método HTTP `POST`.

El destino es una URL de despliegue de Google Apps Script, que debe configurarse en Jira.

No se incluye la URL completa en esta documentación para evitar exponer un endpoint operativo.

### Cuerpo de la solicitud

```json
{
  "issueKey": "{{issue.key}}",
  "timeSpentSeconds": "{{issue.timetracking.timeSpentSeconds}}",
  "originalEstimateSeconds": "{{issue.timetracking.originalEstimateSeconds}}",
  "assignee": "{{issue.assignee.displayName}}",
  "epic": "{{issue.parent.summary}}",
  "steering": 3
}
```

Las expresiones entre llaves son smart values de Jira, que se resuelven al procesar cada subtarea.

### Datos enviados

- `issueKey`: identificador de la subtarea.
- `timeSpentSeconds`: tiempo registrado, en segundos.
- `originalEstimateSeconds`: estimación original, en segundos.
- `assignee`: nombre visible del responsable.
- `epic`: resumen del elemento padre inmediato.
- `steering`: identificador fijo con valor 3.

## Cómo reproducir la automatización

1. Abrir el proyecto en Jira Cloud.
2. Acceder a Project settings > Automation.
3. Crear una regla con el disparador Scheduled.
4. Configurar la ejecución diaria a las 12:30.
5. Habilitar la ejecución sobre tickets seleccionados mediante JQL.
6. Introducir la consulta JQL indicada.
7. Agregar la acción Send web request.
8. Seleccionar el método POST.
9. Configurar la URL del despliegue de Google Apps Script.
10. Configurar el cuerpo JSON con las smart values.
11. Verificar el tipo de contenido y la configuración HTTP requerida por el endpoint.
12. Guardar y activar la automatización.
13. Revisar el Audit log y comprobar la recepción de datos en el sistema de destino.

## Requisitos

- Acceso a Jira Automation.
- Permisos para consultar las subtareas y sus registros de tiempo.
- Un endpoint de Google Apps Script preparado para recibir solicitudes POST.
- Configuración adecuada de permisos y acceso al endpoint.
- Datos de seguimiento de tiempo disponibles en Jira.

## Consideraciones

El valor `steering` está fijado en 3 y no cambia automáticamente.

El campo `epic` obtiene el resumen del padre inmediato, por lo que su nombre no garantiza que el elemento sea una épica.

La regla envía datos al endpoint, pero la actualización efectiva de la planilla depende de la implementación de Google Apps Script.

Como la automatización se ejecuta diariamente, el sistema receptor debe contemplar la posibilidad de recibir varias veces información de una misma subtarea.

## Verificación

Comprobar que:

- El filtro selecciona las subtareas esperadas.
- La solicitud POST contiene las claves y valores correspondientes.
- Las smart values se resuelven correctamente.
- El endpoint responde sin errores.
- Los datos recibidos se reflejan correctamente en el sistema de destino.
- El Audit log permite identificar fallas de ejecución.

## Ejemplo de uso

**Pedido:** Configurá una automatización de Jira para enviar diariamente las horas trabajadas y estimaciones de las subtareas de Conexia a Google Apps Script para el seguimiento del valor ganado.

**Resultado:** La guía permite configurar una ejecución programada que selecciona subtareas mediante JQL y envía un JSON con identificador, tiempo registrado, estimación, responsable, padre y steering. El procesamiento posterior depende del script receptor.
