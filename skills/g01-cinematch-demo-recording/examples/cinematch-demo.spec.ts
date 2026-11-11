import { test } from './capture/recorded-test';
import { DemoBeat } from './scenario/demo-timing';
import {
  demoAccountFromEnvironment,
  logIn,
  openTheLoginScreen,
} from './scenario/log-in';
import {
  pullUpTheDetailsPane,
  pushTheDetailsPaneBackDown,
  readDownTheDetailsPane,
} from './scenario/pull-up-the-details-pane';
import { dislikeTopCard, likeTopCard } from './scenario/swipe-the-deck';

test('log in, swipe the deck, pull up the details pane', async ({
  page,
  recording,
}) => {
  await openTheLoginScreen(page);
  await recording.start();

  await logIn(page, demoAccountFromEnvironment());

  await likeTopCard(page);
  await dislikeTopCard(page);
  await likeTopCard(page);
  await dislikeTopCard(page);
  await likeTopCard(page);

  await pullUpTheDetailsPane(page);
  await readDownTheDetailsPane(page);
  await pushTheDetailsPaneBackDown(page);

  await page.waitForTimeout(DemoBeat.LINGER_ON_RESULT);
});
