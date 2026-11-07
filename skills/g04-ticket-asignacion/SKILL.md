---
name: g04-ticket-asignacion
description: Reparte los tickets de una semana de PitStop entre los devs por carga, dependencias y continuidad, evitando que un ticket bloquee a otro. Usar cuando se pide asignar tickets o repartir el trabajo de la semana.
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

# Asignación de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

## Asignacion

- Solo reciben tickets las personas con `takes_tickets: true`. PM, PO, Tech Leader
  y QA nunca reciben tickets de desarrollo (restriccion del charter: programa
  unicamente Lab2).
- Como todos los tickets son fullstack, no hay division por area: repartir por
  carga, por dependencias y por continuidad (quien ya toco esa parte la sigue).
- **Nunca inventar un `linear_user_id`.** Si es `null`, crear el ticket sin asignar
  y avisarlo al final indicando quien deberia tomarlo.

## Bloqueos

**Objetivo: que ningun ticket de la semana bloquee a otro de la misma semana.**

En orden de preferencia:

1. Elegir el corte de la semana de forma que los tickets sean independientes entre
   si, aunque eso signifique saltear una funcionalidad y tomar la siguiente.
2. Si un ticket bloquea a otro y los dos tienen que entrar, **los dos van a la
   misma persona**, con el bloqueante primero, siempre que sumen hasta sus 6 SP.
3. Si la suma pasa los 6 SP, van a dos personas que coordinan el orden dentro de la
   semana: el bloqueante arranca primero y el otro sigue apenas queda liberado. Se
   avisa en el reparto para que las dos sepan que dependen una de la otra.

El cronograma planifica encadenados en la misma semana a proposito cuando esperar una
semana entera dejaria al equipo a media carga. El panel de la semana de la app los marca
con "va con...": esos son los que hay que repartir con este criterio.

Las dependencias reales estan en `depends_on`. Una dependencia hacia una
funcionalidad ya `done` no bloquea nada. Al crear el ticket, las dependencias
vigentes van en `blockedBy` **y ademas** escritas como `Depende de: PIT-XX` en
`## Datos del ticket`, al principio del bloque tecnico.

## Ejemplo de uso
**Pedido:** Repartí los tickets de la semana entre los tres devs.

**Resultado:** Una tabla por dev con sus tickets y puntos, hasta 6 SP cada uno, indicando qué tickets encadenados deben coordinar entre ellos.
