---
name: g14-redactor-de-tickets-ejecutables
description: "Crea y desglosa tareas del cronograma en tickets ejecutables de 1 a 3 h con estructura fija (guía de implementación, cómo probarlo, criterios atómicos, DoD y alcance). Usala al bajar un hito a tickets; su revisión de un ticket existente se limita a estructura, tamaño y criterios atómicos, y no traduce para Jira ni hace la revisión final del lote."
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-traductor-de-tickets-para-jira
  - g09-redactar-tickets-tecnicos
  - g11-redactar-ticket
  - g03-planify-jira-ticket
---

# Redactor de tickets ejecutables

Convierte una tarea del cronograma en tickets que un dev pueda tomar y ejecutar sin volver a preguntar.

## El principio

**Un ticket es una guía técnica accionable, nunca un contrato declarativo abstracto.**

La razón es aritmética, no estética: hay 180 h de desarrollo contra 240 de dirección, con dos devs a 6 h semanales. Toda hora que un dev gasta en decidir en vez de construir sale del camino crítico. Un ticket que llega con contexto, decisiones ya tomadas y criterios verificables vale el doble que uno que llega con un título.

## La estructura, obligatoria

1. **Ficha y relaciones** — ID, épica, padre, sprint, carril, estimación con triplete, prioridad, y `Depende de` / `Bloquea` / `Relacionado`. Las precondiciones que Jira no modela van en prosa acá.
2. **Qué hay que hacer** — archivos y rutas a tocar, el mecanismo técnico concreto (trigger, hook, consulta, contrato de payload o props), la lógica a implementar, y **qué NO hacer**, que es lo que frena el scope creep.
3. **Cómo probarlo localmente** — comandos de consola reales, flujo de navegación o de datos, y las consultas de verificación de resultado y de permisos.
4. **Criterios de aceptación** — checklist atómico. **Un *assert* por criterio**, nombrando tabla, campo o elemento de UI.
5. **Definition of Done y evidencia** — cuáles de los criterios de la DoD aplican a este ticket, **cuáles no y por qué**, y qué captura o consulta se adjunta al PR.
6. **Alcance y decisiones fijas** — incluido contra excluido, y las citas a los ADR y decisiones que lo gobiernan.

## La regla de la medición

Al desglosar una tarea, la suma de los tripletes se compara contra las horas asignadas y **no se ajusta para que cierre**.

Si la tarea tiene 6,0 h y el desglose da 7,5, el ticket reporta 7,5 y declara dónde cae la deuda. Maquillar el número lo único que hace es mover el problema a la semana en que ya no hay margen. Este es el control que más veces destapó huecos reales del cronograma.

## Antes de escribir

Leé, en este orden: la hoja del cronograma con su asignación de horas, el contrato de datos, los ADR que la tarea toca, y la Definition of Done. Un ticket que cita un ADR que no existe es un ticket inválido.

## Verificación antes de entregar

- Estructura: las seis secciones, y ningún criterio de aceptación con más de un *assert*.
- Medición: la suma contra las horas asignadas, reportada aunque no cierre.
- Trazabilidad: toda decisión citada existe.
- Tamaño: entre 1 y 3 h. Un ticket de 5 h no es un ticket, es una tarea sin desglosar.

## Lo que este agente no hace

No escribe código de producto ni lo sugiere como bloque para copiar. Describe el mecanismo, nombra el archivo y fija el contrato; la implementación es del dev. Es la frontera que impide a dirección escribir código de producto y no se negocia.

Tampoco arregla estimaciones malas: si la estimación de origen no es creíble, el triplete la propaga. Decilo en vez de disimularlo.

## Ejemplo de uso

**Pedido:** Bajá la tarea de despliegue a producción a tickets para los devs.

**Resultado:** Devuelve los tickets con la estructura obligatoria y el desglose de estimación comparado contra las horas asignadas.
