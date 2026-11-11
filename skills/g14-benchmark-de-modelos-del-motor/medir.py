# Medición de dirección (no producto): prompt del motor sobre el golden set v1 vía OpenRouter.
# Uso: SSL_CERT_FILE=/etc/ssl/cert.pem python3 medir.py google/gemini-3.1-flash-lite '{"reasoning":{"effort":"none"}}'
#      SSL_CERT_FILE=/etc/ssl/cert.pem python3 medir.py vertex:gemini-3.1-flash-lite '{"thinkingConfig":{"thinkingBudget":0}}'
#      (vertex: usa la service account de ~/.config/vaiven/vertex-n8n.json; el extra va a generationConfig)
import json, re, sys, time, statistics, subprocess, urllib.request, concurrent.futures as cf
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MODO = 'parser'
KEY = next(l.split('=', 1)[1].strip().strip('"') for l in (ROOT / 'vaivendev/.env').read_text().splitlines() if l.startswith('OPENROUTER_API_KEY='))
wf = json.loads(subprocess.run(['git', '-C', str(ROOT / 'ai-config/vaiven-app'), 'show', 'origin/main:n8n/workflows/matching-v2.json'], capture_output=True, text=True, check=True).stdout)
node = lambda suf: next(n for n in wf['nodes'] if n['type'].endswith(suf))
PROMPT = node('chainLlm')['parameters']['text'].lstrip('=')
SCHEMA = json.loads(node('outputParserStructured')['parameters']['inputSchema'])

# planilla: donación por caso + necesidades por fila
plan = (ROOT / 'docs/qa/golden-set-v1-planilla.md').read_text()
final = {m[0]: int(m[1]) for m in re.findall(r'^\| ([A-F]\d) \|.*\*\*(\d)\*\* \|', (ROOT / 'docs/qa/golden-set-v1.md').read_text(), re.M)}
pairs = []
for caso in re.split(r'^## Caso ', plan, flags=re.M)[1:]:
    h = re.search(r'^\*\*(.+?)\*\* · (.+?) · cantidad (\d+) · estado: (.+)$\n\n> (.+)$', caso, re.M)
    don = dict(titulo=h[1], categoria=h[2], cantidad=int(h[3]), estado_objeto=h[4], descripcion=h[5])
    for r in re.findall(r'^\| ([A-F]\d) \| \*\*(.+?)\*\* · (.+?) · cant\. (\d+) — «(.+)» \|', caso, re.M):
        nec = dict(titulo=r[1], categoria=r[2], cantidad=int(r[3]), descripcion=r[4])
        pairs.append((r[0], nec, don))
assert len(pairs) == 31 and set(final) == {p[0] for p in pairs}, (len(pairs), len(final))

def vertex_token():  # JWT de la service account firmado con openssl, sin dependencias
    import base64, os, tempfile, urllib.parse
    k = json.load(open(os.path.expanduser('~/.config/vaiven/vertex-n8n.json')))
    b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b'=')
    now = int(time.time())
    seg = b64(b'{"alg":"RS256","typ":"JWT"}') + b'.' + b64(json.dumps({'iss': k['client_email'], 'scope': 'https://www.googleapis.com/auth/cloud-platform', 'aud': k['token_uri'], 'iat': now, 'exp': now + 3600}).encode())
    with tempfile.NamedTemporaryFile('w', delete=False) as f: f.write(k['private_key'])
    try: sig = subprocess.run(['openssl', 'dgst', '-sha256', '-sign', f.name], input=seg, capture_output=True, check=True).stdout
    finally: os.unlink(f.name)
    body = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': (seg + b'.' + b64(sig)).decode()}).encode()
    return k['project_id'], json.load(urllib.request.urlopen(k['token_uri'], body))['access_token']

def juzgar_vertex(model, text, extra):
    url = f'https://aiplatform.googleapis.com/v1/projects/{VERTEX[0]}/locations/global/publishers/google/models/{model}:generateContent'
    body = dict(contents=[dict(role='user', parts=[dict(text=text)])], generationConfig=dict(temperature=0, **extra))
    r = json.load(urllib.request.urlopen(urllib.request.Request(url, json.dumps(body).encode(), {'Authorization': f'Bearer {VERTEX[1]}', 'Content-Type': 'application/json'}), timeout=120))
    u = r['usageMetadata']
    return ''.join(p.get('text', '') for p in r['candidates'][0]['content']['parts'] if not p.get('thought')), \
        dict(entrada=u.get('promptTokenCount', 0), salida=u.get('candidatesTokenCount', 0), pensamiento=u.get('thoughtsTokenCount', 0)), r.get('modelVersion')

