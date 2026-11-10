import { useEffect, useState } from 'react';
import { DeckContext } from './DeckContext';
import { Stage } from './Stage';
import type { SlideDef } from './types';

const fmt = (s: number) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;

/**
 * Presenter view (open with P): current and next slide, notes, timer. It
 * drives the audience window through the shared BroadcastChannel.
 */
export function Presenter({ slides, index, go }: { slides: SlideDef[]; index: number; go: (n: number) => void }) {
  const [start, setStart] = useState(() => Date.now());
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    const t = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(t);
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (['ArrowRight', 'PageDown', ' '].includes(e.key)) go(index + 1);
      else if (['ArrowLeft', 'PageUp'].includes(e.key)) go(index - 1);
      else if (e.key === 'r' || e.key === 'R') setStart(Date.now());
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [go, index]);

  const current = slides[index];
  const next = slides[index + 1];

  return (
    <DeckContext.Provider value={{ isStatic: true }}>
      <div className="grid h-full grid-cols-[3fr_2fr] gap-6 bg-neutral-900 p-6 font-sans text-neutral-100">
        <div className="flex flex-col gap-4">
          <div className="overflow-hidden rounded-xl ring-1 ring-white/10">
            <Stage width={960} height={540}>
              <current.Component />
            </Stage>
          </div>
          <div className="flex-1 overflow-auto rounded-xl bg-neutral-800 p-6 text-2xl leading-relaxed">
            {current.notes || <span className="text-neutral-500">Sin notas.</span>}
          </div>
        </div>
        <div className="flex flex-col gap-4">
          <div className="flex items-baseline justify-between font-mono">
            <span className="text-5xl">{fmt(Math.floor((now - start) / 1000))}</span>
            <span className="text-2xl text-neutral-400">
              {index + 1} / {slides.length}
            </span>
          </div>
          <p className="text-neutral-400">Siguiente</p>
          {next ? (
            <div className="overflow-hidden rounded-xl opacity-80 ring-1 ring-white/10">
              <Stage width={560} height={315}>
                <next.Component />
              </Stage>
            </div>
          ) : (
            <p className="text-neutral-500">Última slide</p>
          )}
          <p className="mt-auto text-sm text-neutral-500">← → navegan · R reinicia el reloj</p>
        </div>
      </div>
    </DeckContext.Provider>
  );
}
