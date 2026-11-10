# Manual operativo de Valor Ganado (EVM)

Cómo medir avance y costo, pronosticar el cierre y sostener los números ante
quien los cuestione. Sirve para cualquier proyecto; lo específico de Zest está
en [`../project-management.md`](./SKILL.md) y la teoría tal como se
dio en clase en [`course.md`](./course.md).

EVM responde tres preguntas con un solo set de datos: **cuánto ibas a tener
hecho**, **cuánto tenés hecho** y **cuánto te costó tenerlo**. Todo lo demás son
derivados.

## 0. Antes de calcular nada

No inventes ni estimes a ojo ningún dato que pueda verificarse contra una
fuente primaria. Si falta un dato, pedilo o medilo; no lo supongas.

| Dato | Dónde sale de verdad |
|---|---|
| Alcance y pesos | EDT/WBS aprobada |
| Qué está terminado | Sistema de tickets, estado de PRs, actas de aceptación |
| Horas reales | Parte de horas; si no hay, estimación reproducible (§7) |
| Costos no laborales | Facturas, consola del proveedor |
| Línea base | Documento de línea base aprobado, con su versión |

**Nunca infles un número.** Si alguien pide "subilo un poco", la respuesta es
no: en el momento en que un número no se puede reconstruir, todo el tablero
pierde autoridad. Un número honesto bien explicado se defiende mejor que uno
cómodo.

**Registrá el método junto al número.** Todo valor que presentes tiene que poder
reconstruirse: qué fórmula, qué datos, qué fecha de corte.

## 1. Los tres números base

Todo EVM se construye sobre tres acumulados a **una fecha de corte única y
explícita**, los tres en la misma unidad (dinero, u horas si el proyecto cotiza
en horas).

- **PV — Valor Planificado.** Cuánto valor decía la línea base que ibas a tener
  producido a la fecha de corte. Es la curva S planificada acumulada y sale solo
  de la línea base aprobada.
- **EV — Valor Ganado.** Cuánto valor produjiste realmente, **valuado a precios
  de la línea base**. Es lo que más se malinterpreta: el EV no se mide en lo que
  costó, sino en lo que el plan decía que valía. `EV = BAC × % de avance real
  ponderado`.
- **AC — Costo Real.** Cuánto gastaste efectivamente para producir ese EV, en el
  mismo período, el mismo alcance y la misma fecha de corte.
- **BAC — Presupuesto hasta la Conclusión.** El total de la línea base de
  costos. **Incluye** la reserva de contingencia y **no incluye** la reserva de
  gestión (§8).

**Regla de oro:** los tres números tienen que estar alineados en fecha de corte
y en alcance. Comparar un EV que incluye un entregable con un AC que no incluye
sus horas rompe todo lo que venga después.

## 2. Cómo medir el EV: el método importa más que la fórmula

Acá es donde se rompen la mayoría de los tableros de EVM. Elegí el método **por
tipo de actividad**, no uno solo para todo el proyecto.

| Método | Cómo funciona | Cuándo usarlo |
|---|---|---|
| 0/100 | 0% hasta terminar, 100% al terminar | Tareas cortas, dentro de un período de reporte |
| 50/50 (o 25/75) | Mitad al empezar, mitad al terminar | Tareas que cruzan dos períodos |
| Hitos ponderados | Cada hito libera un % del presupuesto | Paquetes largos con entregables intermedios claros |
| % ponderado por EDT | Peso × % completado, sumado | Lo más común; requiere pesos defendibles |
| Medida física | Unidades producidas / unidades totales | Cuando hay algo contable (planos, km, endpoints) |
| Esfuerzo prorrateado | % atado a una actividad base discreta | QA, inspección: lo que se mueve con otra cosa |
| Nivel de esfuerzo (LOE) | EV = PV, siempre y por definición | Gestión, soporte, infraestructura, licencias |

### La regla del nivel de esfuerzo (leer dos veces)

Una actividad de nivel de esfuerzo gana valor con el **calendario**, no con el
alcance. Gestión de proyecto, reuniones, infraestructura corriendo, licencias:
consumen presupuesto hayas entregado o no.

Por definición, en LOE **el EV es igual al PV**. Consecuencia directa: una
actividad LOE nunca puede generar variación de cronograma. **Su SV es cero,
siempre.**

Si aplicás un único porcentaje de avance de producto sobre todo el BAC
(incluidas las líneas LOE), estás fabricando variación donde no la hay. Es el
error más común y el que más infla los índices.

