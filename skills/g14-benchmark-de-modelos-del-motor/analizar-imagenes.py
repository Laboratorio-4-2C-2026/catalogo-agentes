# Resume las corridas contra el criterio fijado en README.md antes de correr.
import json, re, statistics
from collections import Counter
from pathlib import Path
AQUI = Path(__file__).resolve().parent
QA = AQUI.parent
ref = dict(v1={m[0]: int(m[1]) for m in re.findall(r'^\| ([A-F]\d) \|.*\*\*(\d)\*\* \|', (QA / 'golden-set-v1.md').read_text(), re.M)},
           v2=json.loads((QA / 'golden-set-v2-spike/niveles-v2.json').read_text()))
PRECIO_IN, PRECIO_OUT = 0.25e-6, 1.50e-6

def cargar(b, s):
    runs = [json.loads((AQUI / f'corridas/{b}-{s}-{n}.json').read_text())['resultados'] for n in (1, 2, 3)]
    assert all(r['nivel'] is not None for run in runs for r in run), (b, s)
    return runs

def moda(runs):
    return {r['id']: Counter(run[i]['nivel'] for run in runs).most_common(1)[0][0] for i, r in enumerate(runs[0])}

def costo(runs):
    todas = [r for run in runs for r in run]
    lat = sorted(r['lat'] for r in todas)
    return dict(lat_media=statistics.mean(lat), p95=lat[int(.95 * (len(lat) - 1))], ent=statistics.mean(r['entrada'] for r in todas),
                sal=statistics.mean(r['salida'] for r in todas), usd=statistics.mean(r['entrada'] * PRECIO_IN + r['salida'] * PRECIO_OUT for r in todas),
                total=sum(r['entrada'] * PRECIO_IN + r['salida'] * PRECIO_OUT for r in todas))

pasa, total = True, 0
for s in ('v1', 'v2'):
    R = ref[s]; m = {b: moda(cargar(b, s)) for b in 'AB'}
    for b in 'AB':
        runs = cargar(b, s)
        ex = [sum(r['nivel'] == R[r['id']] for r in run) for run in runs]
        c = costo(runs); total += c['total']
        malo = [i for i in R if (m[b][i] <= 1) != (R[i] <= 1)]
        print(f'{b} {s}: exacto moda {sum(m[b][i] == R[i] for i in R)}/{len(R)} (corridas {ex}) · cruzan Malo {malo} · '
              f'lat {c["lat_media"]:.2f}/p95 {c["p95"]:.2f} s · tokens {c["ent"]:.0f}+{c["sal"]:.0f} · US${c["usd"]*1000:.3f}/1000 llamadas')
        print('   fallos (ref→moda):', ' '.join(f'{i} {R[i]}→{m[b][i]}' for i in R if m[b][i] != R[i]))
    pierde = [i for i in R if m['A'][i] == R[i] != m['B'][i]]
    gana = [i for i in R if m['B'][i] == R[i] != m['A'][i]]
    cruza_nuevo = [i for i in R if (m['B'][i] <= 1) != (R[i] <= 1) and (m['A'][i] <= 1) == (R[i] <= 1)]
    ok = len(pierde) <= 1 and not cruza_nuevo  # pares perdidos brutos, como en el spike v2; el neto se informa aparte
    pasa &= ok
    print(f'{s}: B gana {gana} · pierde {pierde} · neto {len(gana) - len(pierde):+d} · cruza nuevo {cruza_nuevo} → {"OK" if ok else "FALLA"}')
A, B = moda(cargar('A', 'adv')), moda(cargar('B', 'adv'))
for b in 'AB':
    total += costo(cargar(b, 'adv'))['total']
print('adversarial A:', A, ' B:', B, ' B < A:', [i for i in A if B[i] < A[i]])
print('VEREDICTO:', 'PASA' if pasa else 'NO PASA', f'· costo total estimado US${total:.3f}')
