---
name: g04-ticket-urgencia
description: Define la prioridad de los tickets de Linear de una semana de PitStop a partir del grafo de bloqueos, para que el tablero ordenado diga qué hacer primero. Usar cuando se pide priorizar u ordenar los tickets de la semana.
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
  requiere:
  - linear
  grupo: "04"
  autor:
    nombre: Manuel Lostaló
    github: ManuLosta
  colaboradores:
  - nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - ManuLosta
  madurez: usado-en-proyecto
  relacionados: []
---

# Urgencia de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

### La priority es el orden en que se hacen los tickets

Los tableros del equipo se miran ordenados por prioridad, asi que **la prioridad no
mide importancia: define el orden**. Arriba tiene que quedar lo que hay que hacer
primero, aunque sea un ticket de infraestructura que nadie considera "importante".

Sale sola del grafo de bloqueos que ya se armo para repartir la semana:

| Priority | Cuando | Que le dice al dev |
|---|---|---|
| `1` Urgent | Bloqueante raiz: sin el no arranca nadie | Esto va el primer dia, si o si |
| `2` High | Bloquea a otro ticket de la semana | Apenas se libere el raiz, esto |
| `3` Medium | No bloquea ni esta bloqueado | Se puede hacer en cualquier momento |
| `4` Low | Esta bloqueado por otros de la semana | Va al final, cuando lleguen sus dependencias |

Con esos cuatro niveles el orden de la semana queda determinado por el tablero solo,
sin que nadie tenga que leer los `blockedBy` para saber por donde empezar. Si dos
tickets caen en el mismo nivel y da igual cual va primero, se dejan empatados.

> **Limite de la herramienta:** el orden manual de Linear (`sortOrder`, lo que se
> arrastra en el tablero) **no se puede setear** — ni `save_issue` ni
> `linear_update_issue` lo exponen. Por eso la prioridad es la unica palanca de orden
> disponible, y por eso se usan los cuatro niveles en vez de dos. Dentro de un mismo
> nivel el orden lo decide Linear; si el PM necesita un orden exacto ahi adentro, lo
> arrastra a mano. No prometer que se ordeno el tablero mas alla de la prioridad.

## Ejemplo de uso
**Pedido:** Poneles prioridad a los tickets de esta semana.

**Resultado:** Asigna Urgent al bloqueante raíz, High a los que bloquean a otro, Medium a los independientes y Low a los bloqueados, y muestra el orden resultante.
