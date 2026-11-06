// Utilidades compartidas por los scripts de los skills de microchangas-dev.
// Vive en levantar-stack, pero validar-branch también la importa
// (../../levantar-stack/scripts/_comun.mjs): los dos skills se instalan juntos,
// uno al lado del otro, en la misma carpeta de skills.
// Todo es Node puro (sin dependencias propias) para que corra igual en
// Windows, macOS y Linux.

import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join } from 'node:path';

export const ENV_LOCAL = '.env.local';

// Los usuarios demo que crea /levantar-stack y que `pnpm db:seed` busca por
// display_name. La clave es el alias que usan los scripts (`como: "worker"`).
export const USUARIOS_DEMO = {
  worker: { email: 'demo.worker@microchangas.test', displayName: 'Demo Worker', fullName: 'Lucía Fernández', role: 'worker' },
  worker2: { email: 'demo.worker2@microchangas.test', displayName: 'Demo Worker 2', fullName: 'Martín Quiroga', role: 'worker' },
  client: { email: 'demo.client@microchangas.test', displayName: 'Demo Client', fullName: 'Carolina Méndez', role: 'client' },
  client2: { email: 'demo.client2@microchangas.test', displayName: 'Demo Client 2', fullName: 'Federico Álvarez', role: 'client' },
};

export function asegurarRaiz(repo, dir = process.cwd()) {
  const pkg = join(dir, 'package.json');
  const ok = existsSync(pkg) && JSON.parse(readFileSync(pkg, 'utf8')).name === repo;
  if (!ok) fallar(`Corré este script desde la raíz de ${repo}.`);
}

export function asegurarRaizBackend() {
  asegurarRaiz('microchangas-backend');
}

export function leerEnv(ruta = ENV_LOCAL) {
  if (!existsSync(ruta)) return {};
  const vars = {};
  for (const linea of readFileSync(ruta, 'utf8').split(/\r?\n/)) {
    const m = linea.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m) vars[m[1]] = m[2].replace(/^(['"])(.*)\1$/, '$2');
  }
  return vars;
}

// Reemplaza todas las apariciones de KEY=... o la agrega al final.
export function escribirVar(ruta, clave, valor) {
  const texto = existsSync(ruta) ? readFileSync(ruta, 'utf8') : '';
  const patron = new RegExp(`^\\s*${clave}\\s*=.*$`, 'gm');
  const nuevo = patron.test(texto)
    ? texto.replace(patron, `${clave}=${valor}`)
    : `${texto.replace(/\s*$/, '')}\n${clave}=${valor}\n`;
  writeFileSync(ruta, nuevo);
}

export function esLocal(url) {
  if (!url) return false;
  try {
    const { hostname } = new URL(url);
    return ['127.0.0.1', 'localhost', '::1', '[::1]'].includes(hostname);
  } catch {
    return false;
  }
}

// Carga una dependencia instalada en el backend (por ejemplo `pg`).
export function requireDelBackend(nombre) {
  return createRequire(join(process.cwd(), 'package.json'))(nombre);
}

// Login contra la API local con un usuario demo. Devuelve el accessToken.
export async function loginDemo(api, alias, password) {
  const { email } = USUARIOS_DEMO[alias];
  const res = await fetch(`${api}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) fallar(`Login ${email}: ${res.status} ${await res.text()}`);
  return (await res.json()).accessToken;
}

export function fallar(mensaje, codigo = 1) {
  console.error(`✖ ${mensaje}`);
  process.exit(codigo);
}
