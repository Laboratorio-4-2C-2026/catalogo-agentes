#!/usr/bin/env node
// Usuarios demo para el seed (`pnpm db:seed` los busca por display_name).
//
//   node usuarios-demo.mjs              crea o resincroniza los 4 usuarios
//   node usuarios-demo.mjs --verificar  hace login contra la API y llama /auth/me
//
// Solo contra Supabase LOCAL. La contraseña se genera una vez por máquina y
// queda en .env.local (DEMO_USERS_PASSWORD), que no se versiona. El script
// nunca la imprime.

import { randomBytes } from 'node:crypto';
import {
  ENV_LOCAL,
  asegurarRaizBackend,
  esLocal,
  escribirVar,
  fallar,
  leerEnv,
  loginDemo,
  USUARIOS_DEMO,
} from './_comun.mjs';

asegurarRaizBackend();
const env = leerEnv();

if (process.argv.includes('--verificar')) {
  await verificar();
} else {
  await sincronizar();
}

async function sincronizar() {
  const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY } = env;
  if (!esLocal(SUPABASE_URL) || !SUPABASE_SERVICE_ROLE_KEY) {
    fallar('SUPABASE_URL de .env.local no es local o falta la service key. Corré env-local.mjs.');
  }

  let password = env.DEMO_USERS_PASSWORD;
  if (!password) {
    password = `Demo-${randomBytes(6).toString('hex')}!`;
    escribirVar(ENV_LOCAL, 'DEMO_USERS_PASSWORD', password);
  }

  const admin = (ruta, init = {}) =>
    fetch(`${SUPABASE_URL}/auth/v1/admin/${ruta}`, {
      ...init,
      headers: {
        apikey: SUPABASE_SERVICE_ROLE_KEY,
        Authorization: `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`,
        'Content-Type': 'application/json',
      },
    });

  const lista = await admin('users?per_page=1000');
  if (!lista.ok) fallar(`No pude listar usuarios (${lista.status}).`);
  const { users } = await lista.json();

  for (const { email, displayName: display_name, fullName: full_name, role } of Object.values(USUARIOS_DEMO)) {
    const existente = users.find((u) => u.email === email);
    const body = JSON.stringify({
      email,
      password,
      email_confirm: true,
      user_metadata: { display_name, full_name, role },
    });
    const res = existente
      ? await admin(`users/${existente.id}`, { method: 'PUT', body })
      : await admin('users', { method: 'POST', body });
    if (!res.ok) fallar(`${email}: ${res.status} ${await res.text()}`);
    console.log(`• ${existente ? 'actualizado' : 'creado    '}  ${email}  (${display_name}, ${role})`);
  }
  console.log(`  Contraseña: ${ENV_LOCAL} → DEMO_USERS_PASSWORD`);
}

async function verificar() {
  const api = `http://localhost:${env.PORT || 3000}`;
  const health = await fetch(`${api}/identity/health`).then((r) => r.json());
  if (health.status !== 'ok') fallar(`Health check: ${JSON.stringify(health)}`);

  const accessToken = await loginDemo(api, 'worker', env.DEMO_USERS_PASSWORD);

  const me = await fetch(`${api}/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  }).then((r) => r.json());
  console.log(`✔ API ok · login ok · /auth/me → ${me.displayName} (${me.role}, ${me.identityStatus})`);
}
