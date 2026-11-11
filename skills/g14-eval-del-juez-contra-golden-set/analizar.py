# Resume las corridas contra los niveles de referencia. Criterios fijados en golden-set-v2-spike.md antes de correr.
import json, re, statistics
from collections import Counter
from pathlib import Path
AQUI = Path(__file__).resolve().parent
ref = dict(v1={m[0]: int(m[1]) for m in re.findall(r'^\| ([A-F]\d) \|.*\*\*(\d)\*\* \|', (AQUI.parent / 'golden-set-v1.md').read_text(), re.M)},
           v2=json.loads((AQUI / 'niveles-v2.json').read_text()))
res = {}
for p in ('actual', 'mejorado'):
    for s in ('v1', 'v2'):
        runs = [json.loads((AQUI / f'corrida-{p}-{s}-{n}.json').read_text())['niveles'] for n in (1, 2, 3)]
        assert all(None not in r.values() and set(r) == set(ref[s]) for r in runs)
        ex = [sum(r[i] == ref[s][i] for i in ref[s]) for r in runs]
        ml = [sum((r[i] <= 1) == (ref[s][i] <= 1) for i in ref[s]) for r in runs]
        moda = {i: Counter(r[i] for r in runs).most_common(1)[0][0] for i in ref[s]}
        inest = sorted(i for i in ref[s] if len({r[i] <= 1 for r in runs}) > 1)
        res[p, s] = dict(moda=moda)
        print(f'{p:9} {s}  exacto {min(ex)}–{max(ex)}/{len(ref[s])} ({min(ex)/len(ref[s]):.0%}–{max(ex)/len(ref[s]):.0%})'
              f'  linea Malo {min(ml)}–{max(ml)}/{len(ref[s])}  inestables Malo {inest}')
        print('          por par (ref: corridas):', ' '.join(f'{i}={ref[s][i]}:{"".join(str(r[i]) for r in runs)}' for i in ref[s] if any(r[i] != ref[s][i] for r in runs)))
for s in ('v1', 'v2'):
    a, m = res['actual', s]['moda'], res['mejorado', s]['moda']
    gana = [i for i in ref[s] if m[i] == ref[s][i] != a[i]]
    pierde = [i for i in ref[s] if a[i] == ref[s][i] != m[i]]
    print(f'{s}: mejorado gana {gana} · pierde {pierde} (por moda de 3, nivel exacto)')
