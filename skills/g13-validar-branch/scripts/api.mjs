#!/usr/bin/env node
// Corre casos contra la API local y devuelve los resultados en JSON.
//
//   node api.mjs <casos.json>      (desde la raíz de microchangas-backend)
//
// casos.json:
// [
//   { "nombre": "Worker ve su dashboard", "como": "worker",
//     "metodo": "GET", "ruta": "/dashboard/worker", "esperado": 200 },
//   { "nombre": "Sin token", "como": "anonimo",
//     "metodo": "GET", "ruta": "/dashboard/worker", "esperado": 401 },
//   { "nombre": "Crear changa", "como": "client", "metodo": "POST",
//     "ruta": "/changas", "body": { ... }, "esperado": 201,
//     "guardar": { "changaId": "id" } },
//   { "nombre": "Ver la changa creada", "como": "worker",
//     "metodo": "GET", "ruta": "/changas/{changaId}", "esperado": 200 }
// ]
//
// `como`: worker | worker2 | client | client2 | anonimo.
// `guardar`: toma campos de la respuesta (ruta con puntos, ej. "data.id") para
// usarlos como {variable} en la ruta o el body de los casos siguientes.
// Todo corre contra la base LOCAL; los casos pueden crear datos.

import { readFileSync } from 'node:fs';
import {
  USUARIOS_DEMO,
  asegurarRaizBackend,
  fallar,
  leerEnv,
  loginDemo,
} from '../../g13-levantar-stack/scripts/_comun.mjs';

asegurarRaizBackend();
const archivo = process.argv[2];
if (!archivo) fallar('Uso: node api.mjs <casos.json>');

const env = leerEnv();
const api = `http://localhost:${env.PORT || 3000}`;
const casos = JSON.parse(readFileSync(archivo, 'utf8'));

const tokens = {};
const vars = {};
const MAX_CUERPO = 600;
const SENSIBLE = /token|password|secret|key|authorization/i;

const reemplazar = (valor) =>
  JSON.parse(
    JSON.stringify(valor ?? null).replace(/\{(\w+)\}/g, (m, k) =>
      k in vars ? String(vars[k]) : m,
    ),
  );
const leerCampo = (obj, ruta) => ruta.split('.').reduce((o, k) => o?.[k], obj);

const resultados = [];
for (const caso of casos) {
  const { nombre, como = 'anonimo', metodo = 'GET', esperado } = caso;
  if (como !== 'anonimo' && !USUARIOS_DEMO[como]) fallar(`${nombre}: "como" inválido (${como})`);

  const headers = { 'Content-Type': 'application/json', ...(caso.headers || {}) };
  if (como !== 'anonimo') {
    tokens[como] ??= await loginDemo(api, como, env.DEMO_USERS_PASSWORD);
    headers.Authorization = `Bearer ${tokens[como]}`;
  }

  const ruta = reemplazar(caso.ruta);
  const body = caso.body === undefined ? undefined : JSON.stringify(reemplazar(caso.body));
  let status;
  let cuerpo;
  try {
    const res = await fetch(`${api}${ruta}`, { method: metodo, headers, body });
    status = res.status;
    const texto = await res.text();
    try {
      cuerpo = JSON.parse(texto);
    } catch {
      cuerpo = texto;
    }
  } catch (e) {
    status = 0;
    cuerpo = `No respondió: ${e.message}`;
  }

  for (const [variable, campo] of Object.entries(caso.guardar || {})) {
    vars[variable] = leerCampo(cuerpo, campo);
  }

  // Los resultados terminan en un comentario de la PR: nada de tokens ni claves.
  const resumen =
    typeof cuerpo === 'string'
      ? cuerpo.replace(/eyJ[\w-]+\.[\w-]+\.[\w-]+/g, '***')
      : JSON.stringify(cuerpo, (k, v) => (SENSIBLE.test(k) ? '***' : v));
  resultados.push({
    nombre,
    como,
    request: `${metodo} ${ruta}`,
    esperado,
    status,
    ok: esperado === undefined ? status >= 200 && status < 300 : status === esperado,
    cuerpo: resumen.length > MAX_CUERPO ? `${resumen.slice(0, MAX_CUERPO)}…` : resumen,
  });
}

console.log(JSON.stringify(resultados, null, 2));
process.exitCode = resultados.every((r) => r.ok) ? 0 : 1;
