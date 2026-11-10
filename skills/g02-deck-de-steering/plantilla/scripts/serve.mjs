import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';

/** Starts `vite preview` on the built deck and resolves once it answers. */
export async function servePreview(port = 4173) {
  const server = spawn('npx', ['vite', 'preview', '--port', String(port), '--strictPort'], { stdio: 'ignore' });
  const url = `http://localhost:${port}/`;
  for (let i = 0; i < 50; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return { url, close: () => server.kill() };
    } catch {
      // not up yet
    }
    await new Promise(r => setTimeout(r, 200));
  }
  server.kill();
  throw new Error('vite preview did not start. Run `npm run build` first.');
}

export async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    // fall through: a global install is reachable through require()
  }
  try {
    return createRequire(import.meta.url)('playwright');
  } catch {
    console.error('Playwright is missing: npm i -D playwright && npx playwright install chromium');
    process.exit(1);
  }
}
