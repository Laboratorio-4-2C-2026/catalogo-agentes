#!/usr/bin/env node
/**
 * Recorre flujos de la app de Zest en un navegador y junta errores y warnings de consola.
 *
 * Uso:
 *   node console_check.mjs flows.json [--out reporte.json] [--headed] [--no-login]
 *
 * Login: si están ZEST_TEST_EMAIL y ZEST_TEST_PASSWORD, inicia sesión con Auth0 antes de los flujos.
 *
 * flows.json:
 * {
 *   "baseUrl": "http://localhost:5173",
 *   "flows": [
 *     { "ticket": "ZEST-120", "nombre": "Crear receta", "pasos": [
 *         { "goto": "/recipes/new" },
 *         { "fill": { "label": "Título", "value": "Prueba" } },
 *         { "click": { "role": "button", "name": "Guardar" } },
 *         { "waitFor": { "text": "Prueba" } },
 *         { "wait": 1000 }
 *     ] }
 *   ]
 * }
 * Pasos: goto, click {text | role+name | selector}, fill {label | placeholder | selector, value},
 *        press {key}, upload {selector, file}, waitFor {text | selector}, wait (ms).
 *
 * Código de salida: 0 = sin errores ni warnings, 1 = hay errores o warnings, 2 = no se pudo correr.
 */
import { chromium } from 'playwright'
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'

const args = process.argv.slice(2)
if (!args[0]) {
  console.error('Uso: node console_check.mjs flows.json [--out reporte.json] [--headed] [--no-login]')
  process.exit(2)
}
const opt = (name, def) => (args.includes(name) ? args[args.indexOf(name) + 1] : def)
const config = JSON.parse(readFileSync(args[0], 'utf8'))
const baseUrl = (config.baseUrl || 'http://localhost:5173').replace(/\/$/, '')
const outPath = resolve(opt('--out', 'reporte-consola.json'))
const shotsDir = resolve(dirname(outPath), 'capturas')
mkdirSync(shotsDir, { recursive: true })

// Ruido conocido que no es un problema de la app
const IGNORAR = [
  /Download the React DevTools/i,
  /\[vite\] (connecting|connected)/i,
  /\[HMR\]/i,
]
const ignorar = (texto) => IGNORAR.some((r) => r.test(texto))

function locator(page, t) {
  if (t.selector) return page.locator(t.selector).first()
  if (t.role) return page.getByRole(t.role, t.name ? { name: t.name } : {}).first()
  if (t.label) return page.getByLabel(t.label).first()
  if (t.placeholder) return page.getByPlaceholder(t.placeholder).first()
  if (t.text) return page.getByText(t.text).first()
  throw new Error(`Paso sin selector: ${JSON.stringify(t)}`)
}

async function runStep(page, paso) {
  if (paso.goto) return page.goto(baseUrl + paso.goto, { waitUntil: 'networkidle' })
  if (paso.click) return locator(page, paso.click).click()
  if (paso.fill) return locator(page, paso.fill).fill(String(paso.fill.value ?? ''))
  if (paso.press) return page.keyboard.press(paso.press.key)
  if (paso.upload) return page.locator(paso.upload.selector).setInputFiles(paso.upload.file)
  if (paso.waitFor) return locator(page, paso.waitFor).waitFor({ timeout: 15000 })
  if (paso.wait) return page.waitForTimeout(paso.wait)
  throw new Error(`Paso desconocido: ${JSON.stringify(paso)}`)
}

async function login(page) {
  const email = process.env.ZEST_TEST_EMAIL
  const password = process.env.ZEST_TEST_PASSWORD
  if (!email || !password) throw new Error('Faltan ZEST_TEST_EMAIL y ZEST_TEST_PASSWORD (o usá --no-login).')
  await page.goto(baseUrl + '/login', { waitUntil: 'networkidle' })
  await page.getByRole('button', { name: /log in/i }).first().click()
  await page.locator('input[name="username"], input#username, input[type="email"]').first().fill(email)
  const pwd = page.locator('input[name="password"], input#password').first()
  if (!(await pwd.isVisible().catch(() => false))) {
    await page.locator('button[type="submit"]').first().click() // flujo de dos pantallas
  }
  await pwd.fill(password)
  await page.locator('button[type="submit"][name="action"], button[type="submit"]').first().click()
  await page.waitForURL((url) => url.toString().startsWith(baseUrl), { timeout: 30000 })
  await page.waitForLoadState('networkidle')
}

const reporte = { fecha: new Date().toISOString(), baseUrl, flujos: [], totales: { errores: 0, warnings: 0, pasos_fallidos: 0 } }
let browser
try {
  browser = await chromium.launch({ headless: !args.includes('--headed') })
  const context = await browser.newContext()
  const page = await context.newPage()
  page.setDefaultTimeout(10000)

  let actual = null
  const registrar = (tipo, texto, extra = {}) => {
    if (!actual || ignorar(texto)) return
    actual[tipo === 'warning' ? 'warnings' : 'errores'].push({ texto: texto.slice(0, 500), url: page.url().replace(baseUrl, ''), ...extra })
  }
  page.on('console', (m) => {
    if (m.type() === 'error') registrar('error', m.text(), { origen: 'console.error' })
    else if (m.type() === 'warning') registrar('warning', m.text(), { origen: 'console.warn' })
  })
  page.on('pageerror', (e) => registrar('error', e.message, { origen: 'excepción no capturada' }))
  page.on('requestfailed', (r) => registrar('error', `${r.method()} ${r.url()} falló: ${r.failure()?.errorText}`, { origen: 'red' }))
  page.on('response', (r) => {
    if (r.status() >= 400 && !/auth0\.com/.test(r.url()))
      registrar(r.status() >= 500 ? 'error' : 'warning', `${r.request().method()} ${r.url()} → ${r.status()}`, { origen: 'HTTP' })
  })

  if (!args.includes('--no-login')) await login(page)

  for (const flujo of config.flows || []) {
    actual = { ticket: flujo.ticket, nombre: flujo.nombre, errores: [], warnings: [], paso_fallido: null }
    for (const [i, paso] of (flujo.pasos || []).entries()) {
      try {
        await runStep(page, paso)
      } catch (e) {
        const shot = resolve(shotsDir, `${flujo.ticket || 'flujo'}-paso${i + 1}.png`)
        await page.screenshot({ path: shot, fullPage: true }).catch(() => {})
        actual.paso_fallido = { paso: i + 1, detalle: JSON.stringify(paso), error: e.message.split('\n')[0], captura: shot }
        break
      }
    }
    await page.waitForTimeout(800) // errores asíncronos al final del flujo
    reporte.flujos.push(actual)
    reporte.totales.errores += actual.errores.length
    reporte.totales.warnings += actual.warnings.length
    reporte.totales.pasos_fallidos += actual.paso_fallido ? 1 : 0
    actual = null
  }
} catch (e) {
  reporte.error_general = e.message.split('\n')[0]
  writeFileSync(outPath, JSON.stringify(reporte, null, 2))
  console.log(JSON.stringify(reporte, null, 2))
  await browser?.close()
  process.exit(2)
}
await browser.close()
writeFileSync(outPath, JSON.stringify(reporte, null, 2))
console.log(JSON.stringify(reporte, null, 2))
const t = reporte.totales
process.exit(t.errores || t.warnings ? 1 : 0)
