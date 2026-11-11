const SIDE_BEZEL_RATIO = 0.06;
const TOP_BEZEL_RATIO = 0.085;
const OUTER_CORNER_RATIO = 0.13;
const SCREEN_CORNER_RATIO = 0.075;

const BEZEL_COLOR = '#0B0B10';
const BEZEL_EDGE_COLOR = 'rgba(255,255,255,0.14)';
const BEZEL_EDGE_WIDTH = 2;

const roundToEven = (value) => Math.round(value / 2) * 2;

/** Every dimension is even because the h264 encoder rejects odd ones. */
export const phoneFrameGeometry = (requestedWidth, requestedHeight) => {
  const screenWidth = roundToEven(requestedWidth);
  const screenHeight = roundToEven(requestedHeight);
  const sideBezel = roundToEven(screenWidth * SIDE_BEZEL_RATIO);
  const topBezel = roundToEven(screenWidth * TOP_BEZEL_RATIO);

  return {
    screenWidth,
    screenHeight,
    screenLeft: sideBezel,
    screenTop: topBezel,
    totalWidth: screenWidth + sideBezel * 2,
    totalHeight: screenHeight + topBezel * 2,
    outerCornerRadius: roundToEven(screenWidth * OUTER_CORNER_RATIO),
    screenCornerRadius: roundToEven(screenWidth * SCREEN_CORNER_RATIO),
  };
};

/**
 * The screen area is cut out so the recording can be composited underneath,
 * while the rounded inner edge stays on top of it and clips the video corners.
 */
export const buildPhoneFrameSvg = (geometry) => `
<svg xmlns="http://www.w3.org/2000/svg" width="${geometry.totalWidth}" height="${geometry.totalHeight}" viewBox="0 0 ${geometry.totalWidth} ${geometry.totalHeight}">
  <defs>
    <mask id="screen-cutout">
      <rect width="${geometry.totalWidth}" height="${geometry.totalHeight}" rx="${geometry.outerCornerRadius}" fill="white"/>
      <rect x="${geometry.screenLeft}" y="${geometry.screenTop}" width="${geometry.screenWidth}" height="${geometry.screenHeight}" rx="${geometry.screenCornerRadius}" fill="black"/>
    </mask>
  </defs>
  <rect width="${geometry.totalWidth}" height="${geometry.totalHeight}" rx="${geometry.outerCornerRadius}" fill="${BEZEL_COLOR}" mask="url(#screen-cutout)"/>
  <rect x="${BEZEL_EDGE_WIDTH / 2}" y="${BEZEL_EDGE_WIDTH / 2}" width="${geometry.totalWidth - BEZEL_EDGE_WIDTH}" height="${geometry.totalHeight - BEZEL_EDGE_WIDTH}" rx="${geometry.outerCornerRadius}" fill="none" stroke="${BEZEL_EDGE_COLOR}" stroke-width="${BEZEL_EDGE_WIDTH}"/>
</svg>
`;
