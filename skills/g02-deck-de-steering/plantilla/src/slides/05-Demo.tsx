import { Background } from '../components/Background';
import { SlideFrame } from '../components/SlideFrame';

/** Full-bleed transition into the live demo (script: decks/<evento>/demo.md). */
export function Demo() {
  return (
    <SlideFrame dark background={<Background kind="aurora" />} className="items-center justify-center text-center">
      <p className="font-mono text-[24px] uppercase tracking-[0.3em] text-white/70">Demo</p>
      <p className="mt-6 font-serif text-[120px] leading-tight text-white">El domingo de Sofi</p>
    </SlideFrame>
  );
}
