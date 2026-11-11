import type { Locator, Page } from '@playwright/test';

/**
 * Cinematch cards listen on pointer events (`SwipeCard.tsx`), which Chromium
 * raises for mouse input too, so a slow interpolated mouse drag reproduces a
 * real swipe including its velocity and the rotation that follows it.
 *
 * A dragged card only moves when a pointer event arrives, so these steps are
 * the frame rate of the gesture: too few and the card teleports between
 * positions however fast the capture runs. Each step already costs a protocol
 * round trip, which paces the gesture on its own, so adding a timer on top
 * only doubles the wall clock.
 */
const DEFAULT_STEPS_PER_GESTURE = 50;

export interface GestureDistance {
  horizontal: number;
  vertical: number;
}

export interface DragShape {
  distance: GestureDistance;
  /** How far the drag bows off the straight line at its midpoint. */
  arcPx?: number;
  steps?: number;
}

interface ScreenPoint {
  horizontal: number;
  vertical: number;
}

const easeInOutQuad = (progress: number): number =>
  progress < 0.5
    ? 2 * progress * progress
    : 1 - Math.pow(-2 * progress + 2, 2) / 2;

const bowAt = (progress: number): number => Math.sin(Math.PI * progress);

const interpolate = (from: number, to: number, progress: number): number =>
  from + (to - from) * progress;

const centerOf = async (element: Locator): Promise<ScreenPoint> => {
  const box = await element.boundingBox();
  if (!box) {
    throw new Error(
      'Cannot start a gesture on an element that is not laid out on screen.',
    );
  }
  return {
    horizontal: box.x + box.width / 2,
    vertical: box.y + box.height / 2,
  };
};

const shiftBy = (
  point: ScreenPoint,
  distance: GestureDistance,
): ScreenPoint => ({
  horizontal: point.horizontal + distance.horizontal,
  vertical: point.vertical + distance.vertical,
});

export const dragFromCenter = async (
  page: Page,
  element: Locator,
  { distance, arcPx = 0, steps = DEFAULT_STEPS_PER_GESTURE }: DragShape,
): Promise<void> => {
  const start = await centerOf(element);
  const end = shiftBy(start, distance);

  await page.mouse.move(start.horizontal, start.vertical);
  await page.mouse.down();

  for (let step = 1; step <= steps; step += 1) {
    const progress = easeInOutQuad(step / steps);
    await page.mouse.move(
      interpolate(start.horizontal, end.horizontal, progress),
      interpolate(start.vertical, end.vertical, progress) +
        bowAt(step / steps) * arcPx,
    );
  }

  await page.mouse.up();
};
