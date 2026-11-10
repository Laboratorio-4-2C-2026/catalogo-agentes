# Plantilla de deck de Zest

Base para cada deck: se copia a `decks/<evento>/` y se llena. Cómo se usa, en
[`../SKILL.md`](../SKILL.md).

```bash
npm install
```

| Comando | Qué hace |
|---|---|
| `npm run dev` | Deck en el navegador. `P` abre la vista de presentador |
| `npm run build` | Compila (TypeScript estricto) |
| `npm run check` | Compila antes con `build`. Renderiza todas las slides, falla si algo se sale del marco, hay texto cortado o queda un dato de ejemplo, y deja capturas en `check/` |
| `npm run pdf` | Compila antes con `build`. Genera `deck.pdf`, una página por slide |
| `npm run add-bit -- Backgrounds/Silk` | Copia un componente de React Bits a `src/components/bits/` |

`check` y `pdf` usan Playwright. Si no está instalado:

```bash
npm i -D playwright && npx playwright install chromium
```

## Estructura

```
src/
  deck/         Deck (navegación, hash, sincronización), Stage (1920×1080 escalado),
                Presenter (vista de presentador), DeckContext (modo estático)
  components/   SlideFrame, Kicker, Assertion, Metric, SCurve, Background, ExampleBadge
  components/bits/  componentes de React Bits (licencia en LICENSE-react-bits.md)
  slides/       una slide por archivo; index.ts define el orden, títulos y notas
  data/         numbers.ts: todos los números, con fuente y fecha de corte
  styles/       tokens.css: paleta Citrus
scripts/        check, export-pdf, add-bit
```

## Cómo funciona

- **Escenario fijo**: cada slide mide 1920×1080 y se escala entera; nunca se
  reacomoda.
- **Solo se monta la slide activa**, así sus animaciones arrancan cada vez que
  se entra.
- **Modo estático** (`?print`, miniaturas del presentador,
  `prefers-reduced-motion`): los componentes muestran su estado final y los
  fondos WebGL se reemplazan por un degradé CSS, que imprime bien.
- **Vista de presentador** (`?presenter`): se sincroniza con la ventana del
  público por `BroadcastChannel`.

Las slides de ejemplo usan los números del Steering 2. La curva S tiene datos
de ejemplo y por eso `npm run check` falla a propósito hasta que se reemplacen.
