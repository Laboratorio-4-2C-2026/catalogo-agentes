import { expect, type Page } from '@playwright/test';

import { AppSelector } from './app-selectors';
import { DemoBeat, TYPING_DELAY_MS } from './demo-timing';

export interface DemoAccount {
  email: string;
  password: string;
}

const requiredVariable = (name: string): string => {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Set ${name} to the demo account before recording.`);
  }
  return value;
};

export const demoAccountFromEnvironment = (): DemoAccount => ({
  email: requiredVariable('DEMO_EMAIL'),
  password: requiredVariable('DEMO_PASSWORD'),
});

/**
 * Filming may only begin once this has returned: web fonts swapping in and the
 * first layout landing are a visible twitch that belongs before the recording,
 * not in it.
 */
export const openTheLoginScreen = async (page: Page): Promise<void> => {
  await page.goto(AppSelector.LOGIN_PATH);
  await expect(
    page.getByRole('heading', { name: AppSelector.LOGIN_HEADING }),
  ).toBeVisible();
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(DemoBeat.AFTER_SCREEN_APPEARS);
};

export const logIn = async (
  page: Page,
  account: DemoAccount,
): Promise<void> => {
  await page
    .getByLabel('Email', { exact: true })
    .pressSequentially(account.email, { delay: TYPING_DELAY_MS });
  await page.waitForTimeout(DemoBeat.BEFORE_GESTURE);

  // Not a substring match: the reveal toggle is labelled "Show password".
  await page
    .getByLabel('Password', { exact: true })
    .pressSequentially(account.password, { delay: TYPING_DELAY_MS });
  await page.waitForTimeout(DemoBeat.BEFORE_GESTURE);

  await page.getByRole('button', { name: AppSelector.LOGIN_BUTTON }).click();

  await expect(page.getByTestId(AppSelector.DECK)).toBeVisible();
  await page.waitForTimeout(DemoBeat.AFTER_SCREEN_APPEARS);
};
