# Teoría de clase — Gestión Financiera y Valor Ganado

Lo que se dio en **Dirección de Proyectos Informáticos 2026** (Universidad
Austral; profesores Marcos Giagnorio, Iván Woscoff y Jorge Marchini), unidad
*Gestión de Costos*. Usalo cuando la pregunta sea de estudio, de examen o de
"cómo lo pide la cátedra". El cómo hacerlo bien en la práctica está en
[`evm-manual.md`](./evm-manual.md).

Fuentes: slides *Gestión Financiera (ex: Costos)* y *Gestión del Valor Ganado
(EVM)*, planilla *EVM_KPIs* (Dimensiones y fórmulas EVM). Base: PMBOK; la cátedra
usa la terminología de dominios ("dominio de Gestión Financiera") y aclara que en
PMBOK v6 era el "área de conocimiento Gestión de costos".

## 1. Concepto

- El dominio de **Gestión Financiera** incluye los procesos y herramientas para
  el uso y la asignación de recursos monetarios, internos y externos, de la
  organización que hace el trabajo.
- El rendimiento financiero se relaciona con los costos, la financiación y, en
  algunos casos, la propuesta de valor del proyecto.
- **El valor de las mediciones financieras no está en recopilar y difundir
  datos, sino en usarlos para tomar decisiones informadas** y actuar. (Es la
  frase que justifica que cada reunión de EVM termine en una decisión.)

**Concepto clave: costo del producto ≠ finanzas del proyecto.**

- *Costo del producto* = materiales + mano de obra + equipos = precio del
  producto.
- *Finanzas del proyecto* = valor esperado → financiamiento → reservas y
  contingencias → flujo de caja → riesgos e incertidumbre → cronograma y plazos
  → calidad y beneficios.

**Keywords:** definición de valor (cada proyecto define su propia medida de valor
generado), maximizar el valor, fondeo (cómo obtiene recursos el proyecto; *Scrum
no lo considera*), restricciones financieras (*Scrum tampoco*), presupuesto del
proyecto, línea base de costos (*cost baseline*), reservas y contingencias.

## 2. Los cuatro procesos

| Grupo | Proceso |
|---|---|
| Planificación | Planificar la Gestión Financiera · Estimar los Costos · Desarrollar el Presupuesto |
| Monitoreo y Control | Monitorear y Controlar las Finanzas |

### 2.1 Planificar la Gestión Financiera

Definir cómo se van a estimar, presupuestar, gestionar, monitorear y controlar
los costos. Por qué hace falta:

- Cada organización lo hace a su manera.
- Hay que definir la **unidad** (ARS, USD, EUR...).
- Puede no haber un proceso y hay que definir un lineamiento.
- Puede haber sistemas, o hay que hacerlo a mano.
- ¿Registro de costos o registro contable?
- Algunas empresas piden 3 cotizaciones para estimar, otras 1, otras ninguna.
- Puede haber áreas (ej. Controlling) a las que hay que informar o que nos
  informan.

Factores **externos**: mercado (productos, proveedores, precios, términos) y
bases comerciales (listas de precios). Factores **internos**: políticas de
estimación, plantillas, lecciones aprendidas, conocimiento y experiencia del
equipo.

### 2.2 Estimar los Costos

Desarrollar una aproximación del costo de los recursos necesarios: personal,
materiales, equipamiento, servicios, instalaciones y categorías especiales
(inflación, costo de financiación, contingencia). Se presentan a nivel
actividad o resumidas.

**Rango de exactitud:** en el inicio, orden de magnitud **−25% a +75%**; más
adelante, con más información, **−5% a +10%**.

**Herramientas de estimación de costos:**

| Técnica | Cómo |
|---|---|
| Análoga | Datos históricos, proyectos similares |
| Paramétrica | `p × q`, `h × q` (precio o tarifa por cantidad) |
| 3 puntos (PERT) | `cE = (cO + 4·cM + cP) / 6` |
| Triangular | `cE = (cO + cM + cP) / 3` |
| Juicio de expertos | |
| Delphi | Rondas de estimaciones que convergen |
| Ascendente (bottom-up) | Se estiman los componentes básicos y se agregan |
| Basada en puntos | Poker cards u otras |
| Análisis de reservas | Buffers |
| Basada en riesgos | `exposición = probabilidad × impacto` |
| Costo de la calidad | Para evitar retrabajo |

**Estimar esfuerzo:**

