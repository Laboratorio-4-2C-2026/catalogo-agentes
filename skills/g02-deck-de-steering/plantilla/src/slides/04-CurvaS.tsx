import { Assertion } from '../components/Assertion';
import { ExampleBadge } from '../components/ExampleBadge';
import { Kicker } from '../components/Kicker';
import { SCurve } from '../components/SCurve';
import { SlideFrame } from '../components/SlideFrame';
import { curve, evm } from '../data/numbers';

export function CurvaS() {
  return (
    <SlideFrame className="justify-between">
      {curve.isExample && <ExampleBadge source="la planilla 10B" />}
      <div className="flex flex-col gap-6">
        <Kicker>Curva S</Kicker>
        <Assertion text="El valor ganado se separó del plan a partir de setiembre" size="md" />
      </div>
      <SCurve points={curve.points} bac={evm.bac} cutIndex={curve.cutIndex} />
    </SlideFrame>
  );
}
