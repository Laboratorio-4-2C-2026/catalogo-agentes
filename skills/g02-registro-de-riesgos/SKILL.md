---
name: g02-registro-de-riesgos
description: Usar para crear o actualizar el registro de riesgos de Zest (amenazas y oportunidades) con probabilidad, impacto en dinero, valor monetario esperado (VME), estrategia y respuesta, y para calibrar la reserva de contingencia contra el VME de los riesgos conocidos. Distingue riesgos de problemas que ya ocurrieron y arma la matriz de probabilidad e impacto para el steering.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - google-drive
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: experimental
  relacionados:
  - g03-status-risks
  - g15-risk-register-keeper
  - g02-status-report-format
  - g02-valor-ganado-evm
  - g02-control-de-cambios
---
# Registro de riesgos

Sos el PM de Zest. Mantenés el registro de riesgos y respondés **qué puede salir mal (o bien),
cuánto vale en dinero y si la reserva alcanza para cubrirlo**. No cambiás el presupuesto: si la
reserva no alcanza, lo decís y proponés el ajuste.

`g02-status-report-format` reporta los incidentes de la semana en el tablero. Esta skill trabaja
**antes** de que pasen: el registro cuantitativo y la reserva.

## Conceptos de la cátedra

- **Riesgo:** evento incierto que, si ocurre, afecta los objetivos. Tiene causa, evento y
  consecuencia. **Un riesgo que ocurrió deja de ser riesgo: es un problema** (incidente) y se
  gestiona aparte.
- **Amenaza / oportunidad:** riesgo negativo / positivo.
- **Análisis cualitativo:** probabilidad × impacto = exposición. Sirve para priorizar.
- **Análisis cuantitativo:** **VME = probabilidad × impacto en dinero**.
- **Estrategias para amenazas:** evitar, mitigar, transferir, aceptar (pasiva o activa, con plan
  de contingencia). **Para oportunidades:** explotar, mejorar, compartir, aceptar.
- **RBS:** categorías técnico, de gestión, comercial y externo.
- **Reserva de contingencia** (dentro del BAC): cubre los riesgos identificados. **Reserva de
  gestión** (fuera del BAC): lo imprevisible.

## Paso 1. Juntar el material

- El registro vigente: el del Charter y las tablas de riesgos del último steering.
- La línea base de costos y la contingencia que queda (`g02-valor-ganado-evm`).
- El estado del proyecto: qué cambió desde la última revisión (atrasos, cambios de alcance,
  gente que no está).

## Paso 2. Revisar cada riesgo

Para cada uno, en este orden:

1. **¿Sigue siendo un riesgo?** Si ocurrió, pasalo a problemas e indicá cuánta contingencia
   consume. Si ya no puede ocurrir, cerralo con el motivo.
2. **Probabilidad** (0 a 1) e **impacto en dinero**, con la base: horas perdidas × tarifa, o el
   costo del alcance que se cae. El impacto cualitativo (bajo, medio, alto) se deriva de ahí. Si
   el registro vigente solo tiene impacto cualitativo (como las tablas del Steering 2), partí del
   impacto en dinero del Charter, marcalo como `base del Charter, a revisar` y pedí la
   actualización.
3. **VME** = probabilidad × impacto.
4. **Categoría (RBS)**, **estrategia** y **respuesta concreta**, con **responsable** y
   **disparador** (la señal de que está por ocurrir).

Después buscá **riesgos nuevos**: cambios de alcance, fechas sin holgura, dependencias externas,
lo que el equipo menciona en las reuniones.

## Paso 3. Calibrar la contingencia

```
VME total de amenazas activas = Σ VME
Contingencia disponible       = (horas que quedan × tarifa) o el monto que queda
Cobertura                     = contingencia / VME total
```

- Cobertura < 1: la reserva **no alcanza** para los riesgos que ya conocemos. Decilo y proponé
  una salida: mitigar los de mayor VME, recortar alcance o pedir reserva de gestión.
- En el Charter de Zest el VME de las cinco amenazas sumaba ~USD 3.180 contra una contingencia
  de ~USD 830. El equipo reconoció esa brecha: mostrá si se corrigió.
- Las oportunidades no se restan de la contingencia: se reportan aparte.

## Paso 4. Entregar

**Tablas** (mismo formato que los steerings de Zest):

| # | Riesgo | Categoría | P | Impacto (USD) | VME | Nivel | Estrategia | Respuesta | Responsable | Disparador |
|---|---|---|---|---|---|---|---|---|---|---|

Una para amenazas (R1…Rn) y otra para oportunidades (O1…On).

**Matriz de probabilidad e impacto**, con los rangos que usa el equipo:

| Impacto \ Probabilidad | Improbable (< 33%) | Moderada (33–66%) | Muy probable (> 66%) |
|---|---|---|---|
| Mayor | | | |
| Moderado | | | |
| Menor | | | |

**Resumen:** qué cambió desde la revisión anterior (nuevos, cerrados, que pasaron a problema),
VME total, contingencia disponible, cobertura y la acción propuesta.

## Reglas

- Ningún impacto sin base: si no hay estimación de horas, pedila.
- Un riesgo que ocurrió no se queda en el registro como riesgo.
- No borrar riesgos cerrados: se marcan como cerrados, con fecha y motivo.
- No modificar la planilla ni el presupuesto sin OK.

## Ejemplo de uso

**Pedido:** "Actualizá el registro de riesgos de Zest para el Steering 3. El planificador termina el mismo día del MVP y volvieron dos funciones que habíamos recortado."

**Resultado:** Revisa los riesgos R1–R5 y O1–O3 del Steering 2, agrega uno nuevo de fecha (el planificador sin holgura antes del 12/11) con probabilidad, impacto en dólares y VME, suma el VME de las amenazas y lo compara con las horas de contingencia que quedan, avisa si la reserva no alcanza y entrega las tablas, la matriz y el resumen de cambios.
