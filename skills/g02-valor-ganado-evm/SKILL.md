---
name: g02-valor-ganado-evm
description: Usar para estimar esfuerzo y costo, armar o revisar el presupuesto y calcular, auditar y defender el valor ganado de Zest (PV, EV, AC, SPI, CPI, EAC, ETC, VAC, TCPI) con la teoría de Dirección de Proyectos de la cátedra. Separa líneas de nivel de esfuerzo del desarrollo, muestra cada cuenta y propone la decisión.
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
  - multica
  - google-drive
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: usado-en-proyecto
  relacionados:
  - g15-evm-calculator
  - g04-earned-value-presentacion
  - g11-auditar-steering
  - g02-status-report-format
  - g02-estimador-de-horas-reales
  - g02-control-de-cambios
---

# Gestión del proyecto: esfuerzo, presupuesto y valor ganado

Asiste a quien tenga el rol de PM (rota entre steerings) para estimar esfuerzo,
armar o revisar el presupuesto, calcular el valor ganado (PV, EV, AC, SPI, CPI,
EAC, ETC, VAC, TCPI) y, sobre todo, **entender qué dicen los números de Zest** y
poder defenderlos. Responde en español.

No es una calculadora. Cada número que da viene con la fórmula, los datos que
usó, de dónde salió cada dato, la fecha de corte y una lectura de qué significa
para el proyecto.

## Archivos de este módulo

Si sos una persona y no un agente, empezá por
[`project-management/README.md`](./guia-de-uso.md): cómo llamar
la skill, qué datos darle y ejemplos de pedidos.

| Archivo | Cuándo leerlo |
|---|---|
| Este archivo | Siempre: fuentes de Zest, composición del presupuesto, último corte conocido, hallazgos abiertos y cómo responder |
| [`project-management/evm-manual.md`](./evm-manual.md) | Siempre que haya que calcular, auditar, pronosticar o defender un número: métodos de EV, diagnóstico, EAC, chequeos, reservas, rebaseline |
| [`project-management/course.md`](./course.md) | Preguntas de estudio o de examen, o "cómo lo pide la cátedra": teoría de Gestión Financiera y Valor Ganado, glosario y ejercicios resueltos |
| `../docs/product.md` (`zest-support/docs/product.md`) | Alcance, hitos, equipo y riesgos |

## De dónde salen los números de Zest

Nunca inventes un PV, EV o AC: leelo de una de estas fuentes o pedilo, y decí
cuál usaste y a qué fecha de corte.

| Qué | Fuente |
|---|---|
| Línea base (PV por período, BAC, reservas) | Planilla **"10B-Equipo 02 - EVM y Curva S - Avance por %"** (Drive, hoja `PRESUPUESTO`) |
| Supuestos de costo (tarifas, HH por rol) | Planilla **"Zest_Presupuesto_EVM"**, hoja `Supuestos` |
| Por qué cada número es el que es | Doc **"Memo_Respaldo_Gestion_Financiera_Zest"** |
| Rutina semanal de EVM del equipo | Doc **"Guía EVM"** |
| Últimos números presentados | Deck **"Zest - Steering 2"** (15/10/2026), slides *Presupuesto* y *Valor ganado* |
| Qué está terminado (EV del desarrollo) | Multica: tickets en `done` (ver `multica.md` (`zest-support/skills/multica.md`)). `in_review` **no** cuenta como terminado |
| Qué se integró de verdad | PRs mergeados y `git log` del repo `zest` |
| Horas reales | Parte de horas de la planilla; si falta, estimación desde el repo (manual §7) |
| Salud de la plataforma (no es EVM, pero da contexto) | Reporte de KPIs en `zest/kpis/` |

Si la sesión tiene conector de Google Drive, leé las planillas directamente. Si
no, pedile al usuario los valores de las filas. Si Multica no responde, decilo y
pedí la cantidad de tickets en vez de adivinarla.

## Composición del presupuesto (línea base v2)

Es lo primero que hay que tener en la cabeza, porque define qué miden los
índices.

| Línea | USD | % del BAC | Tipo de medición |
|---|---|---|---|
| Desarrollo (2 devs, 192 HH a USD 10/h) | 1.920 | 26,5% | **Impulsada por alcance**: tickets terminados |
| Gestión (PM, PO, TL, QA; 384 HH a USD 10/h) | 3.840 | 52,9% | **Nivel de esfuerzo** (EV = PV) |
| Infraestructura, dominio y herramientas | 956 | 13,2% | **Nivel de esfuerzo** (EV = PV) |
| Costo de actividades | 6.716 | | |
| Contingencia de actividades (quedan 54 de 66 h) | 540 | 7,4% | Reserva dentro del BAC |
| **BAC: línea base de costos** | **7.256** | 100% | |
| Reserva de gestión | 660 | | Fuera del BAC |
| **Presupuesto total del proyecto** | **7.916** | | |

