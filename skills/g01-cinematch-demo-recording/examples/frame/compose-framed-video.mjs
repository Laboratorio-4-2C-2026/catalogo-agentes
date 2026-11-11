import { spawn } from 'node:child_process';

import { locateFfmpegTool } from './ffmpeg-location.mjs';

/** The capture peaks at 60fps during gestures; resampling lower discards it. */
const OUTPUT_FRAME_RATE = 60;
const QUALITY_FACTOR = '16';

/**
 * The frame is used twice: once as the backdrop the recording is dropped into,
 * and once on top, so its rounded inner edge clips the square video corners.
 */
const buildFilterGraph = (geometry) =>
  [
    '[0:v]split=2[backdrop][edge]',
    `[1:v]scale=${geometry.screenWidth}:${geometry.screenHeight}:flags=lanczos[screen]`,
    `[backdrop][screen]overlay=${geometry.screenLeft}:${geometry.screenTop}:shortest=1[screened]`,
    // The rate is settled once, at the end: an overlay takes its timing from
    // the backdrop, which is a still image loop and knows nothing about pace.
    `[screened][edge]overlay=0:0:shortest=1,fps=${OUTPUT_FRAME_RATE}[framed]`,
  ].join(';');

const runToCompletion = (executable, args) =>
  new Promise((resolve, reject) => {
    const child = spawn(executable, args, { stdio: 'inherit' });
    child.on('error', reject);
    child.on('close', (exitCode) =>
      exitCode === 0
        ? resolve()
        : reject(new Error(`${executable} exited with code ${exitCode}.`)),
    );
  });

export const composeFramedVideo = async ({
  timelinePath,
  framePath,
  geometry,
  outputPath,
}) => {
  const ffmpeg = await locateFfmpegTool('ffmpeg');
  await runToCompletion(ffmpeg, [
    '-y',
    '-loop',
    '1',
    '-framerate',
    String(OUTPUT_FRAME_RATE),
    '-i',
    framePath,
    // The captured frames carry their own timing, so they arrive through the
    // concat demuxer rather than at a fixed input frame rate.
    '-f',
    'concat',
    '-safe',
    '0',
    '-i',
    timelinePath,
    '-filter_complex',
    buildFilterGraph(geometry),
    '-map',
    '[framed]',
    '-c:v',
    'libx264',
    '-pix_fmt',
    'yuv420p',
    '-crf',
    QUALITY_FACTOR,
    '-preset',
    'slow',
    '-movflags',
    '+faststart',
    outputPath,
  ]);
};
