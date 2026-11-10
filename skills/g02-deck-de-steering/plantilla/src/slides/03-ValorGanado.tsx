import { Assertion } from '../components/Assertion';
import { Kicker } from '../components/Kicker';
import { Metric } from '../components/Metric';
import { SlideFrame } from '../components/SlideFrame';
import { cut, evm, indices } from '../data/numbers';

const nf = new Intl.NumberFormat('es-AR');

export function ValorGanado() {
  return (
    <SlideFrame className="justify-between">
      <div className="flex flex-col gap-8">
        <Kicker>{`Valor ganado · corte ${cut.date}`}</Kicker>
        <Assertion text="Vamos por encima del plan, y estamos revisando cuánto es mérito y cuánto método" size="md" />
      </div>
      <div className="grid grid-cols-2 gap-16">
        <Metric label="SPI" value={indices.spi} decimals={2} tone="good" formula={`EV / PV = ${nf.format(evm.ev)} / ${nf.format(evm.pv)}`} />
        <Metric label="CPI" value={indices.cpi} decimals={2} tone="good" formula={`EV / AC = ${nf.format(evm.ev)} / ${nf.format(evm.ac)}`} />
      </div>
      <p className="font-mono text-[20px] text-muted-foreground">Fuente: {cut.source}</p>
    </SlideFrame>
  );
}
