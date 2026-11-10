/**
 * Shown on any slide whose data is still an example. It must be gone before
 * presenting: `npm run check` fails while it appears.
 */
export function ExampleBadge({ source }: { source: string }) {
  return (
    <div data-example-data className="absolute right-[120px] top-[96px] rounded-full bg-lemon px-5 py-2 font-mono text-[18px] text-foreground">
      DATO DE EJEMPLO · reemplazar con {source}
    </div>
  );
}
