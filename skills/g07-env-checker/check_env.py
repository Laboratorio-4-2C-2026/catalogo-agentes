"""Compara variables de entorno entre .env.example, .env y lo que lee el código (g07-env-checker).

Nunca imprime valores: solo nombres y si están vacíos.

Uso: python3 -I check_env.py --repo <raiz-del-repo> [--env .env] [--example .env.example] [--json salida.json]
"""
import argparse
import json
import re
import sys
from pathlib import Path

IGNORAR_DIRS = {"node_modules", ".git", "build", "bin", "dist", "target", ".gradle", "out", ".idea", ".vscode", ".next"}

PATRONES = [
    # Spring: ${VAR} o ${VAR:default} en application*.yml / .properties
    ("spring", ("application*.yml", "application*.yaml", "application*.properties"),
     re.compile(r"\$\{([A-Z][A-Z0-9_]*)(:[^}]*)?\}")),
    # Java/Kotlin
    ("java", ("*.java", "*.kt"), re.compile(r"System\.getenv\(\s*\"([A-Z][A-Z0-9_]*)\"")),
    # Vite
    ("vite", ("*.ts", "*.tsx", "*.js", "*.jsx", "*.mjs"), re.compile(r"import\.meta\.env\.([A-Z][A-Z0-9_]*)")),
    # Node
    ("node", ("*.ts", "*.tsx", "*.js", "*.jsx", "*.mjs", "*.cjs"), re.compile(r"process\.env\.([A-Z][A-Z0-9_]*)")),
    # docker compose: ${VAR}, ${VAR:-x}, ${VAR?err}
    ("compose", ("docker-compose*.yml", "docker-compose*.yaml", "compose*.yml", "compose*.yaml"),
     re.compile(r"\$\{([A-Z][A-Z0-9_]*)(:?[-?][^}]*)?\}")),
    # GitHub Actions: secrets.X / vars.X
    ("ci", ("*.yml", "*.yaml"), re.compile(r"\$\{\{\s*(?:secrets|vars)\.([A-Z][A-Z0-9_]*)\s*\}\}")),
]
VITE_INTERNAS = {"MODE", "DEV", "PROD", "SSR", "BASE_URL"}
NODE_INTERNAS = {"NODE_ENV"}
CI_AUTOMATICAS = {"GITHUB_TOKEN"}
COMPOSE_ENV_KEY = re.compile(r"^\s+(?:-\s*)?([A-Z][A-Z0-9_]*)\s*[:=]\s*(.*)$")
SECRETO = re.compile(r"SECRET|PASSWORD|PASS|TOKEN|KEY|PRIVATE|CREDENTIAL", re.I)


def definidas_en_compose(raiz):
    """Variables que docker-compose define con valor literal en environment: (no ${VAR})."""
    definidas = {}
    for f in archivos(raiz, ("docker-compose*.yml", "docker-compose*.yaml", "compose*.yml", "compose*.yaml")):
        dentro = False
        indent_env = 0
        for n, linea in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            sangria = len(linea) - len(linea.lstrip())
            if re.match(r"^\s+environment:\s*$", linea):
                dentro, indent_env = True, sangria
                continue
            if dentro and linea.strip() and sangria <= indent_env:
                dentro = False
            if dentro:
                m = COMPOSE_ENV_KEY.match(linea)
                if m and "${" not in m.group(2):
                    definidas[m.group(1)] = f"{f.relative_to(raiz)}:{n}"
    return definidas


def leer_env(ruta):
    vars_ = {}
    if not ruta.exists():
        return None
    for n, linea in enumerate(ruta.read_text(errors="ignore").splitlines(), 1):
        l = linea.strip()
        if not l or l.startswith("#"):
            continue
        l = re.sub(r"^export\s+", "", l)
        if "=" not in l:
            continue
        k, v = l.split("=", 1)
        v = v.strip().strip('"').strip("'")
        vars_[k.strip()] = dict(vacia=(v == "" or v.startswith("<") or v.lower() in {"changeme", "xxx", "todo"}),
                                linea=n)
    return vars_


def archivos(raiz, globs):
    for g in globs:
        for f in raiz.rglob(g):
            if not any(p in IGNORAR_DIRS for p in f.parts):
                yield f