**Diagnóstico:** calculá qué porcentaje del BAC es LOE.

- Más de ~30%: los índices globales ya no hablan de eficiencia, hablan de
  composición.
- Más de ~60%: los índices globales solos son casi inútiles; hay que reportar
  aparte el subconjunto impulsado por alcance.

### Regla de los ítems a medias

Salvo que uses 50/50 explícitamente, **solo cuenta lo terminado**. Nada de "casi
listo", "en revisión" o "falta el merge". Trabajo hecho pero no integrado es
costo sin valor ganado, y esa es exactamente la señal que EVM existe para dar.
No la tapes: es tu argumento más fuerte cuando alguien pregunta por qué bajó el
CPI.

### Cómo armar pesos defendibles

El peso de cada paquete sale de **su presupuesto**, no de una intuición de
importancia. Si un paquete vale 1.920 de un BAC de 7.256, su peso es 26,5%.
Punto. Pesos asignados "por relevancia" son la puerta de entrada a un EV inflado,
y es lo primero que va a cuestionar alguien que sepa.

## 3. Variaciones e índices

```
SV  = EV − PV          Variación de cronograma (en dinero)
CV  = EV − AC          Variación de costo
SPI = EV / PV          Índice de desempeño del cronograma
CPI = EV / AC          Índice de desempeño del costo
```

| Valor | SPI | CPI |
|---|---|---|
| > 1 | Adelantado respecto al plan | Produjiste más valor del que ese gasto debía comprar |
| = 1 | En fecha | En presupuesto |
| < 1 | Atrasado | Sobrecosto |

### Qué NO significan

- **SV y SPI no miden tiempo, miden dinero.** SPI 1,30 no es "estamos 30%
  adelantados en el calendario". Para traducirlo a tiempo, dividí el SV por el
  PV promedio por período, y presentalo como aproximación, no como dato.
- **Un CV positivo no es plata ahorrada.** El dinero ya se gastó: es valor
  producido por encima de lo que ese gasto debía comprar.
- **Un CPI alto no es necesariamente eficiencia.** Puede ser composición (§2) o
  pesos mal puestos.

### El SPI pierde sentido cerca del cierre

Al terminar el proyecto, EV y PV convergen los dos al BAC, así que el SPI tiende
a 1 aunque el proyecto esté atrasadísimo. **En el último tercio, el SPI deja de
ser diagnóstico.** Qué hacer:

1. Reportarlo junto al análisis de ruta crítica (días reales de atraso).
2. Usar **Cronograma Ganado** (Earned Schedule): `SPI(t) = ES / AT`, donde `ES`
   es el momento del plan en que estaba previsto el EV actual y `AT` el tiempo
   transcurrido. Da un índice en unidades de tiempo que no converge
   artificialmente a 1.

## 4. Diagnóstico: por qué un índice da lo que da

Un índice sin explicación causal no se sostiene en una revisión. Para cada
índice fuera de rango, buscá la causa y verificala.

### Si el SPI está muy por encima de 1

Revisá en este orden:

1. **¿El equipo trabajó más horas de las planificadas?**
   `relación de esfuerzo = horas reales / horas planificadas al corte`. Si esa
   relación se parece al SPI, ya encontraste la causa: el adelanto es volumen,
   no eficiencia. Es el hallazgo más frecuente y el más fácil de verificar.
2. **¿La línea base arrancó conservadora?** Mirá la trayectoria del SPI período
   a período. Un recorrido tipo `0,4 → 0,6 → 0,9 → 1,1 → 1,3` no es velocidad de
   crucero, es recuperación, y conviene decirlo así.
3. **¿El método de EV está inflando?** Revisá §2: LOE medido con % de producto,
   pesos por relevancia, ítems a medias contados.
4. **¿El trabajo inicial era infraestructura?** Setup, entornos, CI y despliegue
   consumen presupuesto y producen poco EV si la EDT pondera entregables de
   producto. Eso hunde el SPI temprano y lo hace rebotar después.

### Si el CPI está muy por encima de 1

1. **Separá el subconjunto impulsado por alcance y calculá su CPI aparte.** Es
   la prueba decisiva:
   `CPI_alcance = (% avance × presupuesto de ese subconjunto) / costo real de ese subconjunto`.
   Si da ≈ 1 mientras el global da 1,3, la diferencia es composición, no
   eficiencia.
