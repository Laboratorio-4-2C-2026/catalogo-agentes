#!/usr/bin/env node
// Sube imágenes a la branch `evidencias` del repo y devuelve sus URLs para
// usarlas en un comentario de la PR (GitHub no tiene API para adjuntar
// imágenes a un comentario).
//
//   node subir-evidencias.mjs <archivo.png> [...más archivos]
//
// (desde la raíz del repo de producto, normalmente microchangas-frontend)
//
// `evidencias` es una branch huérfana: no comparte historia con el código,
// nunca se mergea y no dispara deploys ni workflows (solo corren en PRs y en
// push a main). Se arma con plumbing de git y un índice temporal, así que NO
// toca tu working tree, tu index ni tu branch actual.
// Las imágenes quedan en evidencias/<tu-branch>/<fecha-hora>/.

import { spawnSync } from 'node:child_process';
import { rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, join, resolve } from 'node:path';
import { fallar } from '../../g13-levantar-stack/scripts/_comun.mjs';

const BRANCH = 'evidencias';
const archivos = process.argv.slice(2).map((a) => resolve(a));
if (!archivos.length) fallar('Uso: node subir-evidencias.mjs <archivo> [...]');

const git = (args, env) => {
  const r = spawnSync('git', args, { encoding: 'utf8', env: { ...process.env, ...env } });
  return { ok: r.status === 0, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
};
const gitOk = (args, env) => {
  const r = git(args, env);
  if (!r.ok) fallar(`git ${args.join(' ')}\n${r.err}`);
  return r.out;
};

const remoto = gitOk(['remote', 'get-url', 'origin']);
const m = remoto.match(/github\.com[:/]([^/]+)\/(.+?)(\.git)?$/);
if (!m) fallar(`origin no es un repo de GitHub: ${remoto}`);
const [, owner, repo] = m;

const rama = gitOk(['branch', '--show-current']) || 'detached';
const sello = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 15);
const carpeta = `${rama.replace(/[^\w.-]+/g, '-')}/${sello}`;

const indice = join(tmpdir(), `evidencias-index-${process.pid}`);
const conIndice = { GIT_INDEX_FILE: indice };

let commit;
try {
  for (let intento = 1; intento <= 3; intento++) {
    // Base: la punta remota de `evidencias`, si existe.
    const existe = git(['ls-remote', '--exit-code', '--heads', 'origin', BRANCH]).ok;
    let padre = null;
    if (existe) {
      gitOk(['fetch', '-q', 'origin', `+refs/heads/${BRANCH}:refs/remotes/origin/${BRANCH}`]);
      padre = gitOk(['rev-parse', `refs/remotes/origin/${BRANCH}`]);
      gitOk(['read-tree', padre], conIndice);
    } else {
      gitOk(['read-tree', '--empty'], conIndice);
    }

    for (const archivo of archivos) {
      const blob = gitOk(['hash-object', '-w', archivo]);
      gitOk(['update-index', '--add', '--cacheinfo', `100644,${blob},${carpeta}/${basename(archivo)}`], conIndice);
    }
    const arbol = gitOk(['write-tree'], conIndice);
    commit = gitOk([
      'commit-tree', arbol,
      ...(padre ? ['-p', padre] : []),
      '-m', `Evidencias de ${rama} (${sello})`,
    ]);

    if (git(['push', '-q', 'origin', `${commit}:refs/heads/${BRANCH}`]).ok) break;
    if (intento === 3) fallar(`No pude pushear a ${BRANCH} (¿alguien pusheó a la vez? ¿tenés permiso de push?).`);
  }
} finally {
  rmSync(indice, { force: true });
}

// URLs fijadas al commit: no cambian aunque la branch siga creciendo.
// Las ven quienes tengan acceso al repo (es privado), igual que la PR.
const urls = Object.fromEntries(
  archivos.map((a) => [
    basename(a),
    `https://github.com/${owner}/${repo}/blob/${commit}/${carpeta}/${encodeURIComponent(basename(a))}?raw=true`,
  ]),
);
console.log(JSON.stringify({ branch: BRANCH, commit, carpeta, urls }, null, 2));
