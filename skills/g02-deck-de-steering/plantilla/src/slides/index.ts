import type { SlideDef } from '../deck/types';
import { Portada } from './01-Portada';
import { Aseveracion } from './02-Aseveracion';
import { ValorGanado } from './03-ValorGanado';
import { CurvaS } from './04-CurvaS';
import { Demo } from './05-Demo';
import { Cierre } from './06-Cierre';

/**
 * The deck, in order. `title` is the assertion (read the titles alone: they
 * should tell the whole story). `notes` are the speaker lines.
 */
export const slides: SlideDef[] = [
  { id: 'portada', title: 'Zest · Steering 3', notes: 'Buenas tardes. Tercer Steering Committee de Zest.', Component: Portada },
  { id: 'estado', title: 'Los cuatro módulos del Sprint 1 y 2 están en producción', notes: 'Repasamos en diez segundos lo que ya está andando.', Component: Aseveracion },
  { id: 'valor-ganado', title: 'Vamos por encima del plan, y estamos revisando cuánto es mérito y cuánto método', notes: 'SPI es valor ganado sobre planificado... (ver skill de gestión).', Component: ValorGanado },
  { id: 'curva-s', title: 'El valor ganado se separó del plan a partir de setiembre', notes: 'Leer la curva: PV punteado, EV en rojo, AC en negro.', Component: CurvaS },
  { id: 'demo', title: 'Demo: el domingo de Sofi', notes: 'Pasar a la app. Guion en demo.md.', Component: Demo },
  { id: 'cierre', title: 'Gracias', notes: '¿Preguntas?', Component: Cierre },
];
