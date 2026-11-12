// Compares two `forge snapshot` files and prints the gas changes as JSON.
//
// Usage: node costos-gas.mjs <base.snap> <head.snap> <base_ok> <head_ok>
//
// The agent only explains what this script measured: it never computes gas
// itself. A snapshot line looks like one of these:
//   EurekaPatentRegistryTest:test_register() (gas: 123456)
//   EurekaPatentRegistryTest:testFuzz_register(uint256) (runs: 256, μ: 12345, ~: 12000)
//   EurekaMarketplaceFeesInvariant:invariant_fees() (runs: 256, calls: 128000, reverts: 0)
// Invariant runs carry no gas figure and are skipped.
//
// The snapshots come from a job that ran the PR's tests, so their content is
// not trusted: a line whose test name does not look like `Contract:fn(types)`
// is dropped. The names end up in the agent's input and in the published table.

import { existsSync, readFileSync } from 'node:fs';

const MAX_CAMBIOS = 60;
const TEST = /^[A-Za-z_$][\w$]*:[A-Za-z_$][\w$]*\([\w$,[\] ]*\)$/;

function parse(path) {
  const gas = new Map();
  if (!existsSync(path)) return gas;
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    const m = line.match(/^(.+?) \((.*)\)\s*$/);
    if (!m || !TEST.test(m[1])) continue;
    const fixed = m[2].match(/(?:^|, )gas: (\d+)/);
    const mean = m[2].match(/(?:^|, )μ: (\d+)/);
    const value = fixed ?? mean;
    if (value) gas.set(m[1], Number(value[1]));
  }
  return gas;
}

const [basePath, headPath, baseOk, headOk] = process.argv.slice(2);
const base = parse(basePath);
const head = parse(headPath);
const medido = baseOk === 'true' && headOk === 'true' && base.size > 0 && head.size > 0;

const cambios = [];
for (const [test, gasHead] of head) {
  const gasBase = base.get(test);
  if (gasBase === undefined || gasBase === gasHead) continue;
  cambios.push({
    test,
    base: gasBase,
    head: gasHead,
    delta: gasHead - gasBase,
    pct: Number((((gasHead - gasBase) / gasBase) * 100).toFixed(2)),
  });
}
cambios.sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta));

const nuevos = [...head.keys()].filter((t) => !base.has(t));
const quitados = [...base.keys()].filter((t) => !head.has(t));

console.log(JSON.stringify({
  medido,
  snapshot_base_ok: baseOk === 'true',
  snapshot_pr_ok: headOk === 'true',
  resumen: {
    tests_comparados: [...head.keys()].filter((t) => base.has(t)).length,
    suben: cambios.filter((c) => c.delta > 0).length,
    bajan: cambios.filter((c) => c.delta < 0).length,
    mayor_suba_pct: cambios.reduce((max, c) => Math.max(max, c.pct), 0),
    tests_nuevos: nuevos.length,
    tests_quitados: quitados.length,
  },
  cambios_truncados: cambios.length > MAX_CAMBIOS,
  cambios: cambios.slice(0, MAX_CAMBIOS),
  tests_nuevos: nuevos.slice(0, MAX_CAMBIOS).map((t) => ({ test: t, gas: head.get(t) })),
  tests_quitados: quitados.slice(0, MAX_CAMBIOS),
}, null, 2));
