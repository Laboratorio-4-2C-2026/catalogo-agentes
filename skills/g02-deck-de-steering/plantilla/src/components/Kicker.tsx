/** The small all-caps label above a headline, like "ESTADO DEL PROYECTO". */
export function Kicker({ children }: { children: string }) {
  return <p className="font-mono text-[18px] uppercase tracking-[0.2em] text-grapefruit">{children}</p>;
}