- Ágiles: story points, planning poker.
- Por experiencia / histórico: análoga, horas/persona, días/persona,
  meses/FTE, bottom-up, Delphi.
- Por tamaño: paramétrica, **puntos de función** (entradas / salidas /
  consultas / datos / integraciones), **COCOMO**.

**Riesgos al estimar costos** (por eso existen checklists):

- Errores en la interpretación del alcance.
- Omisiones y ambigüedades en la definición del alcance.
- Pobre definición del cronograma.
- Plazos demasiado optimistas.
- WBS incorrecta.
- Inadecuada estimación o valoración de riesgos.
- Técnicas de estimación inapropiadas.
- Errores en la asignación y el cálculo de costos indirectos.

**Costo de los defectos (ej. software):** un defecto introducido en
requerimientos cuesta $100 si se detecta ahí, $1.000 en análisis, $10.000 en
código, $100.000 en test y $1.000.000 en deploy (×10 por fase). Un modelo
iterativo detecta antes y baja tiempo y costo. Es el mismo mensaje del video
*Costs Shift Left*: el costo del error crece cuanto más avanzado está el
producto, así que hay que detectarlo lo antes posible.

**Ventana de Johari → costos** (competencia del PM: autoconocimiento):

| | Yo conozco | Yo no conozco |
|---|---|---|
| **Otros conocen** | Área pública → **incluir** | Área ciega → **juicio de expertos** |
| **Otros no conocen** | Área oculta → **incluir** | Área desconocida → **gestión de riesgos y aceptar** |

### 2.3 Desarrollar el Presupuesto

Sumar los costos estimados de las actividades o paquetes de trabajo para
establecer una **línea base de costos autorizada**.

- Entradas: plan de dirección (planes de gestión financiera y de recursos,
  línea base de alcance), documentos (base de las estimaciones, estimaciones de
  costos, cronograma, registro de riesgos), documentos de negocio (business
  case, plan de beneficios), acuerdos, factores ambientales, activos de la
  organización.
- Herramientas: juicio de expertos, **agregación de costos**, análisis de
  reservas, revisión de información histórica, **conciliación del límite de
  financiamiento**, financiación.
- Salidas: **línea base de costos**, **requisitos de financiamiento**,
  actualizaciones (estimaciones, cronograma, registro de riesgos).

**Componentes del presupuesto** (de abajo hacia arriba):

```
Estimaciones de costos de las actividades
  + Reserva para contingencias de las actividades
  = Estimaciones de costos de los paquetes de trabajo
  + Reserva para contingencias
  = Cuentas de control
  = LÍNEA BASE DE COSTOS (BAC)
  + Reserva de gestión
  = PRESUPUESTO DEL PROYECTO
```

**Reservas implícitas vs explícitas:** con reservas *implícitas* la contingencia
va metida dentro de la línea base y la reserva de gestión dentro del
presupuesto inicial; con reservas *explícitas* se muestran como bloques
separados encima de cada nivel. La recomendación práctica es hacerlas
explícitas: se ven, se miden y se pueden reportar.

**Curva S:** como las estimaciones están ligadas a las actividades del
cronograma, la línea base se puede ver por fases temporales: la curva S. Arriba
del BAC queda la reserva de gestión hasta el presupuesto del proyecto. Los
**requisitos de financiamiento** se dibujan como escalones (los fondos entran por
tramos) y los **gastos** como una curva que va detrás de la línea base.

**Ejemplos de presupuesto vistos en clase** (sirven de plantilla):

- *Project Budget Template* (CFI): por WBS, tiempo estimado vs real, tarifa
  estimada vs real, costo de mano de obra y de materiales, total estimado vs
  real y desvío.
- **Base de las estimaciones** por paquete: WBS ID, costos de recursos (físicos
  y humanos), costos directos, indirectos, **reserva de contingencia**,
  estimación, **método**, supuestos/restricciones, información adicional,
  **rango** y **nivel de confianza**.
- *Project Budget*: tareas con horas × tarifa, unidades × precio, materiales,
  viajes, otros; budget vs actual y under/(over).
- PV mensual y **PV acumulado** por actividad (el que alimenta la curva S).
- *Project Budgetary Analytics Tool (Budget vs. Actuals)*: por recurso y
  workstream, tarifa, presupuesto original, real a la fecha, ETC, EAC, variación
  y **burn rate** (% del presupuesto y % de horas consumidas contra lo esperado),
  con semáforo.

