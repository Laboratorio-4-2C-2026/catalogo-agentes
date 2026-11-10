// Copies a free React Bits component (TypeScript + Tailwind variant) from the
// official repo into src/components/bits/. Works even where reactbits.dev is
// blocked. Usage: npm run add-bit -- Backgrounds/Silk
import { writeFile } from 'node:fs/promises';

const target = process.argv[2];
if (!target || !target.includes('/')) {
  console.error('Uso: npm run add-bit -- <Categoría>/<Nombre>   (ej. Backgrounds/Silk, TextAnimations/ShinyText)');
  process.exit(1);
}

const name = target.split('/').pop();
const url = `https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/ts-tailwind/${target}/${name}.tsx`;
const res = await fetch(url);
if (!res.ok) {
  console.error(`No encontré ${target} (${res.status}). Revisá el nombre en https://github.com/DavidHDev/react-bits/tree/main/src/ts-tailwind`);
  process.exit(1);
}
const source = await res.text();
await writeFile(`src/components/bits/${name}.tsx`, source);

const deps = [...source.matchAll(/from '([^'.][^']*)'/g)].map(m => m[1]).filter(d => d !== 'react');
console.log(`Agregado src/components/bits/${name}.tsx`);
if (deps.length) console.log(`Importa: ${[...new Set(deps)].join(', ')} — instalalas si faltan (npm i <paquete>@<versión>).`);
