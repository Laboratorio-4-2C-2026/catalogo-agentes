// Plantilla de grabación de demos (ver la skill demo-video). Captura cuadros por CDP (cada uno
// con su marca de tiempo), así los tramos poco importantes se aceleran sin desfasar nada.
// Subtítulos, cursor y placas se dibujan dentro de la página.
//
// Por video se editan tres cosas: la configuración de acá abajo, el bloque SLIDES y el guion
// de escenas dentro de `scenes()`. El resto es maquinaria y no hace falta tocarlo.
import { execFileSync } from 'node:child_process'
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import ffmpeg from 'ffmpeg-static'
import { chromium } from 'playwright'
import { PASSWORD } from './seed.mjs'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const APP = process.env.APP_URL ?? 'http://localhost:5173'
const OUT = path.join(HERE, 'output')
/** Nombre del MP4 y del SRT. */
const NAME = process.env.DEMO_NAME ?? 'mi-app-demo'
/** Tope duro: si el video se pasa, no se exporta nada. */
const MAX_SECONDS = Number(process.env.DEMO_MAX_SECONDS ?? 60)
/** Imagen de carátula. Las placas siguientes copian su estilo. */
const COVER_FILE = process.env.DEMO_COVER ?? path.join(HERE, '..', '..', 'portada.png')
// 1440×810 CSS a 4/3 de densidad: cuadros de 1920×1080 sin reescalar.
const VIEWPORT = { width: 1440, height: 810 }
const SCALE = 4 / 3

const COVER = `data:image/png;base64,${readFileSync(COVER_FILE).toString('base64')}`
const fontFace = (weight) => {
  const file = path.join(HERE, 'node_modules', '@fontsource', 'raleway', 'files', `raleway-latin-${weight}-normal.woff2`)
  return `@font-face{font-family:Raleway;font-weight:${weight};font-display:block;src:url(data:font/woff2;base64,${readFileSync(file).toString('base64')}) format('woff2')}`
}
const FONTS = [500, 600, 700].map(fontFace).join('')

// Escalera con flecha, del mismo trazo y color que la ilustración de la portada.
const ARROW = `
<svg class="arrow" viewBox="0 150 880 580" aria-hidden="true">
  <g fill="#747BE6" stroke="#747BE6">
    <path d="M40 660 L400 632 L400 470 L690 444 L748 328" fill="none" stroke-width="78" stroke-linejoin="miter"/>
    <polygon points="812,196 832,386 648,294" stroke-width="6" stroke-linejoin="round"/>
  </g>
</svg>`

const slide = ({ eyebrow, title, sub }) =>
  `<div class="s"><p class="eyebrow">${eyebrow}</p><h1>${title}</h1>${sub ? `<p class="sub">${sub}</p>` : ''}</div>${ARROW}`

// ── Placas ─────────────────────────────────────────────────────────────────
// La portada es la imagen; las demás se arman con el mismo estilo. Editar por video.
const SLIDES = {
  cover: `<img class="cover" src="${COVER}" alt="">`,
  handoff: slide({
    eyebrow: 'Del otro lado',
    title: 'Mientras<br>tanto…',
    sub: '<b>Tomás</b> abre la app en su computadora',
  }),
  end: slide({
    eyebrow: 'Demo de sprint · Fecha',
    title: '¡Gracias!',
    sub: '<b>Integrantes:</b> Nombre Apellido - Nombre Apellido -<br>Nombre Apellido - Nombre Apellido',
  }),
}

