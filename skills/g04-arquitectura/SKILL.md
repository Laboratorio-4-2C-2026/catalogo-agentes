---
name: g04-arquitectura
description: 'Analiza decisiones de arquitectura de un proyecto y las deja como ADR: contexto, drivers, opciones comparadas con sus costos, decisión, riesgos y validación. Usar para una decisión técnica difícil de revertir, como una integración, un servicio nuevo o un cambio de estructura.'
metadata:
  tipo: skill
  area:
  - backend
  - documentacion
  fase:
  - diseno
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - martinbarreiroo
  madurez: experimental
  relacionados:
  - g15-product-adr-drafter
---

# Arquitectura

Ayuda a tomar decisiones técnicas caras de revertir y a dejarlas escritas. Las reglas diarias del backend están en `g04-nestjs-prisma-backend-architecture`.

## ¿Hace falta un ADR?

Sí, si la decisión es difícil de revertir, afecta a varios módulos o sumará costo de operación. Si no, resolverla en el ticket.

## Flujo

1. **Entender las restricciones:** requisitos, fecha, capacidad del equipo, servicios ya contratados, consigna de la materia. Si falta algo decisivo, preguntar.
2. **Leer lo que existe:** código, ADRs anteriores y documentación actual de cada tecnología. No decidir de memoria sobre versiones o límites.
3. **Definir de 3 a 5 criterios** antes de comparar. Priorizar reutilizar lo existente y que el equipo pueda operarlo.
4. **Comparar de 2 a 4 opciones reales** con los mismos criterios, incluida "no hacer nada" si es válida. Indicar qué agrega cada una: servicios, secretos, costo, carga de operación.
5. **Elegir y justificar**, diciendo qué se resigna.
6. **Definir el contrato:** módulos afectados, API o datos, seguridad y fallos.
7. **Pensar riesgos y validación:** qué podría invalidarla y qué prueba barata lo confirma antes de construir.

## Formato del ADR

```markdown
# ADR NN Título

Fecha y estado (propuesta, aceptada, reemplazada).

## Context
## Decision Drivers
## Options Considered
## Proposed Decision
## Risks and Validation
```

## Reglas

- No agregar servicios ni capas sin una necesidad presente.
- Separar hechos verificados de supuestos.
- Un ADR aceptado no se reescribe: una decisión nueva lo reemplaza y lo referencia.
- Proponer; la decisión final es del equipo.

## Ejemplo de uso
**Pedido:** ¿Cómo hacemos el reporting diario de KPIs, con Vercel Cron o GitHub Actions?

**Resultado:** Un ADR con el contexto, tres opciones comparadas según los mismos criterios, la decisión recomendada, los riesgos y cómo validarla, listo para revisar con el equipo.
