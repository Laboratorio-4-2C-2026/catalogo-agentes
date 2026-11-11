# Spike de dirección (no producto): ¿el juez empeora si ve la foto de la donación?
# Uso: SSL_CERT_FILE=/etc/ssl/cert.pem python3 correr.py <A|B> <v1|v2|adv> <n>
# Reusa correr.py del spike v2 (que reusa medir.py): mismo prompt, mismo parser, mismas credenciales de Vertex.
import base64, importlib.util, json, re, sys, time, urllib.request, concurrent.futures as cf
from pathlib import Path

AQUI = Path(__file__).resolve().parent
QA = AQUI.parent
# correr.py vive en la pieza hermana g14-eval-del-juez-contra-golden-set
spec = importlib.util.spec_from_file_location('v2', AQUI.parent / 'g14-eval-del-juez-contra-golden-set/correr.py')
v2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v2)
MODELO = 'gemini-3.1-flash-lite'
INSTR = ('La donación trae una foto adjunta. Tenela en cuenta junto con el texto al juzgar estado, tamaño y cantidad.\n'
         'En la narrativa mencioná brevemente qué se ve en la foto.\n')

def adversariales():
    v1 = v2.casos((QA / 'golden-set-v1-planilla.md').read_text()); vv = v2.casos((QA / 'golden-set-v2-spike/planilla.md').read_text())
    nec = {p[0]: p[1] for c in (*v1.values(), *vv.values()) for p in c['pares']}
    don = lambda c: dict(c['don'])
    return [('X1', nec['A2'], don(v1['A'])),
            ('X2', nec['G1'], dict(titulo='Heladera con freezer', categoria='Electrodomésticos', cantidad=1, estado_objeto='bueno',
                                   descripcion='heladera familiar con freezer, anda perfecto. la cambiamos por una mas nueva')),
            ('X3', nec['C2'], don(v1['C'])),
            ('X4', nec['I1'], don(vv['I'])),
            ('X5', nec['C4'], dict(titulo='Bicicleta rodado 26', categoria='Transporte', cantidad=1, estado_objeto='bueno',
                                   descripcion='bici rodado 26, anda perfecto, lista para usar')),
            ('X6', nec['L1'], don(vv['L']))]

def pares(set_):
    if set_ == 'adv':
        return adversariales()
    plan = (QA / 'golden-set-v1-planilla.md' if set_ == 'v1' else QA / 'golden-set-v2-spike/planilla.md').read_text()
    return [p for c in v2.casos(plan).values() for p in c['pares']]

def juzgar(brazo, pid, nec, don):
    text = v2.PROMPT.replace('{{ JSON.stringify($json.necesidad) }}', json.dumps(nec, ensure_ascii=False)).replace('{{ JSON.stringify($json.donacion) }}', json.dumps(don, ensure_ascii=False))
    parts = []
    if brazo == 'B':
        foto = AQUI / 'fotos' / f'{pid if pid[0] == "X" else pid[0]}.jpg'
        parts.append(dict(inlineData=dict(mimeType='image/jpeg', data=base64.b64encode(foto.read_bytes()).decode())))
        text += INSTR
    text += '\n\nYou must format your output as a JSON value that adheres to a given "JSON Schema" instance.\n\nHere is the JSON Schema instance your output must adhere to. Include the enclosing markdown codeblock:\n```json\n' + json.dumps(v2.SCHEMA) + '\n```\n'
    parts.append(dict(text=text))
    url = f'https://aiplatform.googleapis.com/v1/projects/{v2.VERTEX[0]}/locations/global/publishers/google/models/{MODELO}:generateContent'
    body = json.dumps(dict(contents=[dict(role='user', parts=parts)], generationConfig=dict(temperature=0, thinkingConfig=dict(thinkingBudget=0)))).encode()
    for intento in range(4):  # 429 / 5xx: reintento con espera; el reintento queda registrado
        t = time.time()
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(url, body, {'Authorization': f'Bearer {v2.VERTEX[1]}', 'Content-Type': 'application/json'}), timeout=120))
            dt = time.time() - t
            c = ''.join(p.get('text', '') for p in r['candidates'][0]['content']['parts'] if not p.get('thought'))
            out = json.loads(re.sub(r'^```(?:json)?|```$', '', c.strip()).strip())
            assert out['nivel'] in range(5) and {'narrativa', 'fortalezas', 'consideraciones'} <= set(out['justificacion'])
            u = r['usageMetadata']
            return dict(id=pid, nivel=out['nivel'], narrativa=out['justificacion']['narrativa'], lat=round(dt, 3), intentos=intento + 1,
                        entrada=u.get('promptTokenCount', 0), salida=u.get('candidatesTokenCount', 0), pensamiento=u.get('thoughtsTokenCount', 0),
                        version=r.get('modelVersion'))
        except Exception as e:
            err = repr(e)[:200]
            time.sleep(10 * (intento + 1))
    return dict(id=pid, nivel=None, error=err)

if __name__ == '__main__':
    brazo, set_, n = sys.argv[1:4]
    v2.VERTEX = v2.vertex_token()
    with cf.ThreadPoolExecutor(4) as ex:
        res = sorted(ex.map(lambda p: juzgar(brazo, *p), pares(set_)), key=lambda r: r['id'])
    out = dict(fecha=time.strftime('%Y-%m-%d %H:%M'), brazo=brazo, set=set_, corrida=n, resultados=res)
    (AQUI / 'corridas').mkdir(exist_ok=True)
    (AQUI / f'corridas/{brazo}-{set_}-{n}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(brazo, set_, n, 'errores', sum(r['nivel'] is None for r in res), 'reintentos', sum(r.get('intentos', 1) - 1 for r in res))
