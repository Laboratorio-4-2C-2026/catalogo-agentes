---
name: g04-estructura-de-presentacion
description: 'Define la estructura de una presentación del proyecto PitStop: objetivo, audiencia, láminas, mensaje de cada una, tiempos y quién presenta. Usar cuando hay que preparar una entrega, un sprint review o la presentación final.'
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Estructura de presentación

Decide qué se cuenta y en qué orden antes de armar láminas o guión.

## Entradas

Tiempo disponible, audiencia, consigna de la cátedra y qué se evalúa. Si falta la consigna, pedirla: no suponer los criterios.

## Flujo

1. **Una frase:** qué tiene que recordar la audiencia al terminar.
2. **Bloques.** Base que se adapta a la consigna:
   - Problema y propuesta.
   - Estado del producto y demo.
   - Avance: Earned Value y cronograma.
   - Riesgos e incidentes.
   - KPIs.
   - Decisiones de arquitectura.
   - Próximos pasos.
3. **Láminas:** una idea por lámina, con el título como mensaje ("Vamos un 8% atrasados por Auth"), no como tema ("Earned Value").
4. **Datos:** cada número indica de dónde sale, por ejemplo `g04-earned-value-presentacion` o `g04-riesgos-presentacion`.
5. **Tiempos:** asignar minutos sin superar el 90% del total, para dejar margen.

## Salida

Tabla: número | título-mensaje | contenido | fuente | minutos | quién presenta. Al final, datos que faltan conseguir.

## Reglas

- Si la consigna pide un punto, tiene que estar. Marcar qué lámina lo cubre.
- No inventar números: marcar "falta dato".
- El guión lo escribe `g04-guion-de-presentacion` y la demo `g04-guion-de-demo`.

## Ejemplo de uso
**Pedido:** Armá la estructura de la presentación del Sprint 3, tenemos 15 minutos.

**Resultado:** Una tabla de láminas con mensaje, contenido, fuente del dato, minutos y responsable, que suma 15 minutos e incluye el bloque de demo.
