/**
 * Automation runs far faster than an audience can follow. Every pause the demo
 * takes is one of these beats, so the whole pace of the video is tunable here.
 */
export const DemoBeat = {
  AFTER_SCREEN_APPEARS: 1300,
  BEFORE_GESTURE: 850,
  AFTER_GESTURE: 1400,
  LINGER_ON_RESULT: 2800,
} as const;

export const TYPING_DELAY_MS = 90;