### 2.4 Monitorear y Controlar las Finanzas

Monitorear el estado del proyecto para actualizar los costos y **gestionar
cambios a la línea base de costos**.

- Para entender la ejecución del presupuesto hay que conocer los **costos reales**
  incurridos a la fecha.
- Cualquier incremento sobre el presupuesto autorizado se aprueba solo por el
  **Control Integrado de Cambios** (o según el modelo de gobernanza del
  proyecto).
- Gran parte del esfuerzo se dedica a **analizar la relación entre los fondos
  consumidos y el trabajo efectuado por esos gastos.**
- La clave de un control eficaz es **gestionar la línea base de costos
  aprobada**.

El control financiero incluye: monitorear el desempeño del trabajo contra lo
gastado; detectar y entender variaciones contra la línea base; influir sobre los
factores que la cambian; asegurar que los gastos no excedan los fondos
autorizados por período, por componente de la WBS, por actividad y en total;
procesar las solicitudes de cambio a tiempo; gestionar los cambios cuando
suceden; informar a los interesados los cambios aprobados y sus costos; y actuar
para mantener los excesos previstos dentro de límites aceptables.

ITTO de *Controlar los Costos*: entradas (plan de dirección con plan de costos,
línea base de costos y línea base de medición del desempeño; lecciones
aprendidas; requisitos de financiamiento; datos de desempeño del trabajo;
activos de la organización) → herramientas (juicio de expertos; **análisis del
valor ganado, de variación, de tendencias y de reservas**; **TCPI**; sistema de
información) → salidas (información de desempeño del trabajo, **pronósticos de
costos**, **solicitudes de cambio**, actualizaciones del plan y de los
documentos: supuestos, base de estimaciones, estimaciones, lecciones
aprendidas, riesgos).

## 3. Valor Ganado

El **análisis del valor ganado (EVA)** compara la línea base para la medición del
desempeño con el desempeño real del **cronograma** y del **costo**. El **EVM**
establece y monitorea tres dimensiones para cada paquete de trabajo y cada
cuenta de control:

1. **PV — Valor planificado**: presupuesto autorizado asignado al trabajo que
   debe ejecutarse para completar una actividad o un componente de la WBS.
2. **EV — Valor ganado**: medida del trabajo realizado expresada en términos del
   presupuesto autorizado para ese trabajo. Hay que establecer **criterios de
   medición del avance** para cada componente de la WBS.
3. **AC — Costo real**: costo incurrido por el trabajo realizado en una
   actividad durante un período específico.

**Análisis de variación**: la explicación (causa, impacto y acciones
correctivas) de las variaciones.

- **SV = EV − PV**: cuánto está adelantado o atrasado el proyecto respecto de la
  fecha de entrega, en un momento dado.
- **CV = EV − AC**: déficit o superávit presupuestario en un momento dado.
- **SPI = EV / PV**: eficiencia del cronograma.
- **CPI = EV / AC**: eficiencia del costo de los recursos presupuestados. **La
  cátedra la considera la métrica más crítica del EVA.**
- **VAC = BAC − EAC**: variación a la conclusión.

**Análisis de tendencias**: examina el desempeño a lo largo del tiempo para ver
si mejora o se deteriora, y compara el BAC con el EAC y las fechas de
conclusión.

**Pronóstico (EAC):** proyección de condiciones y eventos futuros basada en el
desempeño y el conocimiento disponibles. `EAC = AC + ETC ascendente`, o:

- ETC a la tasa presupuestada: `EAC = AC + (BAC − EV)`
- ETC con el CPI actual: `EAC = BAC / CPI`
- ETC considerando SPI y CPI: `EAC = AC + [(BAC − EV) / (CPI × SPI)]`

En el gráfico resumen: el **ETC** es el tramo de AC que falta hasta el EAC; el
**VAC** es la distancia entre EAC y BAC; el *schedule slippage* a la fecha es la
distancia horizontal entre EV y PV, y el *projected schedule slippage* es el
corrimiento de la fecha de fin.

## 4. Glosario de la cátedra (planilla *EVM_KPIs*)

