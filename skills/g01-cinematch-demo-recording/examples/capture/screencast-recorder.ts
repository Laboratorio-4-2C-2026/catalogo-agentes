import { mkdir, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';

import type { Page } from '@playwright/test';

import { capturedFrameSize } from './recording-format';

/**
 * Every frame is JPEG-encoded inside the browser, and that encode is what
 * throttles the capture, so quality here is really a frame-rate dial.
 */
const FRAME_QUALITY = 80;

/**
 * Chrome emits a frame only when the page paints, so the gaps between frames
 * carry the demo's real timing. They are written out as concat-demuxer
 * durations, which is what keeps a still moment from racing past on playback.
 */
const TIMELINE_FILE_NAME = 'timeline.txt';
const MINIMUM_FRAME_SECONDS = 1 / 60;

interface CapturedFrame {
  fileName: string;
  timestamp: number;
}

const frameFileName = (index: number) =>
  `frame-${String(index).padStart(5, '0')}.jpg`;

const timelineFor = (frames: CapturedFrame[]): string => {
  const lines = frames.flatMap((frame, index) => {
    const next = frames[index + 1];
    const seconds = next
      ? Math.max(next.timestamp - frame.timestamp, MINIMUM_FRAME_SECONDS)
      : MINIMUM_FRAME_SECONDS;
    return [`file '${frame.fileName}'`, `duration ${seconds.toFixed(4)}`];
  });

  const lastFrame = frames[frames.length - 1];
  return [...lines, `file '${lastFrame.fileName}'`, ''].join('\n');
};

export interface Screencast {
  stop(): Promise<void>;
}

export const startScreencast = async (
  page: Page,
  framesDirectory: string,
): Promise<Screencast> => {
  await rm(framesDirectory, { recursive: true, force: true });
  await mkdir(framesDirectory, { recursive: true });

  const client = await page.context().newCDPSession(page);
  const frames: CapturedFrame[] = [];
  let pendingWrites: Promise<unknown> = Promise.resolve();

  client.on('Page.screencastFrame', ({ data, metadata, sessionId }) => {
    const fileName = frameFileName(frames.length);
    frames.push({ fileName, timestamp: metadata.timestamp ?? 0 });
    pendingWrites = pendingWrites.then(() =>
      writeFile(path.join(framesDirectory, fileName), data, 'base64'),
    );
    void client
      .send('Page.screencastFrameAck', { sessionId })
      .catch(() => undefined);
  });

  await client.send('Page.startScreencast', {
    format: 'jpeg',
    quality: FRAME_QUALITY,
    maxWidth: capturedFrameSize.width,
    maxHeight: capturedFrameSize.height,
    everyNthFrame: 1,
  });

  return {
    stop: async () => {
      await client.send('Page.stopScreencast');
      await pendingWrites;
      if (frames.length === 0) {
        throw new Error('The screencast produced no frames.');
      }
      await writeFile(
        path.join(framesDirectory, TIMELINE_FILE_NAME),
        timelineFor(frames),
      );
    },
  };
};