def usos_en_codigo(raiz):
    usos = {}
    for origen, globs, rx in PATRONES:
        vistos = set()
        for f in archivos(raiz, globs):
            if f in vistos:
                continue
            vistos.add(f)
            if origen == "ci" and ".github" not in f.parts:
                continue
            txt = f.read_text(errors="ignore")
            for m in rx.finditer(txt):
                nombre = m.group(1)
                if origen == "vite" and nombre in VITE_INTERNAS:
                    continue
                if origen == "node" and nombre in NODE_INTERNAS:
                    continue
                default = bool(m.lastindex and m.lastindex >= 2 and m.group(2)
                               and (m.group(2).startswith(":") and not m.group(2).startswith(":?")
                                    or m.group(2).startswith(":-") or m.group(2).startswith("-")))
                linea = txt.count("\n", 0, m.start()) + 1
                u = usos.setdefault(nombre, dict(fuentes=[], con_default=True, origenes=set()))
                u["fuentes"].append(f"{f.relative_to(raiz)}:{linea}")
                u["origenes"].add(origen)
                u["con_default"] = u["con_default"] and default
    return usos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--env", default=".env")
    ap.add_argument("--example", default=".env.example")
    ap.add_argument("--json")
    a = ap.parse_args()
    raiz = Path(a.repo).resolve()
    ej = leer_env(raiz / a.example)
    loc = leer_env(raiz / a.env)
    if loc is None and (raiz / ".env.local").exists():
        a.env = ".env.local"
        loc = leer_env(raiz / a.env)
    usos = usos_en_codigo(raiz)
    compose = definidas_en_compose(raiz)
    # Subproyectos con su propio ejemplo (p. ej. frontend/.env.example): sus variables se chequean ahí.
    sub_ejemplos = {}
    for f in raiz.rglob(a.example):
        if f.parent != raiz and not any(p in IGNORAR_DIRS for p in f.parts):
            for var in (leer_env(f) or {}):
                sub_ejemplos[var] = str(f.relative_to(raiz))
    if ej is None:
        print(f"⚠️  No existe {a.example}")
        ej = {}
    if loc is None:
        print(f"⚠️  No existe {a.env} (solo se compara el ejemplo contra el código)")
    hallazgos = []

    def h(sev, tipo, var, detalle):
        hallazgos.append(dict(sev=sev, tipo=tipo, var=var, detalle=detalle))

    for var, u in sorted(usos.items()):
        if "ci" in u["origenes"] and u["origenes"] == {"ci"}:
            continue  # secretos del CI: se reportan aparte
        if var in compose:
            u["con_default"] = True  # docker-compose le da valor (vale para el stack levantado con compose)
        if var in sub_ejemplos and var not in ej:
            continue  # documentada en el .env.example de su subproyecto
        if var not in ej:
            sev = "🟡" if u["con_default"] else "🔴"
            extra = (f" (la define {compose[var]})" if var in compose
                     else " (tiene default)" if u["con_default"] else " (sin default)")
            h(sev, "falta en el ejemplo", var, "usada en " + ", ".join(u["fuentes"][:3]) + extra)
        if loc is not None and var not in loc and not u["con_default"]:
            h("🔴", "falta en tu .env", var, "usada sin default en " + ", ".join(u["fuentes"][:3]))
        elif loc is not None and var in loc and loc[var]["vacia"] and not u["con_default"]:
            h("🟠", "vacía en tu .env", var, f"{a.env}:{loc[var]['linea']}")
        if "vite" in u["origenes"] and not var.startswith("VITE_"):
            h("🔴", "no expuesta por Vite", var, "Vite solo expone variables VITE_*: " + u["fuentes"][0])
        if "vite" in u["origenes"] and SECRETO.search(var):
            h("🔴", "posible secreto en el front", var, "todo lo VITE_* termina en el bundle público: " + u["fuentes"][0])
    for var, d in sorted(ej.items()):
        if var not in usos:
            h("⚪", "en el ejemplo pero sin uso", var, f"{a.example}:{d['linea']}")
        if not d["vacia"] and SECRETO.search(var) and var not in sub_ejemplos:
            h("🟠", "el ejemplo trae un valor en una variable sensible", var,
              f"{a.example}:{d['linea']} (revisá que no sea un secreto real)")
    if loc is not None:
        for var, d in sorted(loc.items()):
            if var not in ej and var not in usos:
                h("⚪", "en tu .env pero sin uso", var, f"{a.env}:{d['linea']}")
    ci = sorted(v for v, u in usos.items() if "ci" in u["origenes"] and v not in CI_AUTOMATICAS)

    orden = {"🔴": 0, "🟠": 1, "🟡": 2, "⚪": 3}
    print(f"Variables usadas en el código: {len(usos)} · en {a.example}: {len(ej)} · en {a.env}: "
          f"{'—' if loc is None else len(loc)}\n")
    for x in sorted(hallazgos, key=lambda x: (orden[x["sev"]], x["var"])):
        print(f"{x['sev']} {x['var']:32} {x['tipo']:45} {x['detalle']}")
    if ci:
        print("\nSecretos/variables del CI (configurar en GitHub, no en .env): " + ", ".join(ci))
    if not hallazgos:
        print("✅ Sin diferencias")
    if a.json:
        Path(a.json).write_text(json.dumps(hallazgos, indent=2, ensure_ascii=False))
    return 1 if any(x["sev"] == "🔴" for x in hallazgos) else 0


if __name__ == "__main__":
    sys.exit(main())
