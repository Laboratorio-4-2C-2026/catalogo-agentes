import type { ComponentType } from 'react';

export interface SlideDef {
  /** Short id, used in the URL hash and the check report. */
  id: string;
  /** The assertion headline, also shown in the presenter view. */
  title: string;
  /** Speaker notes: what is said on this slide (from the storytelling pack). */
  notes: string;
  Component: ComponentType;
}