2. **¿El AC está subestimado?** Horas no registradas, trabajo en ramas sin
   mergear, tiempo de gente que no carga partes. Un AC incompleto infla el CPI.
3. **¿Hay costos diferidos?** Facturas que no llegaron, licencias anuales no
   devengadas.

### Principio de interpretación

Una variación favorable es un **disparador de análisis, no un motivo de
festejo**. Un SPI de 1,3 es una señal para revisar si la línea base era
realista, no un permiso para gastar el excedente. Y el excedente no es
capacidad: si los recursos están fijos por contrato, calendario o convenio,
estar adelantado no crea horas.

## 5. Pronóstico

```
ETC = EAC − AC         Costo pendiente hasta el cierre
EAC = AC + ETC         Costo total estimado a la conclusión
VAC = BAC − EAC        Variación a la conclusión (positivo = cierra por debajo)
```

### Las cuatro formas de estimar el EAC

| Fórmula | Supuesto | Cuándo usarla |
|---|---|---|
| `EAC = AC + (BAC − EV)` | Lo que falta cuesta lo presupuestado | La desviación fue puntual y no se repite |
| `EAC = BAC / CPI` | La eficiencia actual continúa | La desviación es sistémica |
| `EAC = AC + (BAC − EV) / (CPI × SPI)` | Costo y cronograma siguen pesando | Hay presión de fecha además de costo |
| `EAC = AC + ETC ascendente` | Reestimación real de lo pendiente | Preferida cuando el plan inicial ya no es válido o el método importa |

Decí siempre qué fórmula usaste y por qué.

### Cuándo te mienten las fórmulas

Si una porción grande del presupuesto es nivel de esfuerzo, las fórmulas
fallan: asumen que lo que falta escala con el alcance pendiente, cuando en
realidad esas líneas van a seguir gastando por calendario pase lo que pase.

Hacé el ETC ascendente:

```
ETC = (períodos restantes × costo LOE por período)
    + (trabajo de alcance pendiente × tasa aplicable)
    + riesgos cuantificados que aún no ocurrieron
```

Y decí explícitamente por qué descartaste la fórmula. Eso demuestra criterio, no
un atajo.

### TCPI: qué eficiencia hace falta de acá en más

```
TCPI = (BAC − EV) / (BAC − AC)     para cerrar dentro del BAC
TCPI = (BAC − EV) / (EAC − AC)     para cerrar dentro del EAC aprobado
```

Mayor que 1 = más difícil de completar; igual a 1 = lo mismo; menor que 1 = más
fácil. Si el TCPI es mucho mayor que el CPI actual, el objetivo es irreal.
**Decilo ahí, no al final.** Un TCPI de 1,4 cuando venís con CPI 0,9 significa que
el plan no cierra.

## 6. Chequeos de consistencia

Correlos siempre antes de presentar. Cada uno atrapa un error distinto.

```
[ ] PV, EV y AC comparten fecha de corte y alcance
[ ] PV acumulado al final del plan = BAC exactamente
[ ] Suma de pesos de la EDT = 100%
[ ] Ningún ítem a medias cuenta (salvo método 50/50 declarado)
[ ] EV ≤ BAC
[ ] AC incluye todo: trabajo en ramas/revisión, horas sin cargar, costos devengados
[ ] CPI recalculado sobre el subconjunto de alcance: ¿coincide con el global?
[ ] Las reservas están del lado correcto del BAC
[ ] ETC + AC = EAC, y BAC − EAC = VAC
[ ] Los totales del tablero cierran con los de la EDT (no dos fuentes de verdad)
[ ] Cada número tiene método documentado y es reconstruible
[ ] Redondeos declarados: si mostrás 159 h pero calculaste con 158,5, decilo
```

## 7. Estimar el AC cuando no hay parte de horas

Es lo normal en equipos chicos. La estimación es aceptable si es
**reproducible y auditable**. Lo que no es aceptable es un número redondo sin
método.

### Método basado en la actividad del repositorio

Para cada persona y cada día con actividad:

```
horas_del_dia = acotar(
    (último evento − primer evento) + margen_previo,
    piso, techo
)
```

Valores razonables: margen previo 1 h (trabajo antes del primer commit), piso
1,5 h, techo 9 h. Sumá por persona y por período.

Advertencias que tenés que declarar vos antes de que te las señalen:

- **Es un piso, no un valor exacto**: no captura diseño, reuniones ni
  investigación que no dejan rastro.
