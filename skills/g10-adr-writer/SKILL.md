---
name: g10-adr-writer
description: Redactar un Architecture Decision Record (ADR) en el formato ya usado por el equipo a partir de una decisión técnica que ya se tomó, con su contexto y motivo. No compara alternativas (eso lo hace una skill de evaluación de alternativas); solo formaliza por escrito una decisión ya definida.
metadata:
  tipo: skill
  area:
  - documentacion
  fase:
  - diseno
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-nestjs-endpoint-doc-generator
  - g10-technical-decision-advisor
  - g15-product-adr-drafter
---
# ADR Writer

Convertir una decisión técnica ya tomada por el equipo (discutida en una reunión, un comentario de PR, o explicada directamente por la persona) en un ADR formal, siguiendo la estructura que ya usa el equipo en sus ADRs de Conexia (ej. "ADR - Conexia - Grupo 10"): contexto, decisión, alternativas consideradas y por qué se descartaron, consecuencias.

## Qué pedir si falta

Antes de escribir, confirmar con la persona (sin inventar):
- Cuál es la decisión exacta que se tomó (no "qué convendría hacer": eso ya se resolvió).
- Qué problema o necesidad la motivó.
- Qué alternativas se evaluaron y por qué se eligió esta, si se discutieron.
- Quién la tomó y cuándo (aunque sea aproximado).

Si alguno de estos datos no está disponible, dejar la sección como "pendiente de completar por el equipo" en vez de completarla con una suposición.

## Estructura del ADR

1. **Título**: corto, en infinitivo o sustantivo (ej. "Usar Firebase Auth para autenticación de usuarios").
2. **Estado**: propuesta / aceptada / reemplazada (preguntar si no se indica).
3. **Contexto**: el problema o restricción que llevó a necesitar esta decisión.
4. **Decisión**: qué se decidió, en una o dos oraciones claras.
5. **Alternativas consideradas**: lista breve de qué otras opciones se vieron y por qué no se eligieron (solo si la persona las mencionó).
6. **Consecuencias**: qué implica esta decisión hacia adelante, incluyendo trade-offs aceptados y qué quedaría más difícil de cambiar después.

## Reglas

- No reabrir la discusión ni sugerir una alternativa mejor: este agente documenta, no decide.
- Escribir en el idioma que use la persona.

## Ejemplo de uso

**Pedido:** Ya decidimos usar Geoapify para geocoding en vez de Google Maps por costo. Armame el ADR.
**Resultado:** Un ADR con título, contexto (necesidad de geocoding para matching de trips), la decisión, por qué se descartó Google Maps (costo) y las consecuencias de depender de Geoapify.
