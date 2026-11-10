# Cómo usar la skill de gestión del proyecto

Una guía para personas, no para el agente. Si sos quien tiene el rol de PM (o
estás estudiando para Dirección de Proyectos), acá está cómo sacarle el jugo.

## Qué hace

Te ayuda con todo lo que sea números del proyecto:

- **Calcular** PV, EV, AC, SV, CV, SPI, CPI, EAC, ETC, VAC y TCPI a una fecha de
  corte.
- **Auditar** un tablero ya armado: si el método de medición infla los índices,
  si los números cierran entre sí, qué te van a preguntar.
- **Pronosticar** cuánto va a costar terminar y si alcanza el presupuesto.
- **Estimar** esfuerzo y costo de algo nuevo (PERT, paramétrica, HH × tarifa).
- **Preparar** la lámina de valor ganado de un steering y sus repreguntas.
- **Estudiar**: explica la teoría como la da la cátedra y la aplica a Zest.

No es una calculadora: siempre te muestra la cuenta, de dónde sacó cada dato y
qué significa el resultado. Y nunca inventa un número: si le falta un dato, te
lo pide.

## Cómo llamarla

**En Claude Code, dentro de este repo (`zest-support`):** escribí `/zest-project-management`
seguido de lo que necesitás, o directamente pedí algo que tenga que ver con
presupuesto o valor ganado; Claude la carga solo.

```
/zest-project-management calculá el EVM al corte del jueves
```

**En otra herramienta (Cursor, ChatGPT, claude.ai):** pegá o adjuntá estos tres
archivos y después hacé tu pregunta:

1. [`../project-management.md`](./SKILL.md): lo específico de
   Zest.
2. [`evm-manual.md`](./evm-manual.md): el método.
3. [`course.md`](./course.md): la teoría de clase (solo si vas a estudiar).

## Qué tenés que darle

Cuanto mejores los datos, mejor la respuesta. Para un corte de EVM:

| Dato | De dónde lo sacás |
|---|---|
| Fecha de corte | La que vas a reportar (por lo general, el jueves de clase) |
| PV acumulado a esa fecha | Planilla *10B-Equipo 02 - EVM y Curva S*, hoja `PRESUPUESTO` |
| Tickets terminados por actividad | Multica, columna `done` (los de `in_review` no cuentan) |
| Horas reales por persona | El parte de horas de la planilla |
| Gastos no laborales | Consolas de Vercel, Render, Neon, S3 |

Si Claude tiene acceso al Drive o a Multica, los lee solo. Si no, pegale los
valores o una captura de la planilla.

## Ejemplos de pedidos

**Reporte semanal**

> Calculá el EVM al 05/11. PV acumulado 5.600, tickets done: [lista], horas
> reales: dev 190, gestión 300. Quiero los índices globales y los de desarrollo.

**Preparar el steering**

> Armame la lámina de valor ganado para el Steering 3 con dato → causa →
> acción, y las 5 repreguntas más probables con su respuesta.

**Auditar lo que ya presentamos**

> Revisá los números del Steering 2. ¿El SPI 1,36 se sostiene?

**Pronóstico**

> ¿Nos alcanza el presupuesto para llegar al 23/11? Usá ETC ascendente.

**Cambio de alcance**

> Nos piden agregar X. Estimalo, decime de dónde salen las horas y qué tiene
> que decir el control de cambios.

**Estimar algo nuevo**

> El planificador: optimista 10 h, más probable 16 h, pesimista 30 h. ¿Cuánto
> presupuesto con PERT y qué rango doy?

**Estudiar**

> Explicame la diferencia entre reserva de contingencia y reserva de gestión
> como la pide la cátedra, y aplicala a Zest.

> Tomame 5 preguntas tipo examen de valor ganado y corregime.

## Qué te devuelve

Para un cálculo, siempre en este orden:

1. **Los datos que usó**, con fuente y fecha de corte.
2. **La cuenta escrita**: `SPI = EV / PV = 6.124 / 4.493 = 1,36`.
3. **Qué significa para Zest**: comparado con el corte anterior, no como foto
   suelta.
4. **La decisión que pide y quién la toma** (PO, TL o PM).
5. **Las debilidades de la medición**, dichas antes de que te las pregunten.

## Lo que conviene saber antes de presentar

- En Zest el 66% del presupuesto es **nivel de esfuerzo** (gestión,
  infraestructura): gana valor con el calendario, no entregando funcionalidades.
  Por eso la skill siempre muestra dos juegos de índices: el global y el de
  desarrollo. El que mide avance real es el de desarrollo.
- Un **SPI o CPI alto no es para festejar**: es para revisar por qué dio así.
- Un **CV positivo no es plata ahorrada**: el dinero ya se gastó.
- Cerca del cierre **el SPI deja de servir** (tiende a 1). La skill usa el
  cronograma ganado y la ruta crítica.
- Si te piden "subir un poco" un número, la respuesta es no. Un número honesto
  bien explicado se defiende mejor.

## Mantenerla al día

Después de cada steering, actualizá en
[`../project-management.md`](./SKILL.md):

- **"Último corte conocido"**: los valores nuevos y la fecha.
- **"Composición del presupuesto"**: si hubo un cambio de línea base (v3,
  etc.), con la fecha del control de cambios.
- **"Hallazgos abiertos"**: tachá lo que se resolvió y agregá lo nuevo.

¿Tenés material nuevo de clase (ejercicios, simuladores, resoluciones)?
Sumalo a [`course.md`](./course.md); la lista de lo que falta está al final de
ese archivo.

¿La skill respondió algo mal o se inventó un dato? Abrí un issue "Skill /
convention miss" en este repo (ver `../README.md` (`zest-support/skills/README.md`)).
