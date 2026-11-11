---
name: g01-cinematch-demo-recording
description: "Graba un video de demo de la app web mobile-first de Cinematch manejándose sola (login, swipes, panel de detalle u otro flujo): Playwright hace los gestos en un viewport de celular, el screencast de Chrome captura los frames y ffmpeg los encodea dentro de un marco de teléfono dibujado. Usala para grabar o regrabar una demo, un walkthrough o un video de la app después de un cambio de UI; trae una implementación completa en examples/."
author: Tomás
metadata:
  tipo: skill
  area:
  - frontend
  fase:
  - revision
  tecnologias:
  - playwright
  - typescript
  - nodejs
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-steering-prep
  - g15-demo-recorder
---
# Recording a Cinematch demo

Cinematch is mobile-first and gesture-driven, so a demo has to show swipes and
drags on a phone-shaped screen with no mouse cursor. This skill builds that as
a scripted, reproducible recording rather than a hand-held screen capture, so
it can be re-recorded whenever the UI moves.

## Keep it outside the app repository

**The demo tooling lives in its own folder, never inside the app repository.**
It only needs the app running:

- It has its own `package.json` for the `@playwright/test` dependency and the
  browser download, so the app's dependencies are never touched.
- It reaches the app through its URL, `DEMO_APP_URL` (by default the local dev
  server), like any other visitor.
- Takes are tens of megabytes of JPEG frames plus the encoded video, so
  `recordings/` stays out of every repository.

## What the pipeline is

Three stages, each replaceable on its own:

1. **Drive.** Playwright opens the app at a phone viewport and performs the
   flow: typing, swipes, drags, scrolls.
2. **Capture.** Chrome's `Page.startScreencast` emits a JPEG whenever the page
   paints. Frames and their timestamps land on disk.
3. **Encode.** ffmpeg reads the frames through the concat demuxer and
   composites them inside a phone bezel, producing an mp4.

`examples/` holds a complete working implementation of all three. Copy it into
its own folder outside the app repository, install `@playwright/test` there,
and adapt the scenario; the capture and frame stages rarely need changing.

```
playwright.config.ts        phone viewport, forced scale factor, no recorder
cinematch-demo.spec.ts      the running order, readable as the demo itself
capture/
  recording-format.ts       screen size, capture scale, chromium arguments
  recorded-test.ts          the fixture that films a test on request
  screencast-recorder.ts    frames and their timings onto disk
scenario/
  app-selectors.ts          every test id and label of the app, to fill in
  demo-timing.ts            every pause in the video, in one place
  log-in.ts                 opening the screen, then the credentials
  swipe-the-deck.ts         like and dislike, with per-card variation
  pull-up-the-details-pane.ts
  pointer-gestures.ts       interpolated drags with an arc
  flick-scrolling.ts        in-page eased scrolling
frame/
  build-framed-video.mjs    entry point for the encode
  phone-frame.mjs           bezel geometry and SVG, pure
  rasterize-svg.mjs         SVG to transparent PNG, via the browser
  compose-framed-video.mjs  the ffmpeg filter graph
  image-dimensions.mjs      ffprobe
  ffmpeg-location.mjs       resolves ffmpeg, or fails with a usable message
```

Wire three scripts: record, frame, and one that does both. The scenario files
never mention recording, which is what makes a new flow cheap to write.

The bezel is drawn rather than shipped as an asset: geometry is derived from
the captured frame size, rendered to SVG, rasterized to a transparent PNG by
the browser that is already a dependency, then composited by ffmpeg twice, once
as the backdrop and once on top so its rounded inner edge clips the video's
square corners.

## Hard-won findings, do not rediscover these

**Playwright's own `recordVideo` is not good enough.** It captures at the CSS
viewport size, ignoring the device scale factor entirely, and its Chromium
encoder is pinned to VP8 at about 1 Mbit/s with no quality option. The result
looks like 360p and no setting improves it. This is why the capture stage uses
Chrome's screencast instead.

**`recordVideo` also pads rather than enlarges.** Asking for a video larger
than the viewport places the page in the top-left corner of a bigger canvas
with dead space around it. It only ever scales down.

**An emulated device scale factor does not raise capture resolution.** Setting
`deviceScaleFactor: 3`, which every Playwright device descriptor does, makes
`page.screenshot()` return 3x images but leaves screencast frames at CSS
pixels. Only a real one works: launch Chromium with
`--force-device-scale-factor=N` and `--window-size`, and set `viewport: null`
so the window itself is the viewport. The page still lays out at a phone's CSS
width, so the mobile layout is untouched. Playwright rejects `isMobile` in this
mode, which costs nothing, since layout follows the CSS viewport either way.

**Capture scale is a frame-rate dial.** Every frame is JPEG-encoded inside the
browser, so the cost is real: 3x throttles the capture to around 7fps and the
swipes stutter, while 2x holds 25 to 60fps. JPEG quality is the same dial;
dropping 92 to 80 measurably raises the frame count. **2x at quality 80 is the
sweet spot.**

