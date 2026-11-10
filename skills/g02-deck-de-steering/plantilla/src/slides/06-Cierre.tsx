import { Background } from '../components/Background';
import { SlideFrame } from '../components/SlideFrame';

export function Cierre() {
  return (
    <SlideFrame dark background={<Background kind="grainient" />} className="justify-center">
      <p className="font-serif text-[140px] leading-none text-white">Gracias</p>
      <p className="mt-8 text-[40px] text-white/85">¿Preguntas?</p>
    </SlideFrame>
  );
}
