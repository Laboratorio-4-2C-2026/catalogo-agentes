import { Background } from '../components/Background';
import { SlideFrame } from '../components/SlideFrame';
import { useDeck } from '../deck/DeckContext';
import BlurText from '../components/bits/BlurText';

export function Portada() {
  const { isStatic } = useDeck();
  return (
    <SlideFrame dark background={<Background kind="grainient" />} className="justify-end">
      <p className="font-mono text-[22px] uppercase tracking-[0.25em] text-white/80">Steering 3 · Laboratorio II y IV · 12/11/2026</p>
      {isStatic ? (
        <h1 className="mt-6 font-serif text-[260px] font-medium leading-none text-white">Zest</h1>
      ) : (
        <BlurText text="Zest" className="mt-6 font-serif text-[260px] font-medium leading-none text-white" animateBy="letters" delay={120} trigger="load" />
      )}
      <p className="mt-8 max-w-[1100px] text-[36px] leading-snug text-white/90">
        Descubrir, guardar, organizar y planificar recetas en un solo lugar.
      </p>
    </SlideFrame>
  );
}
