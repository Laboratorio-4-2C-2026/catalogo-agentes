import { expect, type Locator, type Page } from '@playwright/test';

import { AppSelector } from './app-selectors';
import { DemoBeat } from './demo-timing';
import { dragFromCenter } from './pointer-gestures';

/**
 * Every travel overshoots the app's swipe threshold (read it from the swipe
 * component; these assume one around 90px), so the gesture
 * stays unambiguous on video and the like or dislike stamp reaches full
 * opacity before the card leaves. They differ from each other so that five
 * swipes in a row do not look like a machine repeating itself.
 */
const SWIPE_STYLES = [
  { travelPx: 208, arcPx: -22, steps: 50 },
  { travelPx: 242, arcPx: 14, steps: 44 },
  { travelPx: 196, arcPx: -8, steps: 56 },
  { travelPx: 228, arcPx: 26, steps: 47 },
  { travelPx: 214, arcPx: -16, steps: 52 },
];

/** Keyed off the card so a rerun of the demo produces the same video. */
const styleFor = (cardId: string) => {
  const characterSum = [...cardId].reduce(
    (total, character) => total + character.charCodeAt(0),
    0,
  );
  return SWIPE_STYLES[characterSum % SWIPE_STYLES.length];
};

export const topCard = (page: Page): Locator =>
  page.getByTestId(AppSelector.ACTIVE_CARD).getByTestId(AppSelector.CARD);

const cardIdOn = async (card: Locator): Promise<string> => {
  const cardId = await card.getAttribute(AppSelector.CARD_ID_ATTRIBUTE);
  if (!cardId) {
    throw new Error(
      `The top card is missing its ${AppSelector.CARD_ID_ATTRIBUTE} attribute.`,
    );
  }
  return cardId;
};

const swipeTopCard = async (page: Page, towards: 1 | -1): Promise<void> => {
  const departingCardId = await cardIdOn(topCard(page));
  const style = styleFor(departingCardId);

  await page.waitForTimeout(DemoBeat.BEFORE_GESTURE);
  await dragFromCenter(page, topCard(page), {
    distance: { horizontal: style.travelPx * towards, vertical: 0 },
    arcPx: style.arcPx,
    steps: style.steps,
  });

  await expect(
    page.locator(`[${AppSelector.CARD_ID_ATTRIBUTE}="${departingCardId}"]`),
    'the swiped card should leave the deck',
  ).toHaveCount(0);
  await page.waitForTimeout(DemoBeat.AFTER_GESTURE);
};

export const likeTopCard = (page: Page): Promise<void> => swipeTopCard(page, 1);

export const dislikeTopCard = (page: Page): Promise<void> =>
  swipeTopCard(page, -1);