**A device descriptor's viewport is not the phone's screen.** `iPhone 15` is
393x659, the browser content area with mobile browser UI subtracted. A demo
that draws a phone around the recording wants the full screen, so set the
viewport explicitly (393x852).

**Frames carry the demo's pacing, not a frame rate.** The screencast emits only
when the page paints, so a still moment produces no frames at all. Feed ffmpeg
through the concat demuxer with per-frame `duration` lines computed from the
timestamps. A fixed input frame rate makes still moments race past.

**An `overlay` filter inherits its timing from the backdrop.** Compositing onto
a looped still image pins the whole output to ffmpeg's default 25fps for image
loops, silently discarding a 60fps capture. Loop the image at the target rate
(`-framerate`) *and* apply `fps=` at the end of the filter chain, not on the
video branch.

**Gesture smoothness is not capture smoothness.** A dragged card only moves
when a pointer event reaches it, so the number of interpolated steps is the
gesture's own frame rate. Use around 50 steps per drag. Do not add a timer
between them: each `mouse.move` is already a protocol round trip that paces the
gesture, and a `waitForTimeout` on top doubles the wall clock for nothing. It
took a five-swipe take from 1.1m to 52s to remove it.

**Never scroll with wheel events.** Each one costs a round trip and moves the
scroll in a discrete jump, which reads as stuttering no matter how fast the
capture runs. Animate `scrollTop` from inside the page on `requestAnimationFrame`
instead: it runs on the browser's frame clock and lets the motion decelerate
like a flicked finger. See `examples/scenario/flick-scrolling.ts`.

**Start recording after the app has settled.** Web fonts swapping in and the
first layout landing are a visible twitch. Navigate, wait for the opening
element, await `document.fonts.ready`, and only then begin capture. The
recording fixture in `examples/capture/recorded-test.ts` exposes an explicit
`recording.start()` for exactly this.

## Natural-looking gestures

Identical repetitions look mechanical and pull attention away from the
product. Two cheap fixes, both in `examples/scenario/`:

- **Vary the gestures.** Keep a small table of swipe styles differing in travel
  distance, arc and step count, and bow each drag off the straight line by
  `arcPx * sin(π · progress)`.
- **Pick the variation deterministically**, by hashing the card's id rather
  than at random, so a rerun produces the identical video and the demo stays
  reproducible.

Ease the scroll rather than moving it linearly: `1 - (1-t)³` is fast off the
mark and settles, which is what a finger does. Coming back up should be quicker
than reading down.

## The app's own gesture thresholds

Read these from the swipe and detail pane components before choosing
distances, since they move: the horizontal travel that commits a like or
dislike, the upward drag that opens the detail pane (steeper than it is wide),
and the downward drag that closes it. The example assumes about 90px, 60px
and 60px.

Always overshoot a threshold comfortably so the gesture is unambiguous on
video and the like or dislike stamp reaches full opacity before the card
leaves.

Every test id, attribute and label the scenario uses lives in
`examples/scenario/app-selectors.ts`; fill it in from the app's source. Prefer
an attribute on the top card that carries the item's id: it is the reliable
way to assert a card left the deck. Check that any close button you use
belongs to the drawer the swipe flow opens, not to another modal with a
similar header.

## What the app needs running

The database, the backend and the frontend of the environment being demoed.

Use a dedicated demo account, registered against that environment before
recording. Pass it
through `DEMO_EMAIL` and `DEMO_PASSWORD`; the example refuses to run without
them, so no credential ever lives in the code.

## Pitfalls that cost time

- **`video.saveAs()` deadlocks in `afterEach`** if you still use Playwright's
  recorder: it waits for the recording to finalise, which only happens when the
  context closes, which the hook is blocking. Close the context first.
- **`getByLabel('Password')` is a substring match** and also hits the reveal
  toggle labelled "Show password". Pass `{ exact: true }`.
- **A device descriptor selects WebKit.** Spreading one into `use` changes the
  browser. Set `browserName: 'chromium'` explicitly, or do not spread it at
  all.
- **ffmpeg's PATH entry is not visible to an already-open shell** after
  installing it. Keep an environment variable escape hatch for its location,
  as `examples/frame/ffmpeg-location.mjs` does.

## Checking a take without watching it end to end

Measure rather than guess. `ffprobe` gives dimensions, duration and average
frame rate. Counting frame intervals in the capture's timeline shows how much
of the take is actually in motion: the share of intervals under 0.04s is the
number worth watching, and it should be most of them. A still sampled from the
video will not show compression artifacts, because a seek lands on a decoded
frame; trust the viewer's eyes over a sampled frame for anything about quality
in motion.

Aim for a demo between 30 and 60 seconds. Beats live in one file
(`examples/scenario/demo-timing.ts`) so the whole pace is tunable from there.

## Ejemplo de uso

**Pedido:** Grabá una demo de unos 40 segundos con el login, cinco swipes y el panel de detalle.

**Resultado:** Copia el pipeline de `examples/` a una carpeta propia, fuera del repo de la app, adapta el escenario y, con la app corriendo, genera un mp4 dentro de un marco de teléfono.
