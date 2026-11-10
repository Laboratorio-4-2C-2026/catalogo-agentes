// Exports the deck to deck.pdf, one 1920×1080 page per slide, animations at
// their final state. It is the backup if the laptop or the network fails.
import { loadPlaywright, servePreview } from './serve.mjs';

const { chromium } = await loadPlaywright();
const { url, close } = await servePreview();
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(`${url}?print`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: 'deck.pdf', width: '1920px', height: '1080px', printBackground: true });
await browser.close();
close();
console.log('deck.pdf listo.');