| Sigla | Nombre | Definición | Fórmula | Interpretación |
|---|---|---|---|---|
| PV | Valor Planificado | Presupuesto autorizado asignado al trabajo planificado | — | Valor del trabajo que se planea cumplir hasta la fecha de corte |
| EV | Valor Ganado | Trabajo ejecutado a la fecha, en términos del presupuesto autorizado | Σ PV del trabajo completado | Sin referencia a los costos reales |
| AC | Costo Real | Costo incurrido por el trabajo en un período | — | Costo real del trabajo terminado a la fecha de corte |
| BAC | Presupuesto a la Conclusión | Suma de todos los presupuestos del trabajo | — | Valor total planificado: la línea base de costos |
| CV | Variación de Costo | Déficit o superávit presupuestario | EV − AC | + por debajo del costo · 0 en costo · − por encima |
| SV | Variación del Cronograma | Cuánto adelantado o atrasado, en dinero | EV − PV | + adelantado · 0 a tiempo · − retrasado |
| VAC | Variación a la Conclusión | Déficit o superávit proyectado al final | BAC − EAC | + cierra por debajo · 0 en costo · − por encima |
| CPI | Índice de Desempeño del Costo | Eficiencia de costos | EV / AC | > 1 por debajo del costo · 1 en costo · < 1 por encima |
| SPI | Índice de Desempeño del Cronograma | Eficiencia del cronograma | EV / PV | > 1 adelantado · 1 a tiempo · < 1 retrasado |
| EAC | Estimación a la Conclusión | Costo total previsto: AC + ETC | BAC/CPI (CPI se mantiene) · AC + BAC − EV (ritmo previsto) · AC + ETC ascendente (plan no válido) · AC + (BAC − EV)/(CPI×SPI) (ambos influyen) | |
| ETC | Estimación hasta la Conclusión | Costo previsto para terminar lo restante | EAC − AC · o reestimar de abajo hacia arriba | |
| TCPI | Índice de Desempeño del Trabajo por Completar | Eficiencia que hay que lograr con los recursos restantes | (BAC − EV)/(BAC − AC) para el BAC · (BAC − EV)/(EAC − AC) para el EAC | > 1 más difícil · 1 lo mismo · < 1 más fácil |

> **Dos errores en la planilla original de la cátedra**, corregidos arriba.
> Conviene saberlos para el examen:
> - En **VAC** la interpretación usa umbrales de índice ("mayor de 1,0"), pero
>   VAC es un monto: se lee positivo / cero / negativo.
> - En **CPI** la interpretación copiada es la del TCPI ("más difícil de
>   completar"). El CPI > 1 significa que se gastó menos de lo que vale lo hecho.

## 5. Ejercicios de clase, resueltos

1. PV = 2.200; EV = 2.000; AC = 2.500; BAC = 10.000. ¿CPI?
   `CPI = 2.000 / 2.500 = 0,80` → **B**: los costos reales excedieron lo
   planeado. (De paso: SPI = 0,91; CV = −500; SV = −200; EAC = BAC/CPI = 12.500;
   VAC = −2.500; TCPI = 8.000 / 7.500 = 1,07.)
2. ¿Qué representa el valor estimado del trabajo realizado? → **A**, el Valor
   Ganado (EV).
3. Un SPI de 0,76 significa... → **C**: se progresa solo un 76% de lo planeado.
4. EV = 350, AC = 400, PV = 325. ¿CV? `CV = 350 − 400 = −50` → **D**. (Ojo: el
   distractor −75 sale de PV − AC, que no es ninguna métrica.)
5. Una forma común de calcular el EAC es tomar el BAC y... → **D**, dividirlo
   por el CPI.
6. El EAC es una evaluación periódica de... → **C**: anticipar el total de los
   costos del proyecto al completarse. (D, "lo que va a costar terminar el
   trabajo", es el ETC.)

## 6. Material de la unidad que todavía no está cargado acá

Si la pregunta depende de esto, pedile el material al usuario en vez de
suponerlo:

- Simuladores *El (mal)Estimado del Dev* (antes de clase) y *LawnMaster+*
  (después).
- *Ejercicios para después del break* y *7 tips para estimar un proyecto*.
- *Portfolio Management — Análisis Financiero*: tareas Empresa H y Empresa S, y
  sus resoluciones.
- Ensayo *Costeo de proyectos en océanos azules* (lecturas *Red vs Blue
  Oceans*).
- *Using multiple currencies for global project costing* (opcional).
- Plantillas *Quick Project Budget Estimate* y *Project Budgetary Analytics Tool*.
- Lab interactivo del equipo: labs.mgiag.ar/lab4-valor-ganado.
