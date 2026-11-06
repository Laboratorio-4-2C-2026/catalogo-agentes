#!/usr/bin/env node
// Deja .env.local del backend (y opcionalmente del frontend) listo para
// correr contra Supabase LOCAL.
//
//   node env-local.mjs [--frontend <ruta a microchangas-frontend>]
//
// - Si no existe .env.local, lo crea desde .env.local.example.
// - Copia URL, claves y DB de `supabase status` (el stack tiene que estar arriba).
// - Completa las variables obligatorias que falten (NODE_ENV, Didit con
//   placeholders + bypass local). No pisa valores que el dev ya cargó.
// - Si .env.local apunta a un Supabase que NO es local, no toca nada y falla.
// Nunca imprime valores, solo nombres de variables.

import { copyFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import {
  ENV_LOCAL,
  asegurarRaizBackend,
  esLocal,
  escribirVar,
  fallar,
  leerEnv,
} from './_comun.mjs';

asegurarRaizBackend();

if (!existsSync(ENV_LOCAL)) {
  copyFileSync('.env.local.example', ENV_LOCAL);
  console.log(`• Creado ${ENV_LOCAL} desde .env.local.example`);
}

const actual = leerEnv();
const remotas = ['SUPABASE_URL', 'DATABASE_URL', 'DIRECT_URL'].filter(
  (k) => actual[k] && !esLocal(actual[k]),
);
if (remotas.length) {
  fallar(
    `${ENV_LOCAL} apunta a un Supabase que no es local (${remotas.join(', ')}). ` +
      'No lo toco: revisalo a mano antes de seguir.',
  );
}

const status = spawnSync('pnpm', ['exec', 'supabase', 'status', '-o', 'json'], {
  encoding: 'utf8',
  shell: process.platform === 'win32',
});
let supa;
try {
  supa = JSON.parse(status.stdout.slice(status.stdout.indexOf('{')));
} catch {
  fallar('Supabase local no está corriendo. Levantalo con `pnpm supabase:start`.', 2);
}

const cambios = [];
const poner = (clave, valor) => {
  if (actual[clave] !== valor) {
    escribirVar(ENV_LOCAL, clave, valor);
    cambios.push(clave);
  }
};
const completar = (clave, valor) => {
  if (!actual[clave]) poner(clave, valor);
};

// Lo que viene de `supabase status` se refresca siempre: ya verificamos que
// apunta a local, y si el stack se recreó las claves viejas no sirven.
poner('SUPABASE_URL', supa.API_URL);
poner('SUPABASE_ANON_KEY', supa.ANON_KEY);
poner('SUPABASE_SERVICE_ROLE_KEY', supa.SERVICE_ROLE_KEY);
poner('DATABASE_URL', supa.DB_URL);
poner('DIRECT_URL', supa.DB_URL);

completar('NODE_ENV', 'development');
completar('PORT', '3000');
completar('FRONTEND_URL', 'http://localhost:5173');
completar('DIDIT_BASE_URL', 'https://verification.didit.me');
if (!actual.DIDIT_API_KEY) {
  // Sin credenciales reales de Didit, la verificación de identidad va por bypass.
  poner('DIDIT_API_KEY', 'local-placeholder');
  completar('DIDIT_WORKFLOW_ID', '00000000-0000-0000-0000-000000000000');
  completar('DIDIT_WEBHOOK_SECRET', 'local-placeholder');
  completar('IDENTITY_BYPASS_ENABLED', 'true');
}

console.log(
  cambios.length
    ? `• Backend ${ENV_LOCAL}: actualicé ${cambios.join(', ')}`
    : `• Backend ${ENV_LOCAL}: ya estaba al día`,
);

const i = process.argv.indexOf('--frontend');
if (i !== -1) {
  const front = process.argv[i + 1];
  const envFront = join(front, ENV_LOCAL);
  const apiUrl = `http://localhost:${leerEnv().PORT || 3000}`;
  const vars = leerEnv(envFront);
  if (vars.VITE_API_URL && vars.VITE_API_URL !== apiUrl) {
    console.log(
      `⚠ Frontend ${ENV_LOCAL}: VITE_API_URL apunta a otro lado, no lo toco (esperado ${apiUrl}).`,
    );
  } else if (!vars.VITE_API_URL) {
    escribirVar(envFront, 'VITE_API_URL', apiUrl);
    console.log(`• Frontend ${ENV_LOCAL}: VITE_API_URL=${apiUrl}`);
  } else {
    console.log(`• Frontend ${ENV_LOCAL}: ya estaba al día`);
  }
}
