# React Bits en el deck

[React Bits](https://reactbits.dev) es una biblioteca de componentes animados de
React que se **copian al proyecto** (pasan a ser código nuestro, no una
dependencia). Cada componente viene en cuatro variantes; la plantilla usa
**TS-TW** (TypeScript + Tailwind).

## Licencia

La versión gratuita es **MIT + Commons Clause**: se puede usar, modificar y
redistribuir, pero no vender el software. Para un proyecto de la facultad está
bien. El aviso de licencia está en
`plantilla/src/components/bits/LICENSE-react-bits.md` y se mantiene.

## Cómo agregar un componente

Por orden de preferencia:

1. **Desde el repo oficial** (funciona aunque reactbits.dev esté bloqueado):
   ```
   npm run add-bit -- Backgrounds/Silk
   ```
   Lo copia a `src/components/bits/` y avisa qué paquetes importa (`gsap`,
   `@gsap/react`, `motion`...). Los fondos actuales no tienen dependencias: usan
   WebGL directo.
2. **Con el CLI de shadcn** (requiere `components.json` en el deck):
   ```
   npx shadcn@latest add @react-bits/SplitText-TS-TW
   ```
3. **A mano**: pestaña *Code* del componente en reactbits.dev, variante TS-TW.

Después, envolvelo como hacen `Assertion` y `Background`: con modo estático
(`useDeck().isStatic`) que muestre el estado final, y con los colores Citrus.
Usá `trigger="load"` (o el equivalente) en vez de "al hacer scroll": el deck
monta solo la slide activa, así que "load" significa "al entrar a la slide".

## Ya incluidos en la plantilla

| Componente | Dónde | Notas |
|---|---|---|
| `SplitText` | Títulos (`Assertion`) | Palabra por palabra, efecto `rise` |
| `BlurText` | "Zest" en la portada | Letra por letra |
| `Grainient` | Portada y cierre (`Background kind="grainient"`) | Degradé con grano en grapefruit → coral → lemon |
| `Aurora` | Transición a la demo (`Background kind="aurora"`) | Sobre fondo oscuro |

No incluimos `CountUp`: no tiene coma decimal, y mostraría "1.36" en vez de
"1,36". `Metric` tiene su propio contador con formato argentino.

## Qué usar en cada slide

| Slide | Fondos sugeridos | Texto sugerido |
|---|---|---|
| Portada | `Grainient`, `Silk`, `SoftAurora`, `GradientWaves` | `BlurText`, `SplitText` |
| Transición de sección | `Threads`, `LineWaves`, `FloatingLines` | `SplitText`, `MaskedHeading` |
| Demo | `Aurora`, `LightRays`, `Hyperspeed` (con moderación) | `RotatingText` ("descubrir → guardar → organizar → planificar"), `TextType` |
| Datos (valor ganado, presupuesto) | ninguno: fondo liso | `Metric` (propio); `ShinyText` para resaltar un solo número |
| Riesgos | ninguno | `DecryptedText` para revelar el nivel, con mucha moderación |
| Cierre | El mismo de la portada, para cerrar el círculo | `BlurText` |

Evitar en un steering (distraen o cansan en un proyector): `Ballpit`, `EvilEye`,
`FaultyTerminal`, `LetterGlitch`, `CRTWarp`, `GlitchText`, `FuzzyText`,
`FallingText`.

## Catálogo gratuito (repo oficial, octubre 2026)

Nombres exactos para `npm run add-bit -- <Categoría>/<Nombre>`.

**Backgrounds (64):** AcidSquares, AeroShards, Antigravity, Aurora, Balatro,
Ballpit, Beams, CRTWarp, ColorBends, DarkVeil, Dither, DotField, DotGrid, EvilEye,
FaultyTerminal, Ferrofluid, FloatingLines, FluxLines, Galaxy, GhostFibers,
GradientASCII, GradientBlinds, GradientWaves, Grainient, GridDistortion,
GridMotion, GridScan, Hyperspeed, Iridescence, LetterGlitch, LightPillar,
LightRays, LightTunnel, Lightfall, Lightning, LineWaves, LiquidChrome,
LiquidEther, MagicRings, MagnetLines, MicroSlats, MoltenMetal, Orb, Particles,
PatternWaves, PixelBlast, PixelSnow, Plasma, PlasmaWave, Prism, PrismaticBurst,
Radar, RippleGrid, Scanner, ShapeGrid, ShapeWaves, SideRays, Silk, SlicedWaves,
SoftAurora, Threads, Topography, Waves, WebThreads.

**TextAnimations (33):** ASCIIText, BlurText, CircularText, CountUp, CurvedLoop,
DecryptedText, DepthText, EchoText, FallingText, FoldText, FuzzyText, GlitchText,
GradientText, MaskedHeading, ParticleText, RotatingText, ScrambledText,
ScrollFloat, ScrollReveal, ScrollVelocity, ShinyText, Shuffle, SplitFlapText,
SplitText, StrokeText, TechText, TextCursor, TextLoop, TextPressure, TextType,
TrueFocus, VariableProximity, WarpText.

Si un nombre no existe más, `add-bit` avisa: revisá
[el repo](https://github.com/DavidHDev/react-bits/tree/main/src/ts-tailwind).

## React Bits Pro: no se usa

[pro.reactbits.dev](https://pro.reactbits.dev) es paga y **el equipo no tiene
licencia**. Usá solo el catálogo gratuito de arriba. Si alguien pide un
componente de Pro, proponé el gratuito más parecido.
