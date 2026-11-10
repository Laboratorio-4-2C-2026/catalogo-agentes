import { useEffect, useState, type ReactNode } from 'react';

export const STAGE_W = 1920;
export const STAGE_H = 1080;

/**
 * Fixed 1920×1080 canvas scaled as a whole to fit its box. Slides are always
 * authored at 1920×1080 and never re-flow: the stage letterboxes instead.
 */
export function Stage({ children, width, height }: { children: ReactNode; width?: number; height?: number }) {
  const [box, setBox] = useState(() => ({ w: width ?? window.innerWidth, h: height ?? window.innerHeight }));

  useEffect(() => {
    if (width && height) {
      setBox({ w: width, h: height });
      return;
    }
    const onResize = () => setBox({ w: window.innerWidth, h: window.innerHeight });
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, [width, height]);

  const scale = Math.min(box.w / STAGE_W, box.h / STAGE_H);

  return (
    <div style={{ width: box.w, height: box.h, position: 'relative', overflow: 'hidden' }}>
      <div
        data-stage
        style={{
          position: 'absolute',
          width: STAGE_W,
          height: STAGE_H,
          left: (box.w - STAGE_W * scale) / 2,
          top: (box.h - STAGE_H * scale) / 2,
          transform: `scale(${scale})`,
          transformOrigin: 'top left',
          overflow: 'hidden',
        }}
      >
        {children}
      </div>
    </div>
  );
}
