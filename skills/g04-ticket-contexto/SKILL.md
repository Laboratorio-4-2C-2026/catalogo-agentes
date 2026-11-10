---
name: g04-ticket-contexto
description: 'Escribe la sección Contexto de un ticket de Linear de PitStop: dos párrafos sin jerga que dicen qué se va a construir y qué problema resuelve, para un dev junior que recién abre el ticket. Usar al redactar o mejorar el contexto de un ticket.'
metadata:
  tipo: skill
  area:
  - gestion
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

# Contexto de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

## Plantilla

```markdown
## Contexto

[Que hay que hacer, en terminos de lo que la app pasa a poder hacer. Sin jerga:
es lo primero que lee el dev.]

[Que problema resuelve: que falta hoy o que se rompe si esto no esta.]
```

### El contexto es la puerta de entrada del ticket

Es lo primero que lee el dev, y lo escribe alguien que ya entendio todo el
problema para alguien que recien arranca. Son dos parrafos cortos, seis frases
como maximo entre los dos: el primero dice **que va a construir**, en terminos de
lo que el usuario final ve o de lo que la app pasa a poder hacer; el segundo dice
**que problema resuelve**, o sea que falta hoy y que se rompe si esto no esta.

Se puede dar por sabido: HTML, CSS, JavaScript y TypeScript, React, componente,
prop, estado, funcion, base de datos, tabla, fila, API, endpoint, request y
response, JSON, Git, rama y pull request.

**No** se puede dar por sabido, y por lo tanto no aparece en el contexto sin
explicarse: guard, interceptor, decorador, upsert, migracion, seed, ORM,
monorepo, CI/CD, ID token, JWT, design system, tokens de diseno, SDK, service
account, bucket, connection string pooled o direct, breakpoint, ring de foco,
PWA, safe area, boilerplate, espejar. Si alguno es inevitable, se aclara ahi
mismo entre parentesis y en cinco palabras.

Nada de hexadecimales, rutas de archivo, nombres de clase ni comandos: eso vive
en el bloque tecnico. Y no es un resumen del alcance: la lista de tareas ya viene
abajo y no hay que repetirla.

Tope: 2 párrafos y 6 frases entre los dos. Lo que no entra se baja a la especificación técnica.

## Ejemplo de uso
**Pedido:** Escribí el contexto del ticket de alta de vehículo.

**Resultado:** Dos párrafos cortos, de hasta seis frases, que explican qué podrá hacer el usuario y qué falta hoy, sin rutas, comandos ni términos técnicos sin aclarar.
