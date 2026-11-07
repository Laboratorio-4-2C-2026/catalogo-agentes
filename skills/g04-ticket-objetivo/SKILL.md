---
name: g04-ticket-objetivo
description: 'Escribe el bloque de un ticket de Linear de PitStop que lee el dev antes de la parte técnica: Objetivo, Referencia visual, Qué tiene que quedar andando, Por dónde empezar y Palabras que vas a ver. Usar al redactar o mejorar esas secciones.'
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - analisis
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

# Objetivo de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

## A quién le habla

**Arriba del separador** lee un dev de segundo ano que abre el ticket por primera vez y
todavia no sabe que es esto. Ahi va que se va a construir, como se ve y por donde
arranca. **Entra en una pantalla**: si hay que scrollear para llegar al separador, esta
largo y hay que bajar cosas.

La regla que decide de que lado va cada cosa: **ningun bullet de arriba del separador
contiene un hexadecimal, una clase de Tailwind, una ruta de archivo, un comando, un
endpoint ni un nombre de modelo de Prisma.** Si aparece uno, ese bullet va abajo. La
unica excepcion es "Por donde empezar", que se explica mas adelante.

## Plantilla

```markdown
## Objetivo

[Resultado esperado, en una frase.]

**Referencia visual:** [la pantalla del prototipo funcionando y como se llega a ella].
El PM adjunta la captura.

## Que tiene que quedar andando

- [Que puede hacer el usuario, verificable abriendo la app. Sin jerga.]
- [...]

## Por donde empezar

1. [Primer paso concreto]
2. [...]

## Palabras que vas a ver

- **[Termino]**: [que es y para que sirve en este ticket, en una linea.]
```

### Los topes del bloque de arriba

| Seccion | Tope |
|---|---|
| Contexto | 2 parrafos, 6 frases entre los dos |
| Objetivo | 1 frase, mas la linea de referencia visual |
| Que tiene que quedar andando | 3 a 6 bullets, 1 linea cada uno |
| Por donde empezar | 3 a 5 pasos, 1 linea cada uno |
| Palabras que vas a ver | 3 a 6 terminos, se omite entera si no hay ninguno |

Estos topes no son una sugerencia. Cuando algo no entra, la respuesta nunca es apretar
mas la letra arriba: es bajarlo al bloque tecnico, que para eso no tiene limite.

### Objetivo y referencia visual

El objetivo es una frase: que queda andando cuando el ticket cierra.

Debajo va la `Referencia visual`, que nombra **la pantalla del prototipo funcionando** y
como se llega a ella ("pantalla de Garage, solapa Informacion"). Va arriba, junto al
objetivo y no enterrada entre las notas, porque es la forma en que un junior entiende
que esta construyendo antes de leer una sola linea tecnica.

### Que tiene que quedar andando

Es la lista de criterios de aceptacion del dev y del QA: lo que se verifica **usando la
app**, sin abrir el codigo.

- Se escribe como lo que el usuario puede hacer, o lo que pasa al tocar algo.
- Cubre mobile y desktop en una frase, en castellano y sin numeros: "el formulario abre
  pegado abajo en el celular y como ventana centrada en la compu".
- Nada de valores: sin hexadecimales, sin tokens, sin clases, sin breakpoints, sin
  nombres de endpoint. Todo eso tiene su lugar abajo.
- Prohibido "funciona correctamente", "queda prolijo" y cualquier cosa que dos personas
  puedan dar por cumplida de manera distinta.

### Por donde empezar

Es el orden de ataque, no un resumen del alcance. Un junior que abre el ticket ya sabe
que hay que hacer; lo que no sabe es que tocar primero.

- 3 a 5 pasos, en el orden en que conviene hacerlos, uno por linea.
- Sigue la vertical del ticket: modelo y migracion, endpoint, pantalla, probar.
- **El ultimo paso es siempre probarlo corriendo la app**, en las dos resoluciones si
  hay UI. Si el ticket toca la API, sus tests de Jest son uno de los pasos.
- Es la **unica seccion del bloque de arriba que puede nombrar** un modelo, una ruta o
  un comando: es el puente hacia el bloque tecnico. Aun asi no lleva valores —ni
  hexadecimales, ni tokens, ni breakpoints— y se queda en una linea por paso.

### Palabras que vas a ver

Cierra el bloque de arriba, y ese lugar es a proposito: el dev se cruza con el glosario
**antes** de entrar en la especificacion, que es donde los terminos lo esperan.

De 3 a 6 terminos, **solo los que realmente aparecen en el cuerpo** y que un dev de
segundo ano probablemente no conoce. Una linea cada uno: que es y para que sirve *en
este ticket*, no la definicion de manual.

Si el ticket no introduce ningun termino nuevo, la seccion se omite entera: no
inventar entradas de relleno. Tampoco repetir lo que ya quedo explicado en el
contexto.

## Ejemplo de uso
**Pedido:** Armá el objetivo y lo que tiene que quedar andando del ticket de historial.

**Resultado:** Una frase de objetivo, la pantalla de referencia, de 3 a 6 criterios verificables usando la app, los pasos en orden y el glosario de los términos nuevos.
