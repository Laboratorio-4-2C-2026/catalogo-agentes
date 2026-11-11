---
name: g12-reportar-semaforo
description: Arma el estado semanal del proyecto para la cátedra o los directores, con alcance, cronograma, costo, riesgos e incidentes en verde, amarillo o rojo, escrito a alto nivel. Usar al preparar el reporte de estado de la semana, un steering o una consulta de cómo va el proyecto.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: usado-en-proyecto
  relacionados:
  - g12-cerrar-semana
  - g12-reportar-incidente
  - g12-registrar-riesgo
---

# Reportar semáforo

Quien lee este reporte no sigue el día a día: necesita saber en un minuto cómo va el
proyecto y qué se está haciendo con lo que no va bien. Es el estado general de la semana.
Una falla puntual se registra con `reportar-incidente`.

## 1. Juntar las fuentes

En el sprint en curso (en SplitIt, `04-iteration/sprints/sprint-N/`):

- el plan vigente (README del sprint y decision log): contra eso se mide el alcance;
- `seguimiento.md`: SPI y CPI de la última semana cerrada y sus notas;
- `risk-log.md`: riesgos abiertos y su exposición;
- `incidentes.md`: lo que pasó en la semana y cómo se resolvió.

Si la semana no está cerrada en el seguimiento, avisar y correr antes `cerrar-semana`.

## 2. Pintar cada dimensión

| Dimensión | Verde | Amarillo | Rojo |
|---|---|---|---|
| Alcance | Se compromete todo lo del plan vigente | Algo prometido está en duda | Algo prometido sale del plan |
| Cronograma | SPI ≥ 0,95 | 0,80 – 0,95 | < 0,80 |
| Costo | CPI ≥ 0,95 | 0,80 – 0,95 | < 0,80 |
| Riesgos | Ninguno abierto en 🟧 o 🟥 | Alguno en 🟧 | Alguno en 🟥 |
| Incidentes | Sin abiertos | Abierto de criticidad Media o Baja | Abierto de criticidad Alta |

Si el proyecto ya tiene umbrales propios, mandan esos.

El alcance se mide contra el **plan vigente**, no contra la línea base original: en SplitIt
es el presupuesto vigente según el decision log.

Un número que sale bien por un motivo engañoso se aclara al lado: un CPI alto con horas sin
usar es capacidad sin usar, no eficiencia. Si falta un dato, la dimensión va en gris
con "sin dato" y el motivo.

## 3. Escribir

Por dimensión: color y una o dos líneas con qué pasó, el impacto y la fecha. Para lo que
no está en verde, agregar qué se está haciendo y para cuándo.

Escribir a alto nivel: sin SPT-xx, sin números de PR, sin nombres de tecnologías ni de
archivos. Nombrar las funcionalidades como las ve el usuario ("el acceso sin cuenta", "el
ingreso con Google"). Usar "llevó más/menos de lo previsto", para no atribuir el desvío a una persona.

Ejemplo de línea: "🟡 Cronograma · SPI 0,85. La carga de gastos no llegó a
mergearse antes del cierre y se entregó dos días después; el valor se recupera la semana siguiente."

## Ejemplo de uso

**Pedido:** Armá el semáforo de esta semana para los directores.

**Resultado:** Pinta alcance, cronograma, costo, riesgos e incidentes en verde, amarillo o rojo con una o dos líneas cada uno, escritas a alto nivel y con qué se hace con lo que no está en verde.
