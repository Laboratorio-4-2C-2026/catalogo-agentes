import { useDeck } from '../deck/DeckContext';

export interface CurvePoint {
  label: string;
  pv: number;
  ev?: number;
  ac?: number;
}

const W = 1400;
const H = 560;
const PAD = { l: 90, r: 160, t: 20, b: 60 };

const nf = new Intl.NumberFormat('es-AR');

/**
 * Earned value S-curve: PV dashed, EV solid grapefruit, AC solid foreground,
 * BAC as a labelled line, the cut date marked, and direct labels at the end of
 * each line instead of a legend. Lines draw in on enter.
 */
export function SCurve({ points, bac, cutIndex }: { points: CurvePoint[]; bac: number; cutIndex: number }) {
  const { isStatic } = useDeck();
  const max = bac * 1.08;
  const x = (i: number) => PAD.l + (i / (points.length - 1)) * (W - PAD.l - PAD.r);
  const y = (v: number) => PAD.t + (1 - v / max) * (H - PAD.t - PAD.b);

  const path = (key: 'pv' | 'ev' | 'ac') =>
    points
      .map((p, i) => (p[key] === undefined ? null : `${x(i)},${y(p[key] as number)}`))
      .filter(Boolean)
      .map((pt, i) => `${i === 0 ? 'M' : 'L'}${pt}`)
      .join(' ');

  const last = (key: 'pv' | 'ev' | 'ac') => {
    for (let i = points.length - 1; i >= 0; i--) if (points[i][key] !== undefined) return { i, v: points[i][key] as number };
    return null;
  };

  const draw = isStatic ? {} : { strokeDasharray: 4000, strokeDashoffset: 4000, animation: 'draw 1.6s ease-out forwards' };

  const series = [
    { key: 'pv' as const, label: 'PV', color: 'rgb(var(--muted-foreground))', dash: '10 10', delay: '0s' },
    { key: 'ac' as const, label: 'AC', color: 'rgb(var(--foreground))', dash: undefined, delay: '0.3s' },
    { key: 'ev' as const, label: 'EV', color: 'rgb(var(--grapefruit))', dash: undefined, delay: '0.6s' },
  ];

  return (
    <svg width={W} height={H} className="font-mono" role="img" aria-label="Curva S de valor ganado">
      <style>{'@keyframes draw { to { stroke-dashoffset: 0; } }'}</style>
      <line x1={PAD.l} x2={W - PAD.r} y1={y(bac)} y2={y(bac)} stroke="rgb(var(--border))" strokeWidth={2} />
      <text x={PAD.l} y={y(bac) - 12} fontSize={22} fill="rgb(var(--muted-foreground))">
        BAC {nf.format(bac)}
      </text>
      <line x1={x(cutIndex)} x2={x(cutIndex)} y1={PAD.t} y2={H - PAD.b} stroke="rgb(var(--lemon))" strokeWidth={3} />
      <text x={x(cutIndex) + 10} y={PAD.t + 24} fontSize={20} fill="rgb(var(--foreground))">
        Corte {points[cutIndex].label}
      </text>
      {points.map((p, i) =>
        i % 2 === 0 ? (
          <text key={p.label} x={x(i)} y={H - 20} fontSize={18} textAnchor="middle" fill="rgb(var(--muted-foreground))">
            {p.label}
          </text>
        ) : null,
      )}
      {series.map(s => {
        const end = last(s.key);
        return (
          <g key={s.key}>
            <path
              d={path(s.key)}
              fill="none"
              stroke={s.color}
              strokeWidth={s.key === 'ev' ? 6 : 4}
              strokeLinecap="round"
              style={s.dash ? { strokeDasharray: s.dash } : { ...draw, animationDelay: s.delay }}
            />
            {end && (
              <text x={x(end.i) + 14} y={y(end.v) + 7} fontSize={24} fontWeight={600} fill={s.color}>
                {s.label} {nf.format(end.v)}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}
