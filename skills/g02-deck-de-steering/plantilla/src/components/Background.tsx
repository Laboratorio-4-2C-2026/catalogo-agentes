import { useDeck } from '../deck/DeckContext';
import Aurora from './bits/Aurora';
import Grainient from './bits/Grainient';

// Citrus palette as hex, for the WebGL backgrounds.
const CITRUS = { grapefruit: '#e8415a', coral: '#f2735a', lemon: '#f5c842', lime: '#7dc242', cream: '#faf7f2', ink: '#1c1a18' };

/**
 * Full-bleed React Bits backgrounds tinted with the Citrus palette. In static
 * mode (PDF, presenter thumbnails, reduced motion) a CSS gradient stands in,
 * because WebGL canvases don't print reliably.
 */
export function Background({ kind }: { kind: 'grainient' | 'aurora' }) {
  const { isStatic } = useDeck();

  if (isStatic) {
    return (
      <div
        className="h-full w-full"
        style={{
          background:
            kind === 'grainient'
              ? `linear-gradient(55deg, ${CITRUS.grapefruit}, ${CITRUS.coral} 45%, ${CITRUS.lemon})`
              : `radial-gradient(ellipse at 50% 0%, ${CITRUS.coral}88, transparent 60%), ${CITRUS.ink}`,
        }}
      />
    );
  }

  if (kind === 'grainient') {
    return <Grainient colors={[CITRUS.grapefruit, CITRUS.coral, CITRUS.lemon]} interactive={false} clickSwirl={false} speed={0.4} />;
  }

  return <Aurora colorStops={[CITRUS.grapefruit, CITRUS.lemon, CITRUS.coral]} amplitude={0.9} speed={0.5} mouseInteraction={false} />;
}