- Un día con un solo commit cae al piso aunque haya sido una jornada entera.
- **Traé todas las ramas, no solo la principal.** Un clon superficial o de una
  sola rama subestima el esfuerzo de forma sistemática. Verificá la
  configuración del remoto antes de confiar en el resultado.
- Excluí al rol de gestión si ya está presupuestado como LOE aparte, o lo contás
  dos veces.

Presentalo así: "es una estimación con este método, reproducible contra el
repositorio". Eso vale más que un número preciso sin respaldo.

## 8. Reservas

| | Reserva de contingencia | Reserva de gestión |
|---|---|---|
| Cubre | Known-unknowns: riesgos identificados | Unknown-unknowns: lo imprevisible |
| ¿Dentro del BAC? | Sí, es parte de la línea base de costos | No, queda fuera |
| Quién la libera | El director del proyecto | El patrocinador / la dirección |
| Al usarla | Se consume dentro de la línea base | Requiere cambio formal de línea base |

```
Línea base de costos = trabajo + contingencia = BAC
Presupuesto total autorizado = BAC + reserva de gestión
```

**Análisis de reservas en cada corte:** reportá cuánto queda, no solo cuánto
usaste. "Quedan 54 de 66 horas, 8% sobre el trabajo restante" dice algo; "usamos
12 horas" no.

Error frecuente: vaciar la contingencia temprano porque "vamos bien". La reserva
cubre todos los períodos que faltan. Gastarla al 60% de avance te deja sin
colchón justo cuando aparecen los riesgos de integración, despliegue y cierre.

## 9. Control de cambios y rebaseline

Cuando entra alcance nuevo, o se saca alcance, el procedimiento no es opcional.

1. Solicitud de cambio por escrito, con origen y justificación.
2. Análisis de impacto cuantificado: horas, costo, cronograma, riesgo, calidad.
3. Decisión de financiamiento: ¿de dónde salen las horas?
   - de la reserva de contingencia,
   - de recortar alcance de menor valor,
   - de presupuesto adicional aprobado.
4. Aprobación por quien tenga autoridad (comité de control de cambios).
5. Actualización de la línea base → v2. La v1 se conserva, no se pisa.
6. Registro en una decisión documentada (ADR, acta, registro de cambios) con
   fecha.
7. Recálculo de todo el tablero contra la línea base nueva.

Reglas duras:

- **Nunca absorbas alcance nuevo contra la línea base vieja.** Si lo hacés,
  todos los índices miden contra un plan que no contempla ese trabajo y quedan
  inválidos.
- **Nunca borres la línea base anterior.** La trazabilidad de versiones es la
  evidencia de que hubo control.
- **Si recortaste alcance, cerralo en el sistema de tickets** con el motivo y la
  referencia a la decisión. Alcance resignado que sigue abierto en el backlog
  contradice tu propio relato, y lo van a encontrar.

### Cómo justificar un recorte de alcance estando adelantado

La objeción clásica: "si van bien, ¿por qué resignan funcionalidad?". La
respuesta, parada en PMBOK:

1. **Restricciones en competencia.** Alcance, cronograma, costo, calidad,
   recursos y riesgo compiten. Si el cronograma y los recursos están fijos, el
   ajuste sale del alcance o de la calidad, y resignar calidad es peor.
2. **El índice mide el plan, no la capacidad.** Estar adelantado no crea horas.
3. **Proteger la reserva.** Absorber todo contra la contingencia la vacía justo
   cuando faltan los períodos de mayor riesgo.
4. **Criterio explícito de qué se cortó.** Lo ideal es cortar caminos de
   conveniencia hacia funciones que siguen existiendo, no requisitos. Si podés
   decir "ninguna capacidad del producto se pierde", ganaste la discusión.
5. **Nombrá el anti-patrón contrario.** Agregar alcance porque parece haber
   capacidad es *gold plating*, una mala práctica reconocida.

## 10. Procedimiento completo, de cero

