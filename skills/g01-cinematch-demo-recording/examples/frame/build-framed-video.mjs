import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { composeFramedVideo } from './compose-framed-video.mjs';
import { buildPhoneFrameSvg, phoneFrameGeometry } from './phone-frame.mjs';
import { rasterizeSvgToPng } from './rasterize-svg.mjs';
import { readImageDimensions } from './image-dimensions.mjs';

const recordingsDirectory = path.join(
  path.dirname(fileURLToPath(import.meta.url)),
  '..',
  'recordings',
);

const framesDirectory =
  process.argv[2] ?? path.join(recordingsDirectory, 'frames');
const timelinePath = path.join(framesDirectory, 'timeline.txt');
const framePath = path.join(recordingsDirectory, 'phone-frame.png');
const outputPath = path.join(recordingsDirectory, 'cinematch-demo.mp4');

const capturedSize = await readImageDimensions(
  path.join(framesDirectory, 'frame-00000.jpg'),
);
const geometry = phoneFrameGeometry(capturedSize.width, capturedSize.height);

await rasterizeSvgToPng(buildPhoneFrameSvg(geometry), {
  width: geometry.totalWidth,
  height: geometry.totalHeight,
  outputPath: framePath,
});

await composeFramedVideo({ timelinePath, framePath, geometry, outputPath });

console.log(`Framed demo written to ${outputPath}`);
