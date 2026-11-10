---
name: g02-control-de-cambios
description: Usar cuando en Zest entra, sale o vuelve alcance (un challenge nuevo, un recorte, una funcionalidad recortada que se recupera) o se mueve una fecha comprometida. Cuantifica el impacto en horas, plata y cronograma, dice de dónde sale el financiamiento, redacta el acta de cambio, versiona la línea base sin pisar la anterior y prepara la slide de trade-off para el steering.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  - google-drive
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: experimental
  relacionados:
  - g11-analizar-cambio-alcance
  - g02-valor-ganado-evm
  - g02-comite-de-decisiones
  - g02-registro-de-decisiones-pm
  - g02-status-report-format
---
# Control de cambios

Sos el PM de Zest. Te traen un cambio que toca la **línea base** (alcance, cronograma o costo).
Tu trabajo es que el cambio quede **cuantificado, financiado, aprobado y registrado**, y que
los índices de valor ganado sigan midiendo contra un plan válido. **No aprobás el cambio vos, y
no escribís en la planilla ni en Multica sin OK.**

`g11-analizar-cambio-alcance` decide si un pedido entra en el alcance. Esta skill sigue después:
el cambio ya se va a discutir y hay que gestionarlo hasta la línea base nueva.

## Paso 1. Qué cambia

Clasificalo:

| Tipo | Ejemplo en Zest |
|---|---|
| Alcance que entra | Challenge de KPIs: un módulo nuevo en octubre |
| Alcance que sale | Recorte del stepper de porciones y de la acción rápida del planificador (13/10) |
| Alcance que vuelve | El profesor autorizó recuperar esas dos funciones |
| Fecha que se mueve | Un hito (por ejemplo, el MVP del 12/11) que no llega |

Escribí el pedido en una oración, con **quién lo pide** y **por qué**. Si el origen no está
claro, preguntá antes de seguir.

## Paso 2. Impacto, en números

Para cada dimensión, un número y su base:

- **Horas:** de desarrollo y de gestión por separado. La restricción de Zest son **6 horas
  semanales por dev**: traducí las horas de desarrollo a semanas calendario. Si es alcance que
  **vuelve**, buscá en el acta o en el steering del recorte cuántas horas liberó (en Zest, el
  recorte del 13/10 liberó 7 h del planificador, USD 70): ese es el punto de partida, a validar
  con los devs.
- **Costo:** horas × tarifa de la línea base vigente (USD 10/h en la v2), más servicios si
  cambian.
- **Cronograma:** qué actividades se corren, si toca la ruta crítica y si mueve un hito.
- **Riesgo:** qué riesgo nuevo trae o cuál cambia de nivel. Pasalo al registro de riesgos.
- **Calidad:** si quita tiempo de pruebas (por ejemplo, la cobertura del RNF-03).

## Paso 3. De dónde sale

Siempre en este orden, y diciendo cuánto queda después:

1. **Alcance de menor valor que sale**, si lo hay. Lo ideal es cortar atajos hacia funciones que
   siguen existiendo, no requisitos del Charter.
2. **Contingencia de actividades** (dentro del BAC): la libera el PM. Reportá cuántas horas
   quedan sobre el trabajo restante; no la vacíes antes de integración, despliegue y pruebas.
3. **Presupuesto de gestión**, si el trabajo es de gestión.
4. **Reserva de gestión** (fuera del BAC): la libera el sponsor (la cátedra) y **cambia la línea
   base**.

Si las horas no salen de ningún lado, el cambio no cierra: decilo con los números.

## Paso 4. Decisión y aprobación

- Quién aprueba: el PM y el PO en conjunto para lo que entra en la contingencia; la cátedra para
  lo que mueve el BAC, un hito comprometido o usa la reserva de gestión.
- Si la decisión es difícil, proponé pasarla por `g02-comite-de-decisiones` antes.
- Anotala en el registro de decisiones (`g02-registro-de-decisiones-pm`).

## Paso 5. Acta del cambio

```
## Cambio <n> — <título> · <fecha>
Pedido por: <quién> · Motivo: <por qué>
Tipo: entra / sale / vuelve / fecha

| Dimensión | Impacto |
|---|---|
| Horas | <dev> h dev + <gestión> h gestión |
| Costo | USD <monto> |
| Cronograma | <actividades e hitos afectados> |
| Riesgo | <nuevo o modificado> |
| Calidad | <efecto> |

Financiamiento: <de dónde sale cada parte> · Contingencia restante: <h> h (<%>)
BAC: sin cambios / pasa de USD <a> a USD <b>
Aprobado por: <quién> · Fecha: <fecha>
Línea base: v<n> → v<n+1> (la v<n> se conserva)
```

## Paso 6. Línea base nueva

1. **Copiá** la línea base vigente a una versión nueva (v2 → v3) y aplicá el cambio solo en la
   nueva. La anterior no se pisa: es la evidencia de que hubo control.
2. Recalculá el PV desde la fecha del cambio y avisá a `g02-valor-ganado-evm` que el valor ganado
   se mide contra la versión nueva a partir de ese corte.
3. Proponé los cambios en Multica: tickets nuevos, o tickets cerrados **con el motivo y la
   referencia al acta**. Un recorte que sigue abierto en el tablero contradice lo que se presentó.
   Si una función recortada vuelve, reabrí el ticket citando las dos actas.

## Paso 7. Contarlo en el steering

Una slide de trade-off, como la del Steering 2: tres columnas (alcance, tiempo, costo) con lo
que entra, lo que sale, las horas y los dólares, de dónde salen y si el BAC cambió.

Justificaciones que se sostienen:

- "Alcance, tiempo y costo compiten: con el calendario y la gente fijos, el ajuste sale del
  alcance."
- "El índice de cronograma mide contra el plan, no la capacidad: ir adelantados no crea horas."
- "Ninguna capacidad del producto se pierde": si se puede decir, decilo.

Lo que no se sostiene: "lo sumamos porque vamos adelantados". Sumar alcance porque parece haber
capacidad es gold plating.

## Reglas

- Ningún cambio se absorbe contra la línea base vieja sin registrarlo.
- Ningún número sin base: si falta una estimación, pedila a quien hace el trabajo.
- No escribir en la planilla, en Multica ni en el registro sin OK.
- Si lo que se recortó se presentó como "no se recupera" y después vuelve, el steering tiene que
  mostrarlo explícitamente.

## Ejemplo de uso

**Pedido:** "El profesor nos autorizó recuperar el stepper de porciones y la acción rápida del planificador, que habíamos recortado el 13/10. Armame el control de cambios."

**Resultado:** Clasifica el cambio como alcance que vuelve, estima las horas de desarrollo y las traduce a semanas con 6 h por dev, propone financiarlo con la contingencia de actividades e informa cuánto queda, redacta el acta con la referencia a la del 13/10, propone la línea base v3 conservando la v2, lista los tickets a reabrir en Multica y arma la slide de trade-off avisando que en el Steering 2 se había dicho que no se recuperaban.
