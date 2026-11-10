---
name: g10-jira-cambios-alcance
description: "Guía para configurar una automatización de Jira que identifica tickets creados después de una fecha de corte y los marca para revisar posibles cambios de alcance."
metadata:
  tipo: skill
  area: [gestion]
  fase: [planificacion, analisis]
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
# Identificación automática de posibles cambios de alcance

## Objetivo

Identificar tickets incorporados al proyecto Conexia después de una fecha de corte de planificación.

La automatización permite distinguir trabajo agregado posteriormente y facilita su análisis como posible cambio de alcance.

La creación de un ticket después de la fecha de corte no implica automáticamente que el cambio haya sido aprobado.

## Contexto

- Proyecto: Conexia.
- Plataforma: Jira Cloud.
- Nombre de la regla: Registro de cambios de alcance.
- Evento: creación de un ticket.
- Etiqueta utilizada: alcance-agregado.
- Fecha de corte: configurable según la planificación.

## Disparador

Utilizar:

`Work item created`

La regla se activa cuando se crea un ticket dentro del proyecto.

## Condición

Agregar una condición de comparación avanzada:

Primer valor:

```text
{{issue.created}}
```

Operador:

`Greater than`

Segundo valor de ejemplo:

```text
2026-10-01T00:00:00.000Z
```

La fecha debe ajustarse al corte de planificación acordado por el equipo.

Es necesario verificar el formato y la zona horaria utilizados en la comparación.

## Acciones

### 1. Agregar etiqueta

Utilizar:

`Edit work item`

Agregar:

`alcance-agregado`

Conservar las etiquetas existentes.

### 2. Registrar comentario

Utilizar:

`Comment on work item`

Comentario:

```text
📌 Posible cambio de alcance

Ticket creado después de la fecha de corte de planificación.

Fecha de creación: {{issue.created.format("dd/MM/yyyy HH:mm")}}
Creado por: {{issue.reporter.displayName}}

Requiere revisión para determinar si corresponde a trabajo adicional al alcance original.
```

## Configuración en Jira

1. Abrir el proyecto Conexia.
2. Acceder a Project settings > Automation.
3. Crear una regla con el disparador Work item created.
4. Agregar una condición de comparación avanzada.
5. Comparar la fecha de creación con la fecha de corte.
6. Agregar la acción Edit work item.
7. Incorporar la etiqueta alcance-agregado.
8. Agregar la acción Comment on work item.
9. Configurar el mensaje de revisión.
10. Guardar y activar la regla.

## Requisitos

- Fecha de corte de planificación definida.
- Permisos para editar tickets.
- Permisos para agregar comentarios.
- Validación del formato de fechas y zona horaria.

## Verificación

- Los tickets posteriores a la fecha de corte reciben la etiqueta.
- Los tickets anteriores quedan excluidos.
- Se conservan las etiquetas existentes.
- Se registra el comentario de revisión.
- La regla no clasifica automáticamente el cambio como aprobado.

## Ejemplo de uso

**Pedido:** Identificá los tickets de Conexia creados después del cierre de la planificación inicial.

**Resultado:** Jira marca los tickets con la etiqueta alcance-agregado y registra un comentario para que el equipo evalúe si representan una modificación del alcance original.
