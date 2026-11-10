import { createContext, useContext } from 'react';

export interface DeckState {
  /**
   * True when animations must not run: print/PDF export, the presenter
   * thumbnails and prefers-reduced-motion. Components render their final state.
   */
  isStatic: boolean;
}

export const DeckContext = createContext<DeckState>({ isStatic: false });

export const useDeck = () => useContext(DeckContext);
