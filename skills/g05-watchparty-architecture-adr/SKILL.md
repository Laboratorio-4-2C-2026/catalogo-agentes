---
name: g05-watchparty-architecture-adr
description: "Documenta decisiones de arquitectura de WatchParty con un ADR. Usar cuando haya que elegir entre alternativas que afecten a varios módulos o que sean costosas de revertir."
metadata:
  tipo: skill
  area: ["gestion","documentacion"]
  fase: ["diseno"]
  tecnologias: ["agnostico"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g06-architecture-adr","g05-watchparty-module-dependency-map"]
---

# Registro de decisiones de arquitectura

## Procedimiento

1. Tomá la decisión a resolver, el ticket, el código o diagramas vigentes y los ADR previos relevantes. Identificá el estado actual y separá restricciones comprobadas de supuestos.
2. Compará las alternativas viables con los mismos criterios: consistencia de sala, latencia, complejidad operativa y costo de revertir. Incluí el estado actual si todavía es viable. Indicá qué evidencia cambiaría la comparación.
3. Redactá un ADR con título, estado, contexto, alternativas, decisión propuesta y consecuencias. Registrá cómo comprobar la decisión, quién debe validarla y cuándo reconsiderarla.
4. Si el equipo ya decidió, citá la evidencia y registrá la decisión acordada. Si queda abierta, conservá el estado «propuesto» y anotá las preguntas pendientes. Usá la ruta y numeración del checkout cuando te pidan guardar el ADR.

## Ejemplo de uso

**Pedido:** Compará recuperar el estado de una sala desde la API al reconectar con reconstruirlo a partir de los eventos recibidos.

**Resultado:** Entrega un ADR propuesto con los costos de ambas opciones y las mediciones que faltan para decidir.
