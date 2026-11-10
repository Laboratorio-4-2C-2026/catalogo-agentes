import type { ReactNode } from 'react';

/**
 * Every slide starts here: a 1920×1080 surface with the deck's margins.
 * `dark` flips the neutral tokens; `background` sits behind the content
 * (a React Bits background, an image...).
 */
export function SlideFrame({
  children,
  dark = false,
  background,
  className = '',
}: {
  children: ReactNode;
  dark?: boolean;
  background?: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`${dark ? 'theme-dark' : ''} absolute inset-0 overflow-hidden bg-background text-foreground`}
    >
      {background && <div className="absolute inset-0">{background}</div>}
      <div className={`relative flex h-full flex-col px-[120px] py-[96px] ${className}`}>{children}</div>
    </section>
  );
}
