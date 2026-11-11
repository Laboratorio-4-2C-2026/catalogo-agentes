# Spike de dirección (no producto): golden set v2 de casos difíciles.
# Uso: SSL_CERT_FILE=/etc/ssl/cert.pem python3 correr.py panel
#      SSL_CERT_FILE=/etc/ssl/cert.pem python3 correr.py motor <actual|mejorado> <v1|v2> <n>
# El motor se llama como en medir.py: Vertex gemini-3.1-flash-lite, global, temperatura 0, sin thinking,
# con las instrucciones de formato del Structured Output Parser de n8n.
import json, re, sys, time, subprocess, urllib.request, concurrent.futures as cf
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[2]
sys.argv, _argv = sys.argv[:1] + ['vertex:gemini-3.1-flash-lite'], sys.argv  # medir.py lee argv al importarse
# medir.py vive en la pieza hermana g14-benchmark-de-modelos-del-motor
exec(compile((AQUI.parent / 'g14-benchmark-de-modelos-del-motor/medir.py').read_text().split('\nmodel = sys.argv[1]')[0], 'medir.py', 'exec'))
sys.argv = _argv
PANEL = ['z-ai/glm-5.3', 'deepseek/deepseek-v4-pro', 'moonshotai/kimi-k3']

def casos(planilla):  # mismo parser que medir.py, para cualquier letra
    out = {}
    for caso in re.split(r'^## Caso ', planilla, flags=re.M)[1:]:
        h = re.search(r'^\*\*(.+?)\*\* · (.+?) · cantidad (\d+) · estado: (.+)$\n\n> (.+)$', caso, re.M)
        don = dict(titulo=h[1], categoria=h[2], cantidad=int(h[3]), estado_objeto=h[4], descripcion=h[5])
        filas = re.findall(r'^\| ([A-Z]\d) \| \*\*(.+?)\*\* · (.+?) · cant\. (\d+) — «(.+)» \|', caso, re.M)
        out[caso[0]] = dict(texto=caso.split('\n---')[0], don=don,
                            pares=[(r[0], dict(titulo=r[1], categoria=r[2], cantidad=int(r[3]), descripcion=r[4]), don) for r in filas])
    return out

def openrouter(model, text):
    body = dict(model=model, temperature=0, messages=[dict(role='user', content=text)], usage=dict(include=True))
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', json.dumps(body).encode(), {'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r['choices'][0]['message']['content'], r['usage'].get('cost', 0)

def panel():
    plan = (AQUI / 'planilla.md').read_text()
    cabecera = plan.split('\n---')[0].split('\n', 2)[2]
    cs = casos(plan)
    def uno(m, c):
        ids = [p[0] for p in cs[c]['pares']]
        text = (cabecera + '\n\n## Caso ' + cs[c]['texto'] + '\n\nRespondé sólo con un objeto JSON: {"niveles": {' +
                ', '.join(f'"{i}": <0-4>' for i in ids) + '}, "top1": "<id>"}')
        for _ in range(3):
            try:
                c_, cost = openrouter(m, text)
                out = json.loads(re.search(r'\{.*\}', c_, re.S)[0])
                assert set(out['niveles']) == set(ids) and all(v in range(5) for v in out['niveles'].values())
                return m, c, out, cost
            except Exception as e:
                err = repr(e)[:200]
        return m, c, dict(error=err), 0
    with cf.ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda mc: uno(*mc), [(m, c) for m in PANEL for c in cs]))
    out = dict(fecha=time.strftime('%Y-%m-%d %H:%M'), modelos=PANEL, juicios={f'{m}|{c}': o for m, c, o, _ in res}, costo=sum(r[3] for r in res))
    (AQUI / 'panel.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps(out, ensure_ascii=False))

def motor(cual, set_, n):
    global PROMPT, VERTEX
    VERTEX = vertex_token()
    if cual == 'mejorado':
        PROMPT = (AQUI / 'prompt-mejorado.txt').read_text().rstrip('\n')
    plan = (ROOT / 'docs/qa/golden-set-v1-planilla.md' if set_ == 'v1' else AQUI / 'planilla.md').read_text()
    pares = [p for c in casos(plan).values() for p in c['pares']]
    with cf.ThreadPoolExecutor(4) as ex:
        res = sorted(ex.map(lambda p: juzgar('vertex:gemini-3.1-flash-lite', *p, {'thinkingConfig': {'thinkingBudget': 0}}), pares))
    out = dict(fecha=time.strftime('%Y-%m-%d %H:%M'), prompt=cual, set=set_, corrida=n, version=sorted({str(r[4]) for r in res}),
               niveles={r[0]: r[1] for r in res}, errores=[r for r in res if r[1] is None])
    (AQUI / f'corrida-{cual}-{set_}-{n}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(cual, set_, n, out['version'], 'errores', len(out['errores']))

if __name__ == '__main__':
    panel() if sys.argv[1] == 'panel' else motor(*sys.argv[2:5])