**El 66% del BAC es nivel de esfuerzo.** Según el manual (§2), por encima de
~60% los índices globales solos son casi inútiles: hablan de composición, no de
eficiencia. En Zest **siempre** se reportan dos juegos de índices: el global y
el del **subconjunto de desarrollo**, que es el único que mide avance real.

La v2 se aprobó por control de cambios el 13/10: el challenge de KPIs sumó 46 h
(19 de desarrollo + 27 de gestión) que costaron USD 460, financiados con USD 70
liberados del planificador (se cortaron el stepper de porciones y la acción
rápida del planificador), USD 120 de contingencia y USD 270 del presupuesto de
gestión. El BAC no cambió. La línea base v1 (en ARS, memo del 01/09) se conserva
y no se mezcla con la v2.

**Después, el profesor autorizó recuperar esas dos funciones.** Volvieron al
cronograma (tickets del 05/11 al 12/11). Es un segundo cambio de alcance y se
registra como tal: fecha de la autorización, horas estimadas y de dónde salen
(lo más probable, de la contingencia de actividades), y cuánta contingencia
queda después.

Todo el proyecto se ejecuta sobre free tiers (desembolso real ≈ 0). El
presupuesto valoriza el proyecto **como si fuera real**, a precios de mercado:
decilo cada vez que alguien pregunte por qué "gastamos" plata.

## Último corte conocido (Steering 2, 15/10/2026)

Úsalo como contexto y control de cordura, **no como dato actual**: buscá en la
planilla un corte más nuevo.

| | Valor | Cómo se lee |
|---|---|---|
| PV | USD 4.493 | 61,9% del BAC |
| EV | USD 6.124 | 84,4% del BAC |
| AC | USD 4.591 | 399 HH incurridas (159 dev + 240 gestión) + servicios |
| SPI | 1,36 | 6.124 / 4.493 |
| CPI | 1,33 | 6.124 / 4.591 |
| SV | +USD 1.631 | En dinero, no en días |
| CV | +USD 1.533 | Margen restante, no ahorro |
| MVP en producción | 12/11/2026 | |

Historia útil para leer la tendencia: con la línea base v1 el SPI fue
1,00 → 0,42 → 0,75 → 0,89 en los períodos 1 a 4. La caída fue de medición (los
tickets cerrados el 27/08 se reconocieron recién al final del período 3), no un
frenazo. En ese momento el AC solo incluía gastos de caja, así que el CPI no
significaba nada. El equipo empezó a cargar horas reales después.

## Hallazgos abiertos: auditar antes del próximo steering

Son cosas que, con los números del Steering 2, **no cierran** o no se pueden
reconstruir. No las des por ciertas ni por falsas: verificalas contra la
planilla y decí qué encontraste.

1. **El EV parece calculado con un único % sobre todo el BAC.** Si gestión e
   infraestructura se midieran como nivel de esfuerzo (EV = PV, SV = 0), todo el
   SV tendría que venir de desarrollo + contingencia, que en total valen 2.460.
   Para un SV de +1.631, el PV de esas líneas al 15/10 tendría que ser ≤ 829
   (un 34% de ellas). Con desarrollo repartido parejo desde el período 2, al
   período 11 el plan ya pedía cerca de dos tercios. **Si se confirma, el SPI
   1,36 y el CPI 1,33 están inflados por composición** (error n.º 1 del manual).
   Recalcular: EV = EV de desarrollo por tickets terminados + PV de las líneas
   LOE.
2. **Relación de esfuerzo.** Calcular `HH reales / HH planificadas al corte`
   (399 contra el plan acumulado de la planilla). Si se parece al SPI, el
   adelanto es volumen, no eficiencia (manual §4).
3. **CPI de desarrollo por separado.** `CPI_dev = EV_dev / (159 h × USD 10)`. Si
   da cerca de 1 mientras el global da 1,33, la diferencia es composición.
4. **Contingencia.** Reportar cuánto queda sobre el trabajo restante, no cuánto
   se usó, y no vaciarla antes del cierre (integración, despliegue y pruebas son
   los períodos de más riesgo).
5. **Alcance recuperado.** El stepper de porciones y la acción rápida del
   planificador se recortaron el 13/10 y volvieron con autorización del
   profesor. En el Steering 2 se dijo "las 2 funciones no se recuperan", así que
   el Steering 3 tiene que mostrar el cambio explícitamente (qué vuelve, horas,
   de dónde salen, riesgo). La justificación es que el challenge cerró antes de
   lo estimado y la contingencia alcanza sin mover el BAC ni el 12/11, no que
   "vamos adelantados". Los dos tickets terminan el día del MVP, sin holgura:
   tienen que quedar últimos en prioridad, para que lo primero que se caiga sean
   ellos y no el planificador base.

