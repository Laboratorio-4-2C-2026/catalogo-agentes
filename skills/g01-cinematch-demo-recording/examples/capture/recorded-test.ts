import path from 'node:path';

import { test as base } from '@playwright/test';

import { startScreencast, type Screencast } from './screencast-recorder';

export const FRAMES_DIRECTORY = path.join(
  __dirname,
  '..',
  'recordings',
  'frames',
);

export interface Recording {
  start(): Promise<void>;
}

/**
 * Filming starts where the scenario says it does, so that whatever the app does
 * on its way to the opening shot stays out of the video. Stopping is automatic.
 */
export const test = base.extend<{ recording: Recording }>({
  recording: async ({ page }, use) => {
    const inProgress: { screencast?: Screencast } = {};

    await use({
      start: async () => {
        inProgress.screencast = await startScreencast(page, FRAMES_DIRECTORY);
      },
    });

    if (!inProgress.screencast) {
      throw new Error('The demo finished without ever starting the recording.');
    }
    await inProgress.screencast.stop();
  },
});

export { expect } from '@playwright/test';
