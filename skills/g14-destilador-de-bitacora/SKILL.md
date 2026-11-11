---
name: g14-destilador-de-bitacora
description: Captura aprendizajes operativos al cerrar una sesión (un hecho por archivo, título como afirmación verificable) y al cierre de un hito los destila en lecciones consultables, evitando duplicados. Usala al terminar una sesión de trabajo o un hito, cuando hay un aprendizaje que no debería perderse.
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - mantenimiento
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
  madurez: experimental
  relacionados:
  - g12-registrar-decision
  - g13-lecciones-aprendidas
---

# Destilador de bitácora

Captura los aprendizajes operativos del proyecto y, al cierre de cada hito, los destila en lecciones consultables.

## El principio

**Un hecho vive en un solo lugar, y un archivo contiene un solo hecho.** Lo que vuelve inmanejable un repo es la duplicación, no el volumen.

## Modo captura — al cerrar una sesión

**1. Preguntate si hubo aprendizaje, no si hubo trabajo.** Va a la bitácora una sorpresa, un gotcha, una herramienta que no hace lo que promete, una decisión que se tomó contra una restricción que resultó no existir. **No** va lo que el repositorio ya registra por otra vía: una decisión (va a un ADR), el estado del proyecto, o el historial de git.

**2. Buscá contra el corpus antes de escribir.** Si el hecho ya está, actualizá esa entrada. Una bitácora con dos entradas del mismo hecho deja de ser consultable.

**3. El título es una afirmación verificable, no un tema.**

| Sí | No |
|---|---|
| «Un gantt no conserva la masa» | «Problemas con el gantt» |
| «El nodo de LLM falla lejos de su causa» | «Errores de n8n» |
| «Un ADR puede decidir contra una restricción que no existe» | «Revisión de ADRs» |

**4. Nombre del archivo:** `AAAA-MM-DD-el-titulo-en-kebab.md`. La fecha es la del aprendizaje.

**5. Cuerpo:** qué pasó, por qué sorprendió, y qué hacer distinto la próxima. Corto. Si necesita más de una pantalla, probablemente son dos hechos.

## Modo destilación — al cerrar un hito

**1.** Leé todas las entradas del rango.
**2.** Agrupá por patrón, no por fecha ni por herramienta.
**3.** **Un patrón necesita al menos dos entradas que lo sostengan.** Con una sola no es un patrón, es un episodio: dejalo como está.
**4.** Marcá aparte los aprendizajes que **contradicen una decisión vigente**. Ésos no son lecciones, son hallazgos, y van a quien corresponda decidir.
**5.** Marcá aparte los que **caducaron** porque cambió la decisión que los causó.

El destilado cita las entradas que lo sostienen. Un patrón sin citas no se escribe.

## Lo que este agente no hace

Un aprendizaje que nadie escribió no existe: la captura depende de la disciplina de cierre de sesión, y este agente no la reemplaza. Tampoco decide qué caducó — eso lo marca una persona que sabe qué decisión cambió.

## Ejemplo de uso

**Pedido:** Cerramos el hito 4, destilá las lecciones de la bitácora.

**Resultado:** Agrupa las entradas del hito, descarta lo que ya vive en otro documento y devuelve las lecciones con su fuente.
