import { chromium } from '@playwright/test';

/**
 * ffmpeg cannot read SVG, and the demo already depends on a browser, so the
 * browser is what turns the frame into the transparent PNG ffmpeg overlays.
 */
export const rasterizeSvgToPng = async (svg, { width, height, outputPath }) => {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width, height } });
    await page.setContent(
      `<body style="margin:0;background:transparent">${svg}</body>`,
    );
    await page.screenshot({ path: outputPath, omitBackground: true });
  } finally {
    await browser.close();
  }
};
