import { expect, type Page } from '@playwright/test';

import { AppSelector } from './app-selectors';
import { DemoBeat } from './demo-timing';
import { flickScrollInside } from './flick-scrolling';
import { dragFromCenter } from './pointer-gestures';
import { topCard } from './swipe-the-deck';

/**
 * The pane opens on an upward drag past the app's threshold (these assume one
 * around 60px) that is steeper than it is wide. A long pull keeps that unmistakable next to the
 * horizontal swipes the demo has just shown.
 */
const PULL_UP_PX = 260;

/** Comfortably past the app's close threshold (assumed around 60px). */
const PUSH_DOWN_PX = 200;

const READ_DOWN = { distance: 620, durationMs: 1100 };
const READ_BACK_UP = { distance: -620, durationMs: 900 };

const detailsPane = (page: Page) => page.getByTestId(AppSelector.DETAILS_PANE);

const expectPaneExpanded = (page: Page, expanded: boolean) =>
  expect(detailsPane(page)).toHaveAttribute(
    AppSelector.DETAILS_PANE_EXPANDED_ATTRIBUTE,
    String(expanded),
  );

export const pullUpTheDetailsPane = async (page: Page): Promise<void> => {
  await page.waitForTimeout(DemoBeat.BEFORE_GESTURE);
  await dragFromCenter(page, topCard(page), {
    distance: { horizontal: 0, vertical: -PULL_UP_PX },
    arcPx: 10,
  });

  await expectPaneExpanded(page, true);
  await page.waitForTimeout(DemoBeat.LINGER_ON_RESULT);
};

export const readDownTheDetailsPane = async (page: Page): Promise<void> => {
  await flickScrollInside(page, AppSelector.DETAILS_PANE, READ_DOWN);
  await page.waitForTimeout(DemoBeat.LINGER_ON_RESULT);

  await flickScrollInside(page, AppSelector.DETAILS_PANE, READ_BACK_UP);
  await page.waitForTimeout(DemoBeat.AFTER_GESTURE);
};

export const pushTheDetailsPaneBackDown = async (page: Page): Promise<void> => {
  await dragFromCenter(page, page.getByTestId(AppSelector.DETAILS_PANE_HANDLE), {
    distance: { horizontal: 0, vertical: PUSH_DOWN_PX },
  });

  await expectPaneExpanded(page, false);
  await page.waitForTimeout(DemoBeat.AFTER_GESTURE);
};
