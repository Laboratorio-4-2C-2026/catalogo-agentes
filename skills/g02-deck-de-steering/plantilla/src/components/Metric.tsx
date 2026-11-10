import { useEffect, useState } from 'react';
import { useDeck } from '../deck/DeckContext';

const format = (value: number, decimals: number) =>
  new Intl.NumberFormat('es-AR', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(value);

/**
 * A big number with what it means and how it was computed. Counts up on
 * enter (own implementation: React Bits CountUp has no Spanish decimal comma).
 */
export function Metric({
  label,
  value,
  decimals = 0,
  prefix = '',
  suffix = '',
  formula,
  tone = 'neutral',
}: {
  label: string;
  value: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  /** The calculation read out loud, e.g. "EV / PV = 6.124 / 4.493". */
  formula?: string;
  tone?: 'good' | 'watch' | 'alert' | 'neutral';
}) {
  const { isStatic } = useDeck();
  const [shown, setShown] = useState(isStatic ? value : 0);

  useEffect(() => {
    if (isStatic) return;
    const start = performance.now();
    const duration = 1100;
    let frame = 0;
    const tick = (t: number) => {
      const p = Math.min((t - start) / duration, 1);
      setShown(value * (1 - Math.pow(1 - p, 3)));
      if (p < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [value, isStatic]);

  const toneClass = { good: 'bg-lime', watch: 'bg-lemon', alert: 'bg-grapefruit', neutral: 'bg-border' }[tone];

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-3">
        <span className={`h-3 w-3 rounded-full ${toneClass}`} aria-hidden />
        <span className="font-mono text-[22px] uppercase tracking-[0.15em] text-muted-foreground">{label}</span>
      </div>
      <span className="font-mono text-[120px] font-medium leading-none tabular-nums">
        {prefix}
        {format(shown, decimals)}
        {suffix}
      </span>
      {formula && <span className="font-mono text-[24px] text-muted-foreground">{formula}</span>}
    </div>
  );
}
