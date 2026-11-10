// Renders every slide and fails if anything would embarrass us on the projector:
// content outside the 1920×1080 frame, text cut off, or example data left in.
// Screenshots land in check/ so a human (or Claude) can look at every slide.
import { mkdir } from 'node:fs/promises';
import { loadPlaywright, servePreview } from './serve.mjs';

const { chromium } = await loadPlaywright();
const { url, close } = await servePreview();
const browser = await chromium.launch();
await mkdir('check', { recursive: true });

const problems = [];

// 1. Static render of all slides at full size: geometry checks + screenshots.
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`${url}?print`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

const report = await page.evaluate(() =>
  [...document.querySelectorAll('[data-slide]')].map(slide => {
    const frame = slide.getBoundingClientRect();
    const issues = [];
    for (const el of slide.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const tol = 2;
      if (r.left < frame.left - tol || r.right > frame.right + tol || r.top < frame.top - tol || r.bottom > frame.bottom + tol) {
        issues.push(`sale del marco: <${el.tagName.toLowerCase()}> "${(el.textContent || '').trim().slice(0, 40)}"`);
      }
      if (el.scrollWidth > el.clientWidth + tol && getComputedStyle(el).overflow === 'hidden' && el.textContent?.trim()) {
        issues.push(`texto cortado: "${el.textContent.trim().slice(0, 40)}"`);
      }
    }
    if (slide.querySelector('[data-example-data]')) issues.push('tiene DATO DE EJEMPLO');
    return { id: slide.getAttribute('data-slide'), issues: [...new Set(issues)].slice(0, 5) };
  }),
);

const slides = await page.$$('[data-slide]');
for (const [i, el] of slides.entries()) {
  await el.screenshot({ path: `check/${String(i + 1).padStart(2, '0')}-${report[i].id}.png` });
}

// 2. Live render at a laptop size, after the entrance animations, to catch
//    layout that only breaks while animating or once scaled down.
const live = await browser.newPage({ viewport: { width: 1280, height: 720 } });
for (let i = 0; i < report.length; i++) {
  await live.goto(`${url}#${i + 1}`, { waitUntil: 'networkidle' });
  await live.waitForTimeout(2500);
  await live.screenshot({ path: `check/${String(i + 1).padStart(2, '0')}-${report[i].id}-live.png` });
}

await browser.close();
close();

for (const { id, issues } of report) {
  if (issues.length) problems.push(`  ${id}:\n${issues.map(x => `    - ${x}`).join('\n')}`);
}

console.log(`${report.length} slides revisadas. Capturas en check/.`);
if (problems.length) {
  console.error(`\nProblemas:\n${problems.join('\n')}`);
  process.exit(1);
}
console.log('Sin problemas de layout ni datos de ejemplo.');
