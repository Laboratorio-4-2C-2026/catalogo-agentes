import type { Page } from '@playwright/test';

/**
 * Scrolling by wheel events means one protocol round trip and one jump per
 * step, which reads as stuttering however fast the capture runs. Animating the
 * scroll position inside the page instead runs on the browser's own frame
 * clock, and lets the motion decelerate the way a flicked finger does.
 */
export interface Flick {
  distance: number;
  durationMs: number;
}

export const flickScrollInside = async (
  page: Page,
  containerTestId: string,
  flick: Flick,
): Promise<void> => {
  await page.evaluate(
    ({ containerTestId, flick }) => {
      const container = document.querySelector(
        `[data-testid="${containerTestId}"]`,
      );
      if (!container) {
        throw new Error(`No element with testid "${containerTestId}".`);
      }

      const candidates: Element[] = [
        container,
        ...Array.from(container.querySelectorAll('*')),
      ];
      const scroller = candidates.find(
        (candidate) =>
          candidate.scrollHeight > candidate.clientHeight + 8 &&
          ['auto', 'scroll'].includes(getComputedStyle(candidate).overflowY),
      );
      if (!scroller) {
        throw new Error(`Nothing scrollable inside "${containerTestId}".`);
      }

      const from = scroller.scrollTop;
      const startedAt = performance.now();

      return new Promise<void>((resolve) => {
        const advance = (now: number) => {
          const progress = Math.min((now - startedAt) / flick.durationMs, 1);
          const decelerating = 1 - Math.pow(1 - progress, 3);
          scroller.scrollTop = from + flick.distance * decelerating;
          if (progress < 1) {
            requestAnimationFrame(advance);
          } else {
            resolve();
          }
        };
        requestAnimationFrame(advance);
      });
    },
    { containerTestId, flick },
  );
};