const OVERLAY = ({ fonts }) => {
  const STYLE = `${fonts}
    #demo-cursor{position:fixed;left:-50px;top:-50px;width:22px;height:22px;z-index:2147483647;pointer-events:none;
      transform:translate(-3px,-2px);filter:drop-shadow(0 1px 2px rgba(0,0,0,.35))}
    #demo-cursor.down{transform:translate(-3px,-2px) scale(.85)}
    .demo-ripple{position:fixed;width:34px;height:34px;margin:-17px 0 0 -17px;border-radius:50%;z-index:2147483646;
      pointer-events:none;background:rgba(116,123,230,.4);animation:demo-ripple .45s ease-out forwards}
    @keyframes demo-ripple{from{transform:scale(.3);opacity:1}to{transform:scale(1.6);opacity:0}}
    #demo-caption{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);z-index:2147483645;pointer-events:none;
      max-width:78%;padding:9px 20px 10px;border-radius:10px;background:rgba(17,17,17,.84);color:#fff;
      font:600 21px/1.35 Raleway,system-ui,sans-serif;letter-spacing:-.01em;text-align:center;
      transition:opacity .25s,bottom .25s;opacity:0}
    #demo-caption.on{opacity:1}
    #demo-card{position:fixed;inset:0;z-index:2147483646;background:#FAFAFA;color:#000;overflow:hidden;
      pointer-events:none;transition:opacity .5s;opacity:0}
    #demo-card.on{opacity:1}
    #demo-card .cover{display:block;width:100%;height:100%;object-fit:cover}
    #demo-card .s{position:absolute;left:6.15vw;top:50%;transform:translateY(-50%)}
    #demo-card .eyebrow{margin:0 0 2.4vw;font:700 1.36vw/1.2 Arial,Helvetica,sans-serif;color:#535AC8}
    #demo-card h1{margin:0;font:500 9.4vw/.86 Raleway,sans-serif;letter-spacing:-.05em}
    #demo-card .sub{margin:2.6vw 0 0;font:500 1.8vw/1.25 Raleway,sans-serif;letter-spacing:-.03em}
    #demo-card .sub b{font-weight:700}
    #demo-card .arrow{position:absolute;right:4vw;top:50%;width:40vw;transform:translateY(-45%)}
    body:has(#demo-card.on) #demo-cursor{opacity:0}`

  const mount = () => {
    if (document.getElementById('demo-cursor')) return
    const style = document.createElement('style')
    style.textContent = STYLE
    document.head.append(style)

    const cursor = document.createElement('div')
    cursor.id = 'demo-cursor'
    cursor.innerHTML =
      '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M4 2l16 10-7 1.5L9.5 21z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>'
    const caption = document.createElement('div')
    caption.id = 'demo-caption'
    const card = document.createElement('div')
    card.id = 'demo-card'
    document.body.append(cursor, caption, card)

    const read = () => JSON.parse(localStorage.getItem('demo-state') ?? '{}')
    const save = (patch) => localStorage.setItem('demo-state', JSON.stringify({ ...read(), ...patch }))
    const state = read()
    if (state.x !== undefined) {
      cursor.style.left = `${state.x}px`
      cursor.style.top = `${state.y}px`
    }
    // Una placa abierta antes de navegar sigue tapando la página nueva desde el primer cuadro.
    if (state.card) {
      card.style.transition = 'none'
      card.innerHTML = state.card
      card.classList.add('on')
    }

    document.addEventListener('mousemove', (e) => {
      cursor.style.left = `${e.clientX}px`
      cursor.style.top = `${e.clientY}px`
      save({ x: e.clientX, y: e.clientY })
    }, true)
    document.addEventListener('mousedown', (e) => {
      cursor.classList.add('down')
      const ripple = document.createElement('div')
      ripple.className = 'demo-ripple'
      ripple.style.left = `${e.clientX}px`
      ripple.style.top = `${e.clientY}px`
      document.body.append(ripple)
      setTimeout(() => ripple.remove(), 500)
    }, true)
    document.addEventListener('mouseup', () => cursor.classList.remove('down'), true)

    // Los toasts de la app salen abajo al centro: mientras haya uno, el subtítulo se corre arriba.
    setInterval(() => {
      const toasts = [...document.querySelectorAll('[data-sonner-toast]')]
      const top = Math.min(...toasts.map((t) => t.getBoundingClientRect().top), innerHeight)
      caption.style.bottom = `${top < innerHeight ? innerHeight - top + 12 : 28}px`
    }, 60)

    window.demo = {
      caption(text) {
        caption.classList.remove('on')
        if (text) setTimeout(() => { caption.textContent = text; caption.classList.add('on') }, 120)
      },
      card(html) {
        card.style.transition = ''
        if (html) card.innerHTML = html
        card.classList.toggle('on', Boolean(html))
        save({ card: html })
      },
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount)
  else mount()
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function main() {
  rmSync(OUT, { recursive: true, force: true })
  const framesDir = path.join(OUT, 'frames')
  mkdirSync(framesDir, { recursive: true })

  const browser = await chromium.launch()
  const context = await browser.newContext({
    viewport: VIEWPORT,
    deviceScaleFactor: SCALE,
    locale: 'es-AR',
    timezoneId: 'America/Argentina/Buenos_Aires',
  })
  await context.addInitScript(OVERLAY, { fonts: FONTS })
  const page = await context.newPage()
  page.setDefaultTimeout(15000)

  const frames = []
  let capturing = false
  const cdp = await context.newCDPSession(page)
  cdp.on('Page.screencastFrame', ({ data, metadata, sessionId }) => {
    cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {})
    if (!capturing) return
    const file = path.join(framesDir, `${String(frames.length).padStart(6, '0')}.jpg`)
    writeFileSync(file, Buffer.from(data, 'base64'))
    frames.push({ at: metadata.timestamp * 1000, file })
  })

  const cues = []
  const speedups = []
  let startAt = 0
  let endAt = 0

  /** Milisegundos de video entre dos instantes de reloj, descontando lo que comprime cada tramo acelerado. */
  const videoMs = (from, to) => {
    let ms = to - from
    for (const { start, end, factor } of speedups) {
      ms -= Math.max(0, Math.min(to, end) - Math.max(from, start)) * (1 - 1 / factor)
    }
    return ms
  }

  const caption = async (text) => {
    // Cada subtítulo queda en pantalla lo necesario para leerlo, medido en tiempo de video.
    const current = cues.at(-1)
    if (current && current.end === null) {
      const needed = Math.max(1500, current.text.split(/\s+/).length * 300)
      const remaining = needed - videoMs(current.start, Date.now())
      if (remaining > 0) await wait(remaining)
    }
    const now = Date.now()
    if (cues.length && cues.at(-1).end === null) cues.at(-1).end = now
    if (text) cues.push({ start: now + 120, end: null, text })
    await page.evaluate((t) => window.demo.caption(t), text)
    if (text) await wait(600)
  }
  const card = async (html) => {
    await caption(null)
    await page.evaluate((h) => window.demo.card(h), html)
    await wait(550)
  }
  /** Lo que se muestra pero importa poco (los logins) va más rápido. */
  const fast = async (factor, scene) => {
    const start = Date.now()
    await scene()
    speedups.push({ start, end: Date.now(), factor })
  }
  const moveTo = async (locator) => {
    await locator.scrollIntoViewIfNeeded()
    const box = await locator.boundingBox()
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 17 })
    await wait(160)
  }
  const click = async (locator) => {
    await moveTo(locator)
    await locator.click()
    await wait(230)
  }
  const type = async (locator, text, delay = 35) => {
    await click(locator)
    await locator.pressSequentially(text, { delay })
    await wait(150)
  }
  const login = async (who, email) => {
    await caption(`${who} inicia sesión`)
    await fast(2.5, async () => {
      await type(page.getByLabel('Email'), email, 25)
      await type(page.getByLabel('Contraseña', { exact: true }), PASSWORD, 25)
      await click(page.getByRole('button', { name: 'Iniciar sesión' }))
      // El login devuelve a la ruta pedida antes de entrar, así se saltean las intermedias.
      await page.waitForURL('**/groups')
      await page.getByRole('heading', { level: 1, name: 'Grupos' }).waitFor()
    })
  }
  const sidebar = page.locator('[data-sidebar="sidebar"]')

  // ── GUION ──────────────────────────────────────────────────────────────
  // Lo único que cambia de un video a otro; lo que sigue es un ejemplo y se reemplaza entero.
  // Herramientas disponibles:
  //   caption(texto)               subtítulo; queda el tiempo necesario para leerlo
  //   card(SLIDES.x) / card(null)  abre y cierra una placa
  //   fast(2.5, async () => {})    acelera un tramo que importa menos (los logins)
  //   moveTo / click / type        mueven el cursor dibujado y actúan
  //   login(nombre, email)         entra y espera la ruta de destino del flujo
  try {
    // ── Portada ──────────────────────────────────────────────────────────
    await page.goto(`${APP}/groups`)
    await page.getByLabel('Email').waitFor()
    await page.evaluate(() => localStorage.setItem('demo-state', JSON.stringify({ x: 720, y: 560 })))
    await page.evaluate((h) => window.demo.card(h), SLIDES.cover)
    await page.evaluate(() => document.fonts.ready)
    await wait(700)
    await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080 })
    await wait(300)
    // El screencast solo manda cuadros cuando algo cambia: la portada quieta no llegaría nunca.
    startAt = Date.now()
    const coverFrame = path.join(framesDir, 'cover.jpg')
    await page.screenshot({ path: coverFrame, type: 'jpeg', quality: 95, scale: 'device' })
    frames.push({ at: startAt, file: coverFrame })
    capturing = true
    await wait(2800)
    await card(null)

    // ── Martina ──────────────────────────────────────────────────────────
    await login('Martina', 'martina.lopez@demo.com')

    await caption('Martina ve todos sus grupos: los que administra y en los que participa')
    for (const name of ['Análisis Matemático II', 'Bases de Datos', 'Inglés Técnico']) {
      await moveTo(page.getByRole('link', { name: `Ver ${name}` }))
      await wait(200)
    }

    await caption('Entra a Análisis Matemático II')
    await click(page.getByRole('link', { name: 'Ver Análisis Matemático II' }))
    await page.getByRole('heading', { level: 1, name: 'Análisis Matemático II' }).waitFor()
    await wait(1000)

    await caption('Y cambia a Bases de Datos desde la barra lateral')
    await click(sidebar.getByRole('link', { name: 'Bases de Datos' }))
    await page.getByRole('heading', { level: 1, name: 'Bases de Datos' }).waitFor()
    await wait(900)

    await caption('Programa una sesión de estudio para mañana')
    await click(page.getByRole('button', { name: 'Crear sesión' }))
    const sessionDialog = page.getByRole('dialog', { name: 'Crear sesión de estudio' })
    await sessionDialog.waitFor()
    await type(sessionDialog.getByLabel('Nombre de la sesión'), 'Repaso de SQL para el parcial', 28)
    await click(sessionDialog.getByText('Programada', { exact: true }))
    const startsAt = sessionDialog.getByLabel('Fecha y hora')
    await moveTo(startsAt)
    const tomorrow = await page.evaluate(() => {
      const d = new Date(Date.now() + 86_400_000)
      const pad = (n) => String(n).padStart(2, '0')
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T18:00`
    })
    await startsAt.fill(tomorrow)
    await wait(400)

    await caption('Elige la duración del enfoque, del descanso y los ciclos')
    // 45 y no 50: la última opción del desplegable cae detrás del subtítulo.
    for (const [label, option] of [['Enfoque (min)', '45'], ['Descanso (min)', '10']]) {
      await click(sessionDialog.getByLabel(label))
      await click(page.getByRole('option', { name: option, exact: true }))
    }
    await moveTo(sessionDialog.getByText('Duración total de la sesión'))
    await wait(500)
    await click(sessionDialog.getByRole('button', { name: 'Programar sesión' }))
    await sessionDialog.waitFor({ state: 'hidden' })
    await caption('La sesión queda programada para mañana a las 18:00')
    await wait(900)

    await caption('Ahora invita a Tomás al grupo')
    await click(page.getByRole('button', { name: 'Invitar' }))
    const inviteDialog = page.getByRole('dialog', { name: 'Invitar al grupo' })
    await inviteDialog.waitFor()
    await type(inviteDialog.getByLabel('Buscar'), 'tomas', 45)
    const tomasRow = inviteDialog.getByRole('listitem').filter({ hasText: 'Tomás Ruiz' })
    await tomasRow.waitFor()
    await wait(300)
    await click(tomasRow.getByRole('button', { name: 'Invitar' }))
    await page.getByText('Invitación enviada').waitFor()
    await caption('Tomás queda invitado')
    await wait(700)
    await page.keyboard.press('Escape')
    await wait(250)

    // ── Transición ───────────────────────────────────────────────────────
    await card(SLIDES.handoff)
    await page.evaluate(() => sessionStorage.clear())
    // Mientras la página recarga hay cuadros en blanco antes de que se vuelva a pintar la placa:
    // se congela la captura y se retoma con un cuadro forzado de la placa ya pintada.
    capturing = false
    await page.goto(`${APP}/groups`)
    await page.getByLabel('Email').waitFor()
    await page.evaluate(() => document.fonts.ready)
    await wait(200)
    const handoffFrame = path.join(framesDir, 'handoff.jpg')
    await page.screenshot({ path: handoffFrame, type: 'jpeg', quality: 95, scale: 'device' })
    frames.push({ at: Date.now(), file: handoffFrame })
    capturing = true
    await wait(1800)
    await card(null)

    // ── Tomás ────────────────────────────────────────────────────────────
    await login('Tomás', 'tomas.ruiz@demo.com')

    const bell = page.getByRole('button', { name: 'Invitaciones (1 pendientes)' })
    await bell.waitFor()
    await caption('Tiene una invitación pendiente')
    await click(bell)
    await wait(450)
    await caption('La acepta y se une a Bases de Datos')
    await click(page.getByRole('button', { name: 'Aceptar' }))
    await page.getByText('Te uniste al grupo').waitFor()
    await wait(500)
    await page.keyboard.press('Escape')

    const navGroup = sidebar.getByRole('link', { name: 'Bases de Datos' })
    await navGroup.waitFor()
    await caption('El grupo ya aparece en su pantalla y en la barra lateral')
    await moveTo(page.getByRole('link', { name: 'Ver Bases de Datos' }))
    await wait(450)
    await click(navGroup)
    const heading = page.getByRole('heading', { level: 1, name: 'Bases de Datos' })
    await heading.waitFor()

    await caption('Adentro ve la descripción y los miembros del grupo')
    await moveTo(heading)
    await wait(500)
    const members = page
      .locator('[data-slot="card"]')
      .filter({ has: page.getByRole('heading', { name: 'Miembros' }) })
      .getByRole('listitem')
    for (let i = 0; i < (await members.count()); i++) await moveTo(members.nth(i))
    await wait(900)

    // ── Cierre ───────────────────────────────────────────────────────────
    await card(SLIDES.end)
    await wait(2200)
    endAt = Date.now()
  } catch (error) {
    await page.screenshot({ path: path.join(OUT, 'error.png') })
    await browser.close()
    throw error
  }

  capturing = false
  await cdp.send('Page.stopScreencast')
  await browser.close()

  const toVideo = (at) => videoMs(startAt, Math.min(Math.max(at, startAt), endAt)) / 1000

  const total = toVideo(endAt)
  console.log(`duración: ${total.toFixed(1)} s (${frames.length} cuadros)`)
  if (total > MAX_SECONDS) throw new Error(`La demo dura ${total.toFixed(1)} s y el máximo es ${MAX_SECONDS} s`)

  const list = []
  frames.forEach((frame, i) => {
    const next = frames[i + 1]?.at ?? endAt
    const duration = toVideo(next) - toVideo(frame.at)
    if (duration <= 0) return
    list.push(`file '${frame.file.replaceAll('\\', '/')}'`, `duration ${duration.toFixed(4)}`)
  })
  // El demuxer ignora la duración del último archivo si no se repite.
  list.push(`file '${frames.at(-1).file.replaceAll('\\', '/')}'`)
  const listFile = path.join(OUT, 'frames.txt')
  writeFileSync(listFile, list.join('\n'))

  const mp4 = path.join(OUT, `${NAME}.mp4`)
  execFileSync(ffmpeg, [
    '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listFile,
    '-vf', 'fps=30,scale=1920:1080:flags=lanczos,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-movflags', '+faststart', mp4,
  ], { stdio: 'inherit' })

  const stamp = (seconds) => {
    const ms = Math.round(seconds * 1000)
    const h = String(Math.floor(ms / 3_600_000)).padStart(2, '0')
    const m = String(Math.floor(ms / 60_000) % 60).padStart(2, '0')
    const s = String(Math.floor(ms / 1000) % 60).padStart(2, '0')
    return `${h}:${m}:${s},${String(ms % 1000).padStart(3, '0')}`
  }
  const srt = cues
    .map((cue, i) => `${i + 1}\n${stamp(toVideo(cue.start))} --> ${stamp(toVideo(cue.end ?? endAt))}\n${cue.text}\n`)
    .join('\n')
  // Con BOM: sin él, varios reproductores de Windows leen mal los acentos.
  writeFileSync(path.join(OUT, `${NAME}.srt`), `﻿${srt}`)

  rmSync(framesDir, { recursive: true, force: true })
  rmSync(listFile)
  console.log(`listo: ${mp4}`)
}

await main()
