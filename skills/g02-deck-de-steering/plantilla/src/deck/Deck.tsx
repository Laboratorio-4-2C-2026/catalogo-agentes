import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { DeckContext } from './DeckContext';
import { Presenter } from './Presenter';
import { Stage, STAGE_H, STAGE_W } from './Stage';
import type { SlideDef } from './types';

const params = new URLSearchParams(window.location.search);
const MODE: 'present' | 'print' | 'presenter' = params.has('print')
  ? 'print'
  : params.has('presenter')
    ? 'presenter'
    : 'present';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const readHash = (total: number) => {
  const n = Number.parseInt(window.location.hash.slice(1), 10);
  return Number.isFinite(n) ? Math.min(Math.max(n - 1, 0), total - 1) : 0;
};

/**
 * The deck shell: navigation, URL hash, presenter sync and print mode.
 * Only the active slide is mounted, so its animations play every time it enters.
 */
export function Deck({ slides }: { slides: SlideDef[] }) {
  const total = slides.length;
  const [index, setIndex] = useState(() => readHash(total));
  const [showNotes, setShowNotes] = useState(false);
  const channel = useMemo(() => new BroadcastChannel('zest-deck'), []);
  const fromRemote = useRef(false);

  const go = useCallback((next: number) => setIndex(Math.min(Math.max(next, 0), total - 1)), [total]);

  // Keep the hash and the other window (presenter or audience) in sync.
  useEffect(() => {
    window.history.replaceState(null, '', `${window.location.search}#${index + 1}`);
    if (fromRemote.current) {
      fromRemote.current = false;
      return;
    }
    channel.postMessage({ index });
  }, [index, channel]);

  // Typing #7 in the URL (or the check script) jumps to that slide.
  useEffect(() => {
    const onHash = () => setIndex(readHash(total));
    window.addEventListener('hashchange', onHash);
    return () => window.removeEventListener('hashchange', onHash);
  }, [total]);

  useEffect(() => {
    channel.onmessage = (e: MessageEvent<{ index: number }>) => {
      fromRemote.current = true;
      setIndex(e.data.index);
    };
    return () => channel.close();
  }, [channel]);

  useEffect(() => {
    if (MODE === 'print') return;
    const onKey = (e: KeyboardEvent) => {
      if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) go(index + 1);
      else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) go(index - 1);
      else if (e.key === 'Home') go(0);
      else if (e.key === 'End') go(total - 1);
      else if (e.key === 'n' || e.key === 'N') setShowNotes(v => !v);
      else if (e.key === 'f' || e.key === 'F') void document.documentElement.requestFullscreen?.();
      else if (e.key === 'p' || e.key === 'P') window.open(`${window.location.pathname}?presenter#${index + 1}`, 'zest-presenter');
      else return;
      e.preventDefault();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [go, index, total]);

  if (MODE === 'print') {
    document.body.classList.add('print');
    return (
      <DeckContext.Provider value={{ isStatic: true }}>
        {slides.map(({ id, Component }) => (
          <div key={id} data-slide={id} style={{ width: STAGE_W, height: STAGE_H, position: 'relative', overflow: 'hidden', breakAfter: 'page' }}>
            <Component />
          </div>
        ))}
      </DeckContext.Provider>
    );
  }

  if (MODE === 'presenter') {
    return <Presenter slides={slides} index={index} go={go} />;
  }

  const { id, Component, notes } = slides[index];

  return (
    <DeckContext.Provider value={{ isStatic: reducedMotion }}>
      <div onClick={() => go(index + 1)} style={{ cursor: 'pointer' }}>
        <Stage>
          <div key={id} data-slide={id} style={{ position: 'absolute', inset: 0 }}>
            <Component />
          </div>
          <div style={{ position: 'absolute', left: 0, bottom: 0, height: 6, width: `${((index + 1) / total) * 100}%`, background: 'rgb(var(--grapefruit))', transition: 'width 300ms ease' }} />
        </Stage>
      </div>
      {showNotes && (
        <div className="fixed bottom-6 left-1/2 max-w-3xl -translate-x-1/2 rounded-xl bg-black/80 px-6 py-4 text-lg leading-relaxed text-white">
          {notes || 'Sin notas para esta slide.'}
        </div>
      )}
    </DeckContext.Provider>
  );
}
