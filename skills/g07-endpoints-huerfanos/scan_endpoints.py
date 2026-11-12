"""Inventario heurístico de endpoints Spring vs llamadas del frontend (g07-endpoints-huerfanos).

Uso:
  python3 -I scan_endpoints.py --back <dir-backend> --front <dir-frontend> [--base-front /api] [--json salida.json]

Es una primera pasada: la skill verifica a mano cada hallazgo antes de reportarlo.
"""
import argparse
import json
import re
import sys
from pathlib import Path

VERBOS = {"GetMapping": "GET", "PostMapping": "POST", "PutMapping": "PUT",
          "PatchMapping": "PATCH", "DeleteMapping": "DELETE"}
ANOT = re.compile(r"@(RequestMapping|GetMapping|PostMapping|PutMapping|PatchMapping|DeleteMapping)\s*(\((.*?)\))?",
                  re.S)
CLASE = re.compile(r"\b(class|interface)\s+(\w+)")
STR = re.compile(r'"([^"]*)"')
METODO_RM = re.compile(r"RequestMethod\.(\w+)")

# Llamadas del front: fetch(`...`), axios.get('...'), api.post("..."), http.delete(`...`)
LLAMADA = re.compile(
    r"""(?:\b(fetch)\s*\(\s*|\b\w+\.(get|post|put|patch|delete)\s*"""
    r"""(?:<(?:[^<>]|<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>)*>)?\s*\(\s*)(`[^`]*`|'[^']*'|"[^"]*")""",
    re.I)
METODO_FETCH = re.compile(r"""method\s*:\s*['"`](\w+)['"`]""", re.I)


def normalizar(path):
    path = re.sub(r"\$\{[^}]*\}", "{}", path)      # ${id}
    path = re.sub(r"\{[^}/]*\}", "{}", path)        # {id}
    path = re.sub(r":\w+", "{}", path)               # :id
    path = path.split("?")[0]
    path = re.sub(r"^https?://[^/]+", "", path)
    path = re.sub(r"^\{\}", "", path)                # ${API_URL}/x -> /x
    path = "/" + path.strip("/")
    return re.sub(r"/+", "/", path)


def backend(raiz):
    eps = []
    for f in list(raiz.rglob("*.java")) + list(raiz.rglob("*.kt")):
        if "/test/" in f.as_posix():
            continue
        txt = f.read_text(errors="ignore")
        if "Controller" not in txt:
            continue
        m_clase = CLASE.search(txt)
        base = ""
        if m_clase:
            antes = txt[: m_clase.start()]
            for m in ANOT.finditer(antes):
                if m.group(1) == "RequestMapping":
                    s = STR.findall(m.group(3) or "")
                    base = s[0] if s else ""
        cuerpo_ini = m_clase.end() if m_clase else 0
        for m in ANOT.finditer(txt, cuerpo_ini):
            args = m.group(3) or ""
            rutas = STR.findall(args) or [""]
            if m.group(1) == "RequestMapping":
                ms = METODO_RM.findall(args) or ["ANY"]
            else:
                ms = [VERBOS[m.group(1)]]
            linea = txt.count("\n", 0, m.start()) + 1
            for r in rutas:
                for verbo in ms:
                    eps.append(dict(metodo=verbo.upper(), ruta=normalizar(base + "/" + r),
                                    fuente=f"{f.relative_to(raiz)}:{linea}"))
    return eps


HELPER = re.compile(r"""(?:const|let)\s+(\w+)\s*=\s*\([^)]*\)\s*(?::\s*\w+\s*)?=>\s*(`[^`]*`|'[^']*'|"[^"]*")""")
HELPER_FN = re.compile(r"""function\s+(\w+)\s*\([^)]*\)[^{]*\{\s*return\s+(`[^`]*`|'[^']*'|"[^"]*")""")
CONST = re.compile(r"""(?:const|let)\s+(\w+)\s*(?::\s*string\s*)?=\s*(`[^`]*`|'[^']*'|"[^"]*")""")
LITERAL_RUTA = re.compile(r"""(`/(?:api|v\d+)/[^`]*`|'/(?:api|v\d+)/[^']*'|"/(?:api|v\d+)/[^"]*")""")


def _resolver(cruda, helpers):
    """Expande ${helper(...)} y ${CONSTANTE} al principio de la ruta, si se conocen."""
    for _ in range(3):
        m = re.match(r"\$\{(\w+)(\([^}]*\))?\}", cruda)
        if not m or m.group(1) not in helpers:
            break
        cruda = helpers[m.group(1)] + cruda[m.end():]
    return cruda


