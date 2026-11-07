---
name: g04-ticket-estimacion
description: Estima tickets de PitStop en la escala de 1 a 5 SP, pensando en un estudiante de 3er año que usa Claude Code, y parte en verticales los que no entran. Usar cuando se pide estimar, reestimar o revisar los puntos de un ticket.
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
  relacionados:
  - g11-estimar-ticket
---

# Estimación de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

### Estimacion

Escala **1 a 5**, sin valores intermedios. Se estima cuanto le lleva a un
**estudiante de 3er año de ingenieria informatica, sin experiencia laboral, que usa
Claude Code**, y se **redondea para arriba**: la idea es que los 6 SP semanales se
resuelvan en 4 o 4,5 horas reales y que el resto quede como margen para lo que se
complique.

| SP | Que es |
|---|---|
| 1 | Configuracion o cambio acotado que Claude Code resuelve casi entero y el dev solo verifica |
| 2 | Una pantalla simple o un endpoint con su modelo, sobre un patron que ya vieron en la capacitacion |
| 3 | Vertical completa estandar: modelo, endpoint y pantalla, todo con patrones conocidos |
| 4 | Vertical con algo nuevo que hay que aprender primero (Firebase, Storage, push, un job) |
| 5 | Lo mas grande permitido: algo nuevo mas varias piezas |

Dos cosas tiran en direcciones opuestas y hay que sopesarlas en cada ticket: Claude
Code acelera mucho el andamiaje y el codigo repetitivo, pero son juniors y lo que
requiere entender una herramienta nueva o depurar una integracion les lleva mas de
lo que parece.

Si `features.yaml` trae un `estimate`, es la sugerencia del PM: respetarla salvo que
el analisis del prototipo muestre que esta muy lejos, en cuyo caso corregirla y
explicar por que.

Evitar tickets que sean solo un componente, un cambio de estilos, un hook, un
endpoint trivial o setup generico. No partir trabajo artificialmente para llegar al
objetivo de puntos.

## Cuándo partir

No partir un ticket en `[BE]` y `[FE]`. Si una funcionalidad es tan grande que la
vertical no entra en 5 SP, partirla en dos verticales mas chicas y completas —
por ejemplo "alta de vehiculo" y "edicion y baja de vehiculo" — no en capas.

## Respuesta

Por ticket: SP propuestos, una frase con el motivo y si difiere del `estimate` del PM. No escribir en Linear sin confirmación.

## Ejemplo de uso
**Pedido:** ¿Cuántos puntos le ponemos al ticket de subir la foto del vehículo?

**Resultado:** Propone 4 SP porque es una vertical con Firebase Storage para aprender primero, explica el motivo y avisa si conviene partirla.
