#!/usr/bin/env node
// Compara las migraciones de la branch (supabase/migrations) con las aplicadas
// en la base LOCAL e imprime un JSON:
//
//   { "pendientes": [...], "soloEnLaBase": [...], "aplicadas": n }
//
// - pendientes:   están en la branch y no en la base → `supabase migration up --local`.
// - soloEnLaBase: están en la base y no en la branch (vienen de otra branch o
//                 se renombraron) → la base no refleja esta branch; hace falta reset.
// Consulta la tabla directo en vez de parsear `supabase migration list`,
// cuyo formato de salida cambia según la terminal.

import { readdirSync } from 'node:fs';
import {
  asegurarRaizBackend,
  esLocal,
  fallar,
  leerEnv,
  requireDelBackend,
} from './_comun.mjs';

asegurarRaizBackend();

const { DATABASE_URL } = leerEnv();
if (!esLocal(DATABASE_URL)) {
  fallar('DATABASE_URL de .env.local no es local. Corré primero env-local.mjs.');
}

const enBranch = readdirSync('supabase/migrations')
  .filter((f) => f.endsWith('.sql'))
  .map((f) => f.split('_')[0])
  .sort();

const { Client } = requireDelBackend('pg');
const db = new Client({ connectionString: DATABASE_URL });
try {
  await db.connect();
} catch (e) {
  fallar(`No pude conectarme a la base local (${e.message}). ¿Está Supabase arriba?`, 2);
}

let enBase = [];
try {
  const { rows } = await db.query(
    'select version from supabase_migrations.schema_migrations order by version',
  );
  enBase = rows.map((r) => r.version);
} catch {
  // Base recién creada sin tabla de migraciones: todo está pendiente.
} finally {
  await db.end();
}

console.log(
  JSON.stringify(
    {
      pendientes: enBranch.filter((v) => !enBase.includes(v)),
      soloEnLaBase: enBase.filter((v) => !enBranch.includes(v)),
      aplicadas: enBase.length,
    },
    null,
    2,
  ),
);