def frontend(raiz):
    llamadas = []
    archivos_front = []
    helpers = {}
    for ext in ("*.ts", "*.tsx", "*.js", "*.jsx"):
        for f in raiz.rglob(ext):
            p = f.as_posix()
            if "node_modules" in p or "/dist/" in p or ".test." in p or ".spec." in p:
                continue
            archivos_front.append(f)
            txt = f.read_text(errors="ignore")
            for rx in (HELPER, HELPER_FN, CONST):
                for m in rx.finditer(txt):
                    valor = m.group(2)[1:-1]
                    if valor.startswith("/") or valor.startswith("${"):
                        helpers.setdefault(m.group(1), valor)
    referencias = []  # rutas literales usadas de forma indirecta (parámetros, constantes): método desconocido
    for f in archivos_front:
        txt = f.read_text(errors="ignore")
        for m in LITERAL_RUTA.finditer(txt):
            linea = txt.count("\n", 0, m.start()) + 1
            referencias.append(dict(metodo="ANY", ruta=normalizar(m.group(1)[1:-1]),
                                    fuente=f"{f.relative_to(raiz)}:{linea}"))
    for f in archivos_front:
        if True:
            txt = f.read_text(errors="ignore")
            for m in LLAMADA.finditer(txt):
                cruda = _resolver(m.group(3)[1:-1], helpers)
                if "/" not in cruda:
                    continue
                if m.group(1):
                    ventana = txt[m.end(): m.end() + 300]
                    mm = METODO_FETCH.search(ventana.split(")")[0] if ")" in ventana else ventana)
                    verbo = mm.group(1).upper() if mm else "GET"
                else:
                    verbo = m.group(2).upper()
                linea = txt.count("\n", 0, m.start()) + 1
                llamadas.append(dict(metodo=verbo, ruta=normalizar(cruda), cruda=m.group(3)[1:-1],
                                     fuente=f"{f.relative_to(raiz)}:{linea}"))
    return llamadas, referencias


def coincide(ep, ll, base_front):
    if ep["metodo"] not in (ll["metodo"], "ANY") and ll["metodo"] != "ANY":
        return False
    a, b = ep["ruta"], ll["ruta"]
    if a == b or a == normalizar(base_front + b):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--back", required=True)
    ap.add_argument("--front", required=True)
    ap.add_argument("--base-front", default="", help="prefijo que agrega el cliente HTTP (ej: /api)")
    ap.add_argument("--json")
    a = ap.parse_args()
    eps = backend(Path(a.back))
    lls, refs = frontend(Path(a.front))
    sin_llamada = [e for e in eps if not any(coincide(e, l, a.base_front) for l in lls)]
    indirectos = [e for e in sin_llamada if any(coincide(e, r, a.base_front) for r in refs)]
    huerfanos = [e for e in sin_llamada if e not in indirectos]
    sin_back = [l for l in lls if not any(coincide(e, l, a.base_front) for e in eps)]
    usados = len(eps) - len(sin_llamada)
    print(f"Endpoints backend: {len(eps)} · usados por el front: {usados} · usados de forma indirecta: "
          f"{len(indirectos)} · sin uso: {len(huerfanos)}")
    print(f"Llamadas frontend: {len(lls)} · sin endpoint: {len(sin_back)}\n")
    print("## Endpoints sin uso en el front")
    for e in sorted(huerfanos, key=lambda x: x["ruta"]):
        print(f"- {e['metodo']:6} {e['ruta']:45} {e['fuente']}")
    print("\n## Endpoints usados de forma indirecta (ruta en una constante o parámetro: verificar el método)")
    for e in sorted(indirectos, key=lambda x: x["ruta"]):
        print(f"- {e['metodo']:6} {e['ruta']:45} {e['fuente']}")
    print("\n## Llamadas del front sin endpoint")
    for l in sorted(sin_back, key=lambda x: x["ruta"]):
        print(f"- {l['metodo']:6} {l['ruta']:45} {l['fuente']}   (literal: {l['cruda']})")
    if a.json:
        Path(a.json).write_text(json.dumps(dict(endpoints=eps, llamadas=lls, indirectos=indirectos, huerfanos=huerfanos,
                                                sin_back=sin_back), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
