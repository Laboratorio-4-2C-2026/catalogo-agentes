import { spawn } from 'node:child_process';

const INSTALL_HINT =
  'Install it (winget install Gyan.FFmpeg) or point DEMO_FFMPEG_DIR at a build that contains ffmpeg and ffprobe.';

const binaryPath = (toolName) => {
  const directory = process.env.DEMO_FFMPEG_DIR;
  return directory ? `${directory}/${toolName}` : toolName;
};

const canRun = (executable) =>
  new Promise((resolve) => {
    const probe = spawn(executable, ['-version'], { stdio: 'ignore' });
    probe.on('error', () => resolve(false));
    probe.on('close', (exitCode) => resolve(exitCode === 0));
  });

export const locateFfmpegTool = async (toolName) => {
  const executable = binaryPath(toolName);
  if (!(await canRun(executable))) {
    throw new Error(`${toolName} is not available. ${INSTALL_HINT}`);
  }
  return executable;
};
