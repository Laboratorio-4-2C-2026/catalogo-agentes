---
name: g04-guion-de-presentacion
description: Escribe el guión hablado de una presentación a partir de su estructura de láminas, por orador y con tiempos, en español natural. Usar cuando ya están definidas las láminas y hay que preparar qué dice cada integrante.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Guión de presentación

Convierte la estructura de la presentación en lo que cada persona va a decir.

## Entradas

La estructura (`g04-estructura-de-presentacion`), los datos reales y quién presenta cada parte.

## Flujo

1. Calcular el presupuesto de cada lámina: unas 130 palabras por minuto hablado.
2. Escribir por lámina:
   - **Orador** y **tiempo**.
   - **Texto:** frases cortas, para decir y no para leer. Abrir con el mensaje, después la evidencia.
   - **Pase:** la frase que conecta con el siguiente orador.
3. Contar palabras y recortar hasta que el total entre en el tiempo, dejando un 10% de margen.
4. Preparar preguntas probables con una respuesta corta y quién la toma.

## Reglas

- No repetir en voz alta lo que ya dice la lámina: explicar qué significa.
- Cada número debe coincidir exactamente con el de la lámina.
- Si un dato no está confirmado, marcarlo `[confirmar]` en vez de inventarlo.
- Escribir para hablar: nada de frases de tres líneas ni siglas sin explicar.

## Ejemplo de uso
**Pedido:** Escribí el guión de la presentación para los cuatro.

**Resultado:** Un guión por lámina con orador, texto para decir, minutos y frase de pase al siguiente, ajustado al tiempo total con el conteo de palabras.
