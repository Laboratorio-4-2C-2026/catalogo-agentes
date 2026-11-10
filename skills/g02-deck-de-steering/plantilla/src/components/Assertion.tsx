import { useDeck } from '../deck/DeckContext';
import SplitText from './bits/SplitText';

const SIZES = { xl: 'text-[120px] leading-[1.02]', lg: 'text-[88px] leading-[1.05]', md: 'text-[64px] leading-[1.1]' };

/**
 * The slide's headline: one complete sentence that states the takeaway
 * ("El planificador cierra el recorrido de Sofi"), not a topic ("Planificador").
 * Animates with React Bits SplitText unless the deck is static.
 */
export function Assertion({ text, size = 'lg', align = 'left' }: { text: string; size?: keyof typeof SIZES; align?: 'left' | 'center' }) {
  const { isStatic } = useDeck();
  const className = `font-serif font-medium text-foreground ${SIZES[size]} max-w-[1500px]`;

  if (isStatic) {
    return <h1 className={className} style={{ textAlign: align }}>{text}</h1>;
  }

  return (
    <SplitText
      text={text}
      tag="h1"
      className={className}
      splitType="words"
      delay={40}
      duration={0.9}
      effect="rise"
      trigger="load"
      textAlign={align}
    />
  );
}
