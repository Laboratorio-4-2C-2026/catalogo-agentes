---
name: g05-watchparty-release-compatibility
description: "Evalúa si distintas revisiones de la web y la API de WatchParty pueden convivir durante un despliegue escalonado o una reversión."
metadata:
  tipo: agente
  area: ["backend","frontend","devops"]
  fase: ["revision","despliegue"]
  tecnologias: ["typescript","react","express"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g08-api-contract-guardian","g05-watchparty-web-api-integration","g05-watchparty-release-readiness"]
---

# Compatibilidad entre versiones web y API

## Procedimiento

1. Identificá las revisiones actualmente desplegadas y las candidatas de web y API. Confirmá qué combinaciones permite el despliegue y cuáles pueden aparecer al revertir.
2. Contrastá cada consumidor relevante con el proveedor de cada combinación. Revisá campos obligatorios, valores de enums, formatos, códigos de respuesta y valores por defecto. Si el cambio afecta eventos de sala, verificá también el formato y los campos que el cliente consume.
3. Entregá una matriz con web actual/candidata × API actual/candidata. Marcá cada combinación como compatible, incompatible, indeterminada o fuera del plan. Citá revisión y archivo, prueba o contrato que sustenta cada marca.
4. Proponé un orden de despliegue y de reversión solo para combinaciones respaldadas. Si ninguna secuencia es viable, identificá el cambio de compatibilidad necesario y la comprobación pendiente.

## Ejemplo de uso

**Pedido:** La API agrega un tipo de reacción. Revisá si podemos desplegarla mientras sigue activa la web anterior.

**Resultado:** Entrega la matriz para las revisiones provistas y señala qué comportamiento del cliente anterior hay que comprobar antes de recomendar el orden.
