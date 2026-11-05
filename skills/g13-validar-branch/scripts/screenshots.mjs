#!/usr/bin/env node
// Saca screenshots del front local, logueado con usuarios demo.
//
//   node screenshots.mjs <tomas.json> <carpeta de salida> [--backend <ruta>]
//
// (desde la raíz de microchangas-frontend; --backend por defecto
//  ../microchangas-backend, de donde lee DEMO_USERS_PASSWORD)
//
// tomas.json:
// [
//   { "nombre": "dashboard-worker", "como": "worker", "ruta": "/dashboard" },
//   { "nombre": "nueva-changa-error", "como": "client", "ruta": "/changas/nueva",
//     "pasos": [
//       { "click": "button[type=submit]" },
//       { "esperar": "text=obligatorio" }
//     ] },
//   { "nombre": "login", "como": "anonimo", "ruta": "/login", "soloDesktop": true }
// ]
//
// Pasos posibles: { "click": selector }, { "llenar": [selector, texto] },
// { "esperar": selector }, { "pausa": ms }. Los selectores son de Playwright
// (CSS, "text=...", "role=button[name=...]").
// Cada toma sale en desktop (1440x900) y mobile (390x844), página completa.
//
// La primera vez instala Playwright + Chromium en ~/.microchangas-dev/playwright
// (unos 150 MB). No toca el package.json del front.

import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { join, resolve } from 'node:path';
import { USUARIOS_DEMO, asegurarRaiz, fallar, leerEnv } from '../../g13-levantar-stack/scripts/_comun.mjs';

asegurarRaiz('microchangas-frontend');
const [archivo, salida] = process.argv.slice(2);
if (!archivo || !salida) fallar('Uso: node screenshots.mjs <tomas.json> <carpeta de salida>');

const i = process.argv.indexOf('--backend');
const backend = resolve(i === -1 ? '../microchangas-backend' : process.argv[i + 1]);
const { DEMO_USERS_PASSWORD } = leerEnv(join(backend, '.env.local'));
const FRONT = 'http://localhost:5173';
const VISTAS = {
  desktop: { viewport: { width: 1440, height: 900 } },
  mobile: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
};

const { chromium } = cargarPlaywright();
const tomas = JSON.parse(readFileSync(archivo, 'utf8'));
mkdirSync(salida, { recursive: true });

const navegador = await chromium.launch();
const archivos = [];
const errores = [];
try {
  for (const [vista, opciones] of Object.entries(VISTAS)) {
    // Un contexto por usuario y vista: el login se hace una sola vez.
    const contextos = {};
    for (const toma of tomas) {
      if (vista === 'mobile' && toma.soloDesktop) continue;
      const como = toma.como || 'anonimo';
      try {
        contextos[como] ??= await nuevoContexto(como, opciones);
        const pagina = await contextos[como].newPage();
        await pagina.goto(`${FRONT}${toma.ruta}`, { waitUntil: 'networkidle' });
        for (const paso of toma.pasos || []) await ejecutar(pagina, paso);
        await pagina.waitForLoadState('networkidle');
        const destino = join(salida, `${toma.nombre}--${vista}.png`);
        await pagina.screenshot({ path: destino, fullPage: true });
        archivos.push({ toma: toma.nombre, vista, como, ruta: toma.ruta, url: pagina.url(), archivo: destino });
        await pagina.close();
      } catch (e) {
        errores.push({ toma: toma.nombre, vista, error: e.message.split('\n')[0] });
      }
    }
    for (const c of Object.values(contextos)) await c.close();
  }
} finally {
  await navegador.close();
}

console.log(JSON.stringify({ archivos, errores }, null, 2));
process.exitCode = errores.length ? 1 : 0;

async function nuevoContexto(como, opciones) {
  const contexto = await navegador.newContext({ ...opciones, locale: 'es-AR' });
  if (como === 'anonimo') return contexto;
  if (!USUARIOS_DEMO[como]) throw new Error(`"como" inválido (${como})`);
  if (!DEMO_USERS_PASSWORD) fallar(`No encontré DEMO_USERS_PASSWORD en ${backend}/.env.local. Corré /levantar-stack.`);

  const pagina = await contexto.newPage();
  await pagina.goto(`${FRONT}/login`, { waitUntil: 'networkidle' });
  await pagina.fill('input[type=email]', USUARIOS_DEMO[como].email);
  await pagina.fill('input[type=password]', DEMO_USERS_PASSWORD);
  await pagina.press('input[type=password]', 'Enter');
  await pagina.waitForURL((url) => !url.pathname.startsWith('/login'), { timeout: 15000 });
  await pagina.close();
  return contexto;
}

async function ejecutar(pagina, paso) {
  if (paso.click) await pagina.click(paso.click);
  else if (paso.llenar) await pagina.fill(paso.llenar[0], paso.llenar[1]);
  else if (paso.esperar) await pagina.waitForSelector(paso.esperar);
  else if (paso.pausa) await pagina.waitForTimeout(paso.pausa);
  else throw new Error(`Paso desconocido: ${JSON.stringify(paso)}`);
}

function cargarPlaywright() {
  const dir = join(homedir(), '.microchangas-dev', 'playwright');
  const requerir = createRequire(join(dir, 'package.json'));
  const correr = (cmd, args) => {
    const r = spawnSync(cmd, args, { cwd: dir, stdio: ['ignore', 'ignore', 'inherit'], shell: process.platform === 'win32' });
    if (r.status !== 0) fallar(`Falló: ${cmd} ${args.join(' ')}`);
  };
  if (!existsSync(join(dir, 'node_modules', 'playwright'))) {
    console.error('• Instalando Playwright (solo la primera vez)…');
    mkdirSync(dir, { recursive: true });
    correr('npm', ['install', '--no-audit', '--no-fund', '--prefix', dir, 'playwright@1']);
  }
  // Idempotente: si Chromium ya está, no descarga nada.
  correr('node', [join(dir, 'node_modules', 'playwright', 'cli.js'), 'install', 'chromium']);
  return requerir('playwright');
}