def juzgar(model, pid, nec, don, extra):
    text = PROMPT.replace('{{ JSON.stringify($json.necesidad) }}', json.dumps(nec, ensure_ascii=False)).replace('{{ JSON.stringify($json.donacion) }}', json.dumps(don, ensure_ascii=False))
    if MODO == 'parser':  # como el Structured Output Parser de n8n: instrucciones de formato en el prompt
        text += '\n\nYou must format your output as a JSON value that adheres to a given "JSON Schema" instance.\n\nHere is the JSON Schema instance your output must adhere to. Include the enclosing markdown codeblock:\n```json\n' + json.dumps(SCHEMA) + '\n```\n'
        rf = {}
    else:
        rf = dict(response_format=dict(type='json_schema', json_schema=dict(name='juicio', strict=True, schema=SCHEMA)))
    if model.startswith('vertex:'):
        t = time.time()
        try:
            c, uso, ver = juzgar_vertex(model[7:], text, extra)
            dt = time.time() - t
            out = json.loads(re.sub(r'^```(?:json)?|```$', '', c.strip()).strip())
            assert out['nivel'] in range(5) and {'narrativa', 'fortalezas', 'consideraciones'} <= set(out['justificacion'])
            return pid, out['nivel'], dt, uso, ver  # en Vertex el costo sale de la consola de facturación; acá van los tokens
        except Exception as e:
            return pid, None, time.time() - t, {}, repr(e)[:120]
    body = dict(model=model, temperature=0, messages=[dict(role='user', content=text)], usage=dict(include=True), **rf, **extra)
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', json.dumps(body).encode(), {'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    t = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=120))
        dt = time.time() - t
        c = r['choices'][0]['message']['content'] or ''
        out = json.loads(re.sub(r'^```(?:json)?|```$', '', c.strip()).strip())
        assert out['nivel'] in range(5) and {'narrativa', 'fortalezas', 'consideraciones'} <= set(out['justificacion'])
        return pid, out['nivel'], dt, r['usage'].get('cost', 0), r.get('provider')
    except Exception as e:
        return pid, None, time.time() - t, 0, repr(e)[:120]

model = sys.argv[1]
VERTEX = vertex_token() if model.startswith('vertex:') else None
extra = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
MODO = sys.argv[3] if len(sys.argv) > 3 else 'parser'
with cf.ThreadPoolExecutor(4) as ex:
    res = sorted(ex.map(lambda p: juzgar(model, *p, extra), pairs))
ok = [r for r in res if r[1] is not None]
lat = sorted(r[2] for r in ok)
exact = sum(r[1] == final[r[0]] for r in ok)
malo = sum((r[1] <= 1) == (final[r[0]] <= 1) for r in ok)
top1 = {}
for c in 'ABCDEF':
    rows = [r for r in ok if r[0][0] == c]
    gold = max(final[r[0]] for r in rows)
    best = max(r[1] for r in rows)
    top1[c] = final[[r for r in rows if r[1] == best][0][0]] == gold  # el primero con nivel máximo es un óptimo humano
print(json.dumps(dict(model=model, modo=MODO, extra=extra, validos=f'{len(ok)}/31', exacto=f'{exact}/{len(ok)}', linea_malo=f'{malo}/{len(ok)}',
    top1=f'{sum(top1.values())}/6', p50=round(statistics.median(lat), 2), p95=round(lat[int(.95 * (len(lat) - 1))], 2),
    costo_31=round(sum(r[3] for r in ok), 5) if not VERTEX else {k: sum(r[3][k] for r in ok) for k in ('entrada', 'salida', 'pensamiento')}, proveedores=sorted({str(r[4]) for r in res}),
    errores=[r for r in res if r[1] is None][:3], niveles={r[0]: r[1] for r in res}), ensure_ascii=False))
