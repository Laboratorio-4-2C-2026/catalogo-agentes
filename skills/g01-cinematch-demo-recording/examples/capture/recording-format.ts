/**
 * A device descriptor's viewport is the browser's content area, with the mobile
 * browser UI already subtracted (393x659 for an iPhone 15). The demo draws a
 * phone around the recording, so it films the whole screen instead.
 */
export const PHONE_SCREEN = { width: 393, height: 852 };

/**
 * Chrome's screencast hands back frames at the compositor's own resolution and
 * refuses to enlarge them, and an *emulated* device scale factor does not move
 * that resolution: only a real one does. Forcing it on the browser is what
 * makes the capture 3x while the page still lays out at a phone's CSS width.
 */
export const CAPTURE_SCALE = 2;

export const capturedFrameSize = {
  width: PHONE_SCREEN.width * CAPTURE_SCALE,
  height: PHONE_SCREEN.height * CAPTURE_SCALE,
};

export const chromiumScaleArguments = [
  `--force-device-scale-factor=${CAPTURE_SCALE}`,
  `--window-size=${PHONE_SCREEN.width},${PHONE_SCREEN.height}`,
];