```
 1. Fijar la fecha de corte y la versión de línea base vigente.
 2. Traer la EDT con presupuesto por paquete. Verificar que los pesos sumen 100%.
 3. Clasificar cada paquete: impulsado por alcance / nivel de esfuerzo / prorrateado.
 4. Elegir método de medición de EV por clase (§2).
 5. Determinar el estado real de cada ítem contra fuente primaria. Solo terminados.
 6. Calcular el % de avance ponderado del subconjunto impulsado por alcance.
 7. Calcular el EV: alcance por avance ponderado + LOE por calendario.
 8. Calcular el PV acumulado desde la curva planificada.
 9. Calcular el AC: horas reales (o estimadas con método, §7) + costos no laborales.
10. Calcular SV, CV, SPI, CPI.
11. Recalcular el CPI solo sobre el subconjunto de alcance. Comparar con el global.
12. Construir el ETC de abajo hacia arriba. Derivar EAC y VAC.
13. Calcular el TCPI y contrastarlo con el CPI real.
14. Análisis de reservas: cuánto queda, sobre qué base.
15. Correr los chequeos de §6.
16. Escribir la causa de cada desvío, con su evidencia.
```

## 11. Presentar y defender

### Estructura de una lámina de desempeño

Primero el dato, después la causa, después la acción. Nunca al revés.

```
NÚMERO  →  QUÉ MIDE EN UNA LÍNEA  →  POR QUÉ DIO ESO  →  QUÉ HACEMOS
```

Cada índice tiene que poder leerse en voz alta en una frase con la fórmula y los
números adentro: "SPI es valor ganado sobre planificado, 6.124 contra 4.493, da
1,36". Si no podés decir la cuenta, no entendés el número.

### Adelantate a las limitaciones

La regla que más rinde: **decí vos la debilidad de tu medición antes de que te la
pregunten.** Reconocer que el método sobrestima el EV de las líneas LOE, que la
línea base arrancó conservadora o que las horas son estimadas te deja mejor
parado que cualquier número. Demuestra que entendés tu propia medición.

### Repreguntas frecuentes y dónde está la respuesta

| Pregunta | Dónde está la respuesta |
|---|---|
| "¿Por qué el índice da tan alto?" | §4: relación de esfuerzo, línea base conservadora, composición |
| "¿El CV positivo es plata ahorrada?" | §3: no, el dinero ya se gastó |
| "¿Cómo midieron el EV del nivel de esfuerzo?" | §2: la pregunta que separa a quien sabe |
| "¿Por qué no usaron la fórmula de EAC?" | §5: composición LOE, ETC ascendente |
| "¿Entonces planificaron mal?" | §4: en parte sí; por eso no se gasta el excedente |
| "¿Van a seguir así?" | §3: el adelanto no se acumula; el SPI converge a 1 |
| "¿No sobrestiman el avance?" | §2: solo ítems terminados; el riesgo está en los pesos |
| "¿Por qué resignan alcance si van bien?" | §9: restricciones fijas, proteger la reserva |

### Coherencia entre fuentes

Todo lo que muestres tiene que contar la misma historia: el tablero, la EDT, el
sistema de tickets y la demo del producto. Si el tablero dice que un módulo está
al 100% pero en el sistema de tickets sigue en revisión, la contradicción la van
a encontrar. Alinealo antes.

## 12. Formulario

```
EV   = BAC × % avance ponderado
SV   = EV − PV
CV   = EV − AC
SPI  = EV / PV
CPI  = EV / AC
ETC  = EAC − AC            (o reestimación ascendente)
EAC  = AC + ETC
EAC  = AC + (BAC − EV)                     desvío puntual
EAC  = BAC / CPI                           desvío sistémico
EAC  = AC + (BAC − EV) / (CPI × SPI)       costo + cronograma
VAC  = BAC − EAC
TCPI = (BAC − EV) / (BAC − AC)             objetivo BAC
TCPI = (BAC − EV) / (EAC − AC)             objetivo EAC
SPI(t) = ES / AT                           cronograma ganado

BAC = trabajo + reserva de contingencia
Presupuesto total autorizado = BAC + reserva de gestión
```

## 13. Los ocho errores que más se repiten

1. Aplicar un único % de avance de producto sobre un BAC que contiene nivel de
   esfuerzo.
2. Contar ítems a medias o "en revisión" como valor ganado.
3. AC incompleto: trabajo en ramas sin integrar, horas sin cargar, facturas
   pendientes.
4. Leer un CPI alto como eficiencia sin revisar la composición del presupuesto.
5. Usar la fórmula de EAC con alta proporción de LOE.
6. Pesos de EDT asignados por relevancia en vez de por presupuesto.
7. Absorber alcance nuevo sin rebaseline, o pisar la línea base anterior.
8. Leer el SPI en el último tercio del proyecto como si fuera diagnóstico.
