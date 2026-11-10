---
name: g02-deck-de-steering
description: 'Usar para armar el deck de un Steering Committee de Zest (o cualquier presentación del proyecto) como una app web en React, Vite y Tailwind en vez de un PowerPoint: primero aprueba los títulos, después muestra tres estilos para elegir y construye con fondos y efectos de React Bits gratuitos, vista de presentador, chequeo automático de layout con capturas y exportación a PDF.'
metadata:
  tipo: skill
  area:
  - gestion
  - diseno
  fase:
  - revision
  tecnologias:
  - react
  - vite
  - typescript
  - tailwindcss
  - playwright
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
  madurez: probado
  relacionados:
  - g15-steering-deck-builder
  - g04-estructura-de-presentacion
  - g11-auditar-steering
  - g02-storytelling-de-demo
  - g02-valor-ganado-evm
---

# Deck de steering: mucho más que un PowerPoint

Arma el deck de un Steering Committee (o de cualquier presentación de Zest) como
una app web chica: escenario fijo de 16:9, animaciones de
[React Bits](https://reactbits.dev) con la marca Citrus, gráficos que se dibujan
solos, **vista de presentador** con notas y reloj, chequeo automático de layout
y exportación a PDF. Las slides se escriben en español.

La base ya existe y funciona: [`../plantilla/`](./plantilla). Esta
skill no arranca de cero: copia la plantilla y la llena.

## Archivos de este módulo

| Archivo | Qué tiene |
|---|---|
| Este archivo | El proceso, de punta a punta |
| [`steering-deck/README.md`](./guia-de-uso.md) | Guía para personas: cómo pedirlo, cómo presentar, atajos de teclado |
| [`steering-deck/design.md`](./design.md) | Reglas de diseño: aseveración + evidencia, densidad, tipografía, color, gráficos, movimiento, lista anti-"slop" |
| [`steering-deck/react-bits.md`](./react-bits.md) | Catálogo de React Bits (64 fondos, 33 efectos de texto), cuál usar en cada slide, cómo instalar y licencia (solo gratuitos) |
| [`../plantilla/README.md`](./plantilla/README.md) | Cómo está hecha la plantilla y sus comandos |

El contenido sale de las otras skills:

- Números (presupuesto, HH, PV/EV/AC, SPI/CPI, EAC) → `project-management.md` (skill `g02-valor-ganado-evm`)
- Historia, guion de demo y notas del presentador → `storytelling.md` (skill `g02-storytelling-de-demo`) (y su `decks/<evento>/demo.md`)
- Producto, equipo, alcance, hitos, riesgos → `../docs/product.md` (`zest-support/docs/product.md`)
- Decisiones difíciles sobre el contenido → `decision-committee.md` (skill `g02-comite-de-decisiones`)

## El proceso

### 0. Modo

- **Deck nuevo**: seguí todos los pasos.
- **Actualizar uno existente** (por ejemplo, el Steering 3 a partir del 2):
  copiá la carpeta del anterior, cambiá datos y slides, y saltá el paso 3.
- **Convertir un deck de Google Slides**: leelo con el conector de Drive si está
  disponible (si no, pedí que lo exporten), mostrá lo que extrajiste (títulos,
  notas, cantidad de imágenes) para que lo confirmen y seguí desde el paso 2.

### 1. Descubrimiento

En un solo mensaje, preguntá solo lo que falte:

- Evento, fecha y cuántos minutos dura la presentación.
- Quién presenta qué parte.
- Densidad: **presentada** (pocas palabras, la persona habla) o **de lectura**
  (se va a mandar por mail y se lee sola). Un steering es presentado; el anexo
  puede ser de lectura.
- Si ya existe `decks/<evento>/demo.md` (de storytelling), leelo y no repreguntes
  lo que ya dice.

Si contestan solo una parte, seguí con supuestos y escribilos.

### 2. Guion de títulos (antes de diseñar nada)

Escribí **solo los títulos** de todas las slides, como aseveraciones (oraciones
completas que dicen la conclusión, ver [`design.md`](./design.md)
§1), más una línea con la evidencia que va en cada una. Para un steering, partí de
la estructura que el comité ya conoce:

| # | Slide | Qué muestra |
|---|---|---|
| 1 | Portada | "Steering <n>", "Laboratorio II y IV", fecha, Zest |
| 2 | Equipo y roles | Los seis roles **de este steering** (rotan: ver `product.md`) |
| 3 | Visión del producto | El pitch del Charter |
| 4 | Avance por módulo | Módulos × backend / frontend / QA / total, por sprint |
| 5 | Cronograma | Gantt por etapa con la línea del corte, hitos y lo que cambió |
| 6 | Cambios de alcance | Qué entró, qué salió, horas y plata, si cambió el BAC |
| 7 | Presupuesto y esfuerzo | HH plan, tarifa, costo plan, HH reales; BAC, contingencia, reserva |
| 8 | Valor ganado | PV, EV, AC; SPI, CPI con la cuenta; índices globales **y** de desarrollo |
| 9 | Curva S | PV, EV, AC acumulados, BAC, corte, MVP |
| 10–11 | Riesgos | Amenazas y oportunidades: P, impacto, estrategia, respuesta |
| 12 | Próximos pasos | Tres o cuatro, numerados |
| 13 | Demo | Transición a pantalla completa; el guion está en `demo.md` |
| 14 | Gracias / preguntas | |
| — | Anexo | Matriz de probabilidad e impacto, tablas de detalle |

**Prueba del guion:** leídos uno tras otro, los títulos tienen que contar la
historia completa. Si un título necesita "y", son dos slides. Mostrá el guion y
**esperá el visto bueno** antes de construir: corregir títulos cuesta minutos;
corregir slides, horas.

### 3. Dirección visual: tres opciones para elegir

No describas estilos con palabras: **mostralos**. Armá tres previews (portada +
una slide de datos, por ejemplo valor ganado), sacales captura y mostralas:

1. **Citrus editorial** (la segura): fondo crema, Playfair grande, un fondo
   animado solo en portada y cierre.
2. **Cocina de noche** (la audaz): slides oscuras, acentos grapefruit y lemon,
   fondo WebGL sutil en las de transición.
3. **Comodín**: una propuesta propia con una idea visual fuerte (por ejemplo, una
   grilla de recetas como hilo visual), siempre dentro de la paleta Citrus.

Las tres usan los tokens de Zest; cambian la composición, el contraste y los
efectos, no la marca. En las previews nunca aparecen textos internos ("Opción A",
nombres de archivo, notas del pedido). Que elijan una, o que mezclen.

### 4. Construir

1. `cp -r plantilla decks/<evento>` y `npm install` adentro.
2. **Datos primero**: todo número va en `src/data/numbers.ts` con su fuente y su
   fecha de corte. Nunca un número escrito adentro de una slide. Lo que todavía
   no se tiene queda con `isExample: true`, que pone el cartel "DATO DE EJEMPLO".
3. **Una slide por archivo** en `src/slides/`, registrada en
   `src/slides/index.ts` con su `title` (la aseveración) y sus `notes` (lo que se
   dice, sacado del guion de storytelling).
4. Usá los bloques de la plantilla: `SlideFrame`, `Kicker`, `Assertion`,
   `Metric`, `SCurve`, `Background`. Si hace falta uno nuevo (Gantt, tabla de
   riesgos, matriz), creálo en `src/components/` con el mismo estilo y con modo
   estático (`useDeck().isStatic`).
5. **React Bits** según [`react-bits.md`](./react-bits.md): como
   máximo un efecto protagonista por slide. Para sumar uno:
   `npm run add-bit -- Backgrounds/Silk`.
6. La demo en vivo no va adentro del deck: la slide de demo es una transición, y
   el plan B (grabación o capturas) se tiene abierto aparte.

### 5. Verificar (siempre, antes de mostrar nada)

1. `npm run build`: sin errores de TypeScript.
2. `npm run check`: renderiza todas las slides y **falla** si algo se sale del
   marco 1920×1080, si hay texto cortado o si queda un "DATO DE EJEMPLO". Deja
   capturas en `check/` (estáticas a 1920×1080 y en vivo a 1280×720).
3. **Mirá las capturas, una por una.** El script no ve superposiciones de
   etiquetas, contraste pobre ni slides desbalanceadas. Corregí y volvé a correr
   hasta que estén bien.
4. Revisá los números contra la fuente y que las cuentas cierren
   (SPI = EV / PV, CPI = EV / AC).
5. Nombres y roles de este steering.

### 6. Entregar

- `npm run dev` para presentar; `P` abre la vista de presentador en otra
  ventana.
- `npm run pdf` genera `deck.pdf` (una página por slide, animaciones en su
  estado final): es el respaldo si falla la compu.
- Resumí: dónde quedó, cuántas slides, qué estilo, cómo se presenta y qué quedó
  como ejemplo o pendiente.
- **Este repo es público.** El deck se puede versionar acá, pero sin
  credenciales, sin mails ni datos de usuarios reales. No publiques el deck en una URL pública sin que el equipo lo pida.

## Reglas que no se negocian

- Ningún número inventado: si falta, `TODO` visible o `isExample` y se pregunta.
- Ninguna funcionalidad que no esté terminada se muestra como hecha (ver
  `storytelling.md`).
- El escenario es fijo de 1920×1080 y se escala entero: nada de layouts que se
  reacomodan.
- Animaciones que se reproducen una vez al entrar a la slide y respetan
  `prefers-reduced-motion`.
- `npm run check` pasa y el PDF está exportado antes de presentar.
- No se toca el repo `zest`: el deck vive en `zest-support/decks/`.

## De dónde salen estas ideas

- **frontend-slides** (skill de Claude Code para decks en HTML, más de 15k
  estrellas): escenario fijo 1920×1080 escalado, previews visuales para elegir el
  estilo, densidad presentada vs. de lectura, lista anti-"slop", verificación con
  capturas, PDF con Playwright.
  [github.com/zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)
- **Aseveración + evidencia**: títulos como oraciones completas con evidencia
  visual; una idea por slide.
  [Harvard Catalyst](https://catalyst.harvard.edu/writing-communication-center/visualize-science/slides),
  [CMU](https://www.cmu.edu/student-success/other-resources/handouts/comm-supp-pdfs/designing-powerpoint-slides.pdf).
- **React Bits** (versión gratuita): ver [`react-bits.md`](./react-bits.md).

## Ejemplo de uso

**Pedido:** "Armame el deck del Steering 3 a partir del Steering 2."

**Resultado:** Propone los títulos de las 16 slides como aseveraciones y espera la aprobación, muestra capturas de tres estilos (Citrus editorial, Cocina de noche y Recetario) con la portada y la slide de valor ganado, copia la plantilla, construye las slides con los números en un solo archivo con su fuente, corre el chequeo de layout, revisa cada captura y exporta el PDF de respaldo.