## Momento del proyecto: el SPI ya no alcanza

El proyecto va del 06/08 al 23/11 (16 períodos semanales). Desde fines de
octubre estamos en el **último tercio**: EV y PV convergen al BAC y el SPI tiende
a 1 aunque haya atraso. A partir de ahora:

- Acompañar el SPI con la ruta crítica hacia el MVP del 12/11 (días reales de
  atraso del planificador y de la corrección de errores).
- Calcular el **cronograma ganado**: `SPI(t) = ES / AT` (manual §3).
- Para el EAC, usar **ETC ascendente**, no `BAC / CPI`: con 66% de LOE las
  fórmulas fallan (manual §5).

```
ETC = (períodos restantes × costo LOE por período)
    + (HH de desarrollo pendientes × USD 10)
    + riesgos cuantificados que todavía no ocurrieron
```

## Estimar AC desde el repositorio

Si faltan horas de desarrollo, usá el método del manual (§7) sobre el repo
`zest`, **con todas las ramas** (`git fetch --all`, y verificá con
`git rev-parse --is-shallow-repository` que el clon no sea superficial). Excluí a
las personas de gestión: ya están presupuestadas como LOE. Presentalo como piso
reproducible, no como valor exacto.

## Estimar esfuerzo y armar presupuesto para Zest

- La restricción que manda (teoría de restricciones) son las **6 h semanales
  por desarrollador**. Toda estimación en calendario pasa por ese número.
- Tarifa de la línea base v2: **USD 10/h** para todos los roles. La v1 usó
  mercado en ARS (encuesta de sueldos Sysarmy/OpenQube 2026.1 y dólar BNA). No
  mezclar monedas ni líneas base en una misma cuenta.
- Dar rango, no un número: PERT `E = (O + 4M + P) / 6` con `σ = (P − O) / 6`, y
  el nivel de confianza.
- Para una tarea nueva, documentar la **base de la estimación** como en la
  plantilla de clase: paquete de la WBS, costos directos e indirectos,
  contingencia, método, supuestos, rango y confianza.
- La contingencia se calibra con el **VME** de los riesgos conocidos. En el
  Charter, el VME de las cinco amenazas sumaba ~USD 3.180 contra una
  contingencia de ~USD 830; es una brecha que el equipo ya reconoció.

## Cómo responder

1. **Traé los datos** de las fuentes de arriba y listalos con fecha de corte y
   fuente. Si falta uno, pedilo; no lo completes.
2. **Seguí el procedimiento del manual (§10)**: clasificar líneas, medir EV por
   tipo, calcular, recalcular sobre el subconjunto de desarrollo, ETC
   ascendente, reservas, chequeos (§6).
3. **Mostrá la cuenta**: `SPI = EV / PV = 6.124 / 4.493 = 1,36`. Dos decimales
   para índices, dólares enteros para montos, formato argentino (`1.234,56`).
4. **Interpretá para Zest**: comparación con el corte anterior (tendencia, no
   foto), doble alerta (CPI < 1 y SPI < 1), composición.
5. **Recomendá una decisión y quién la toma**, como pide la Guía EVM: recortar o
   simplificar alcance (PO), simplificar la solución técnica (TL), destrabar un
   bloqueo (PM), o recalcular el EAC y avisar temprano. Una reunión de EVM sin
   decisión es "estar ocupados", no avanzar.
6. **Decí vos las debilidades** de la medición antes de que te las pregunten
   (manual §11).

Si la persona está estudiando y no reportando, primero el concepto como lo da la
cátedra (`course.md`), después aplicado a los números reales de Zest: el examen
premia conectar la teoría con el proyecto.

## Qué NO hacer

- No inflar un número ni mover la línea base para que los índices se vean
  mejor. Solo un cambio formal de alcance mueve la línea base.
- No presentar un CPI calculado con un AC sin las horas del equipo como si
  midiera eficiencia.
- No contar tickets en `in_review` o PRs sin mergear como valor ganado.
- No escribir en la planilla ni en Multica sin que el usuario lo pida.

## Ejemplo de uso

**Pedido:** "Calculá el valor ganado de Zest al corte del 05/11: PV acumulado 5.600, tickets terminados por actividad [lista], horas reales dev 190 y gestión 300. Quiero los índices globales y los de desarrollo."

**Resultado:** Lista los datos con su fuente y fecha, mide gestión e infraestructura como nivel de esfuerzo (EV = PV) y desarrollo por tickets terminados, muestra cada cuenta (`SPI = EV / PV = ...`), compara con el corte anterior, avisa si los índices globales están inflados por composición y cierra con la decisión que corresponde y quién la toma.
