import { defineConfig, devices } from '@playwright/test';

import { chromiumScaleArguments } from './capture/recording-format';

const DEFAULT_APP_URL = 'http://localhost:5173';

export default defineConfig({
  testDir: '.',
  outputDir: 'recordings/playwright-artifacts',
  timeout: 120_000,
  workers: 1,
  retries: 0,
  use: {
    browserName: 'chromium',
    userAgent: devices['iPhone 15'].userAgent,
    hasTouch: true,
    // The window's own size is the viewport, so that the forced device scale
    // factor applies to it. Playwright rejects `isMobile` in this mode, which
    // costs nothing here: the layout follows the CSS viewport either way.
    viewport: null,
    launchOptions: { args: chromiumScaleArguments },
    baseURL: process.env.DEMO_APP_URL ?? DEFAULT_APP_URL,
    headless: true,
  },
});
