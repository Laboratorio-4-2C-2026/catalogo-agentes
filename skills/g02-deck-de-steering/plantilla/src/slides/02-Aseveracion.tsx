import { Assertion } from '../components/Assertion';
import { Kicker } from '../components/Kicker';
import { SlideFrame } from '../components/SlideFrame';

/** Assertion–evidence layout: the headline is the claim, the body is the proof. */
export function Aseveracion() {
  return (
    <SlideFrame className="justify-between">
      <div className="flex flex-col gap-8">
        <Kicker>Estado del proyecto</Kicker>
        <Assertion text="Los cuatro módulos del Sprint 1 y 2 están en producción" />
      </div>
      <div className="grid grid-cols-4 gap-8">
        {[
          ['Gestión de recetas', 'Crear, editar, eliminar'],
          ['Explorador', 'Feed, búsqueda y filtros'],
          ['Usuarios', 'Login con Auth0 y perfiles'],
          ['Colecciones', 'Guardar y organizar'],
        ].map(([name, detail]) => (
          <div key={name} className="rounded-3xl border border-border bg-card p-10">
            <span className="mb-6 block h-3 w-3 rounded-full bg-lime" aria-hidden />
            <p className="font-serif text-[40px] leading-tight">{name}</p>
            <p className="mt-3 text-[26px] text-muted-foreground">{detail}</p>
          </div>
        ))}
      </div>
    </SlideFrame>
  );
}
