---
name: g12-actualizar-cronograma
description: Prepara o aplica una actualización del cronograma de un proyecto comparando línea base, ejecución real y plan futuro en su herramienta de planificación, con evidencia por cambio. Usar al hacer un corte de avance, al reprogramar trabajo o antes de un steering.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g04-cronograma
---

# Actualizar cronograma

Actualizar el plan conservando la comparación con lo que se había comprometido.
Ejemplo: `/actualizar-cronograma corte al 5 de noviembre de 2026`.

## Fuente y alcance

Identificar en la documentación o con el usuario la fuente autorizada del cronograma,
la línea base aprobada y la herramienta donde se mantiene el plan vigente. Puede ser
una planilla, un gestor de proyectos o un archivo. Consultar su esquema y las decisiones
aplicables antes de interpretar campos o escribir. Los backups fechados son evidencia
histórica, no el estado actual.

Distinguir el tracker de tareas de la autoridad del cronograma. Si se usan varias
herramientas, seguir la regla de precedencia y sincronización del equipo. Ante fuentes
incompatibles sin autoridad definida, mostrar la diferencia y preguntar cuál gobierna
antes de aplicar cambios; se puede avanzar con la comparación provisional.

Determinar fecha de corte, hitos afectados y horizonte. Si no hay acceso a la fuente vigente,
entregar una propuesta basada en las fuentes disponibles con su fecha y faltantes;
no presentarla como lectura actual ni afirmar que quedó actualizado.

## Comparación

Por historia o tarea, distinguir: inicio/fin de línea base, inicio/fin real cuando
existan, inicio/fin proyectado para el remanente, estado, dependencias y fuente.
Inspeccionar cómo representa esas fechas la herramienta antes de usar sus campos.

- Mantener la línea base al reprogramar. Trabajo nuevo lleva la base definida por la
  decisión que lo incorporó, sin retrofechar compromisos.
- Una fecha de merge demuestra integración; no prueba por sí sola inicio, aceptación
  funcional ni puesta en producción. Usar la evidencia exigida para ese hito.
- Marcar fechas reales sólo con evidencia. Las fechas futuras son proyecciones.
- Tratar explícitamente trabajo parcial y bloqueos. Calcular el plan restante según
  capacidad y dependencias confirmadas; exponer supuestos cuando falten.
- Conservar los hitos comprometidos. Si el plan ya no llega, mostrar la brecha y las
  opciones de decisión, sin mover la entrega silenciosamente.
- Evitar sumar épicas y tareas como trabajo independiente. Aplicar la convención
  vigente para filas agrupadoras y fechas de épicas.

Entregar el impacto por hito, tareas en riesgo y diferencias de fechas. Expresar atrasos
con calendario explícito; no inventar feriados ni ruta crítica sin dependencias y duraciones.

## Propuesta o aplicación

Preparar una tabla con ítem, campo, valor actual, valor propuesto, motivo y fuente.
Si el pedido es analizar o mostrar cambios, terminar con esa propuesta. Si incluye
actualizar el cronograma, aplicar sólo los cambios sustentados y dentro del alcance.
Las decisiones nuevas de alcance, capacidad o fechas comprometidas quedan pendientes
hasta que las tome el responsable correspondiente.

Antes de una escritura autorizada, guardar un snapshot fechado del estado afectado en
una ubicación permitida. Volver a leer los valores a cambiar; si cambiaron desde la
comparación, reconciliar antes de escribir. Verificar por lectura cada campo actualizado.
Si una escritura falla, informar qué se aplicó y qué quedó pendiente; no repetir cambios
ya confirmados. Respetar las restricciones de escritura de los repositorios y archivos de destino.

## Entrega

Mostrar comparación base/real/proyección, efecto sobre hitos, cambios propuestos o
aplicados, fuentes y pendientes. Agregar un Gantt cuando ayude a ver la diferencia,
usando estilos y leyenda distintos para las tres series. Comprobar inicio ≤ fin,
consistencia con dependencias y que un trabajo pendiente no figure como terminado.

## Ejemplo de uso

**Pedido:** /actualizar-cronograma corte al 5 de noviembre de 2026

**Resultado:** Devuelve por tarea la comparación entre línea base, fechas reales y proyección, el efecto sobre cada hito y una tabla de cambios propuestos con su fuente; solo los aplica si el pedido lo incluye, guardando antes un snapshot.
