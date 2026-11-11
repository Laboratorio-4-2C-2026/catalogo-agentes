---
name: g12-validar-pr-de-producto
description: Hace la validación de producto de una PR — prueba la historia desde la preview, cruza cada criterio de aceptación, revisa que sea un slice vertical y marca solo lo técnico que rompe algo — y deja un comentario en la PR. Usar cuando una PR de una historia está lista para revisar, o al pedir "validá esta PR".
owner: '@n-mangini'
role: qa
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: experimental
  relacionados:
  - g12-revisar-pr
  - g12-generar-tests-e2e
---

# Validar PR de producto

Una PR necesita dos validaciones y ninguna reemplaza a la otra: puede estar bien hecha y no
cerrar la historia, o cerrarla con un código que no conviene mergear. La técnica la hacen el
TL y CodeRabbit, que también se ocupa de estilo, nombres y formato. Esta skill hace la otra:
**¿esta PR le da a la persona lo que pide la historia?**

## 1. Leer la historia

Del cuerpo de la PR salen el ticket y la historia (en SplitIt, el ticket en Linear y la
historia en `SplitItLab/roadmap`). Tomar los criterios de aceptación tal cual están escritos
y el link al canvas, que es la referencia visual.

Si la PR no nombra ticket ni historia, decirlo y frenar: sin criterios no hay qué validar.

## 2. Revisar que sea un slice vertical

La PR tiene que entregar una porción de la historia de punta a punta: algo que una persona
pueda usar desde la pantalla. Si es solo una capa (solo backend, solo una pantalla sin datos),
marcarlo: la validación de producto se corre hasta la integración, cuando ya no queda margen
para corregir. Igual seguir con lo que se pueda validar.

## 3. Probar desde la preview

Abrir la preview de Vercel de la PR (link en los comentarios del bot o en los checks) y
recorrer la historia como la haría la persona. Para cada criterio de aceptación:

- ✅ se cumple, con lo que se vio;
- ❌ no se cumple, con los pasos para reproducirlo;
- ⚠️ no se pudo probar, con el motivo.

Comparar contra el canvas solo lo que el criterio pide. Listo cuando cada criterio tiene
una de las tres marcas.

## 4. Mirar lo técnico grave

Leer el diff buscando únicamente lo que rompe: algo que ya andaba y deja de andar, pérdida
o exposición de datos, un agujero de seguridad, un camino sin salida. Para cada uno, la
línea y por qué rompe.

## 5. Comentar

Un comentario en la PR, en este orden:

1. Veredicto: **se puede mergear** o **pide cambios**.
2. Criterios con su marca.
3. Slice vertical: sí o qué falta.
4. Lo técnico grave, si hay.

Se piden cambios solo si un criterio no se cumple o algo técnico rompe. Lo menor va como
comentario y la PR se mergea igual; si lo puede resolver CodeRabbit, se le pide a CodeRabbit.
Si un detalle lo va a resolver un ticket que viene, se anota en ese ticket.

Mostrar el comentario antes de publicarlo.

## Ejemplo de uso

**Pedido:** Validá esta PR: https://github.com/<org>/<repo>/pull/<n>

**Resultado:** Prueba la historia desde la preview, marca cada criterio con ✅, ❌ o ⚠️, revisa que sea un slice vertical y muestra el comentario con el veredicto antes de publicarlo en la PR.
