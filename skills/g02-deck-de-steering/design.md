# Reglas de diseño del deck

## 1. Aseveración + evidencia

- **El título es una oración completa que dice la conclusión.** "El planificador
  cierra el recorrido de Sofi", no "Planificador". "Vamos por encima del plan, y
  estamos revisando cuánto es mérito y cuánto método", no "Valor ganado".
- **El cuerpo es la prueba**: un número, un gráfico, una captura, una tabla
  corta. No párrafos.
- **Una idea por slide.** Si el título necesita "y" para dos cosas distintas, son
  dos slides.
- El título entra en **una o dos líneas**.
- **Los títulos solos cuentan la historia**: es la prueba del guion de títulos.

## 2. Densidad

| Modo | Cuándo | Límites |
|---|---|---|
| Presentada | Steering, demo, cualquier cosa que se dice en vivo | 1–3 puntos por slide, cuerpo ≥ 28 px, más slides si hace falta |
| De lectura | Anexo, deck que se manda por mail | 4–8 puntos o 4–6 tarjetas, tablas, cuerpo ≥ 24 px |

En los dos: nada de scroll, nada fuera del marco, nada superpuesto. **Si no
entra, se divide la slide; no se achica la letra.** Un minuto por slide como
referencia: si explicarla lleva más de dos, se divide.

## 3. Escenario

- Lienzo fijo de **1920×1080**, escalado entero a la pantalla (con bandas si la
  pantalla no es 16:9). Medidas fijas en px adentro del lienzo; nada de
  breakpoints.
- Márgenes de la plantilla: 120 px a los costados, 96 px arriba y abajo.
- Texto alineado a la izquierda; centrado solo en portada, demo y cierre.

## 4. Tipografía

| Uso | Familia | Tamaño |
|---|---|---|
| Títulos | Playfair Display | 64 / 88 / 120 px (`Assertion` md / lg / xl) |
| Portada | Playfair Display | 200–260 px |
| Kicker (etiqueta arriba del título) | Geist Mono, mayúsculas, espaciado | 18–22 px |
| Cuerpo | Geist | 28–40 px |
| Números grandes | Geist Mono, `tabular-nums` | 120 px o más |
| Fuentes, notas al pie | Geist Mono | 20 px |

Formato argentino siempre: `1.234,56`. Dos decimales para índices, dólares
enteros para montos.

## 5. Color

- Solo los tokens de Zest (`tailwind.config.ts` y `src/styles/tokens.css`), nunca
  un hex suelto en una slide.
- **Significado fijo en todo el deck**: lime = en camino / hecho, lemon = en
  curso / atención, grapefruit = alerta / pendiente. Nunca solo el color: siempre
  con la etiqueta o el número.
- Slides oscuras (`SlideFrame dark`) para portada, transiciones, demo y cierre.
  El resto, claras: se leen mejor en un proyector del aula.

## 6. Gráficos

- La curva S: PV punteado, EV grapefruit grueso, AC color texto, BAC como línea
  rotulada, línea del corte en lemon, **etiquetas al final de cada línea** en vez
  de leyenda.
- Un gráfico responde una pregunta, y el título de la slide es la respuesta.
- Ejes con pocas marcas. Sin grilla de fondo salvo que haga falta leer valores.
- Si el gráfico usa datos de ejemplo, lleva el cartel `ExampleBadge`.

## 7. Movimiento

- **Un efecto protagonista por slide** como máximo (un fondo WebGL **o** un
  título animado llamativo, no los dos compitiendo).
- Las animaciones se reproducen **una vez, al entrar**, y terminan en ~1 s. Nada
  que siga moviéndose detrás de una tabla o un gráfico que hay que leer. Los
  fondos animados, solo en portada, transiciones, demo y cierre.
- Entradas escalonadas (primero el título, después la evidencia) mejor que diez
  microanimaciones sueltas.
- `prefers-reduced-motion`, PDF y miniaturas del presentador: todo se muestra en
  su estado final (lo resuelve `useDeck().isStatic`).

## 8. Lista anti-"slop"

Lo que hace que un deck parezca hecho por una IA en cinco minutos:

- Títulos de tema ("Resultados", "Conclusiones") en vez de aseveraciones.
- Viñetas de diez palabras en todas las slides.
- Degradés violeta sobre blanco y paletas genéricas: acá la paleta es Citrus.
- Inter, Roboto o Arial: acá la tipografía es Playfair + Geist.
- La misma grilla de tres tarjetas en todas las slides.
- Íconos genéricos decorando cada punto.
- Efectos en todas las slides "porque se puede".
- Números sin fuente o sin fecha de corte.
- Textos internos que se escaparon a la slide ("Opción A", "TODO del prompt",
  nombres de archivo).
