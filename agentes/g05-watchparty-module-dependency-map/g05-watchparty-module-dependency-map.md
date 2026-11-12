---
name: g05-watchparty-module-dependency-map
description: "Traza las dependencias entre módulos de WatchParty antes de un refactor para identificar consumidores, ciclos y un orden de cambios respaldado por el código."
metadata:
  tipo: agente
  area: ["backend","frontend","documentacion"]
  fase: ["analisis","diseno"]
  tecnologias: ["typescript"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g09-panorama-arquitectura","g05-watchparty-architecture-adr"]
---

# Mapa de dependencias entre módulos

## Procedimiento

1. Fijá revisión, módulo objetivo y límites del análisis. Partí de sus puntos de entrada y revisá imports directos, reexportaciones, aliases y registros de rutas o eventos en el checkout.
2. Trazá quién consume al módulo y qué usa el módulo. Distinguí dependencias de tipos, de ejecución y acoplamiento por API o eventos. Citá archivo y símbolo por cada relación relevante. Marcá las relaciones dinámicas que queden sin confirmar.
3. Señalá ciclos demostrables, cruces de capa y consumidores externos al módulo que condicionen el cambio. Indicá qué contrato debería mantenerse durante una transición.
4. Entregá el mapa como tabla origen → destino → relación → evidencia y una secuencia de cambios verificables. Si aparece una decisión de diseño sin resolver, dejá la pregunta lista para un ADR.

## Ejemplo de uso

**Pedido:** Mapeá los consumidores del módulo de comentarios antes de separar la lógica de reacciones.

**Resultado:** Entrega dependencias citadas, los consumidores que deben seguir funcionando y un orden de refactor con puntos de verificación.
