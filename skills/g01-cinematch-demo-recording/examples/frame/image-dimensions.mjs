import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

import { locateFfmpegTool } from './ffmpeg-location.mjs';

const execFileAsync = promisify(execFile);

export const readImageDimensions = async (imagePath) => {
  const ffprobe = await locateFfmpegTool('ffprobe');
  const { stdout } = await execFileAsync(ffprobe, [
    '-v',
    'error',
    '-select_streams',
    'v:0',
    '-show_entries',
    'stream=width,height',
    '-of',
    'json',
    imagePath,
  ]);

  const [stream] = JSON.parse(stdout).streams ?? [];
  if (!stream) {
    throw new Error(`No image stream found in ${imagePath}.`);
  }
  return { width: stream.width, height: stream.height };
};
