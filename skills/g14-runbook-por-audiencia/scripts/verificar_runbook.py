#!/usr/bin/env python3
"""verificar_runbook.py — audita las vistas de un runbook contra sus hechos.

Comprueba, sin interpretar la prosa:

  1. Cobertura: todo hecho etiquetado para una audiencia aparece citado ([H#])
     en la vista de esa audiencia.
  2. Fuga: una vista no cita hechos que no están etiquetados para ella.
  3. Fuente: cada paso o viñeta cita algo — un hecho [H#], [ticket], [ADR-NNNN],
     [commit <sha>] o [bitácora <archivo>] — y esa fuente existe.
  4. Existencia: cada ruta de archivo entre backticks existe en el commit de la
     feature (o en los repos hermanos); cada nombre de variable, secreto o
     credencial entre backticks figura en los hechos.
  5. Secretos: ningún patrón de clave, token o JWT.
  6. Forma: la vista de dirección no lleva bloques de código.

Uso:
  python3 verificar_runbook.py --hechos hechos.json --repo ~/Projects/vaiven/vaiven-app \\
      --raiz ~/Projects/vaiven --vistas devops.md devs.md direccion.md
Las vistas se reconocen por el nombre del archivo (devops / devs / direccion).
Sale con 1 si hay errores.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

AUDIENCIAS = ("devops", "devs", "direccion")
REF = re.compile(r"\[(H\d+|ticket|ADR-\d{4}|commit [0-9a-f]{7,}|bitácora [\w.-]+)\]")
HECHO = re.compile(r"\[(H\d+)\]")
TOKEN = re.compile(r"`([^`\n]+)`")
EXT = r"(?:py|sh|mjs|js|jsx|ts|tsx|md|json|ya?ml|toml|sql|html|css|env|example)"
RUTA = re.compile(r"^(?:[A-Za-z0-9_.@-]+/)+[A-Za-z0-9_.@-]*$|^[A-Za-z0-9_.-]+\." + EXT + r"$")
NOMBRE_SECRETO = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+$|^[a-z]+_[a-z_]+$")
SECRETOS = [re.compile(p) for p in (
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"\bAKIA[0-9A-Z]{16}\b", r"\bgh[pousr]_[A-Za-z0-9]{36,}",
    r"\bgithub_pat_[A-Za-z0-9_]{50,}", r"\bxox[baprs]-[A-Za-z0-9-]{10,}", r"\bAIza[0-9A-Za-z_-]{35}\b",
    r"\bATATT[A-Za-z0-9_=-]{30,}", r"\bsk-(?:or-v1-|ant-)?[A-Za-z0-9_-]{32,}", r"\bsb_secret_[A-Za-z0-9_-]{20,}",
    r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")]


def git_existe(repo, rev, ruta):
    return subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{rev}:{ruta.rstrip('/')}"], capture_output=True).returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hechos", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--raiz", help="carpeta con los repos hermanos (para rutas de docs y bitácora)")
    ap.add_argument("--vistas", nargs="+", required=True)
    ap.add_argument("--salida")
    a = ap.parse_args()

    d = json.loads(Path(a.hechos).read_text("utf-8"))
    hechos = {h["id"]: h for h in d["hechos"]}
    nombres_conocidos = set()
    for h in d["hechos"]:
        det = h["detalle"]
        if det.get("nombre"):
            nombres_conocidos.add(det["nombre"])
        for o in det.get("objetos", []):  # nombres de funciones, triggers, políticas… de una migración
            nombres_conocidos |= {t.split(".")[-1] for t in re.findall(r"[\w.]+", o)}
        for o in det.get("secretos_vault", []):
            nombres_conocidos.add(o)
        for c in det.get("credenciales", []):
            nombres_conocidos.add(c)
            nombres_conocidos.add(c.split(": ", 1)[-1])
        nombres_conocidos |= {w["path"] for w in det.get("webhooks", []) if w.get("path")}
        nombres_conocidos |= set(det.get("nuevas", {})) | set(det.get("actualizadas", {}))
    shas = {c["sha"] for c in d["commits"]}
    raiz = Path(a.raiz) if a.raiz else None
    repo = Path(a.repo)
    errores, avisos = [], []

    for ruta_vista in a.vistas:
        p = Path(ruta_vista)
        aud = next((x for x in AUDIENCIAS if x in p.stem.lower()), None)
        if not aud:
            errores.append(f"{p.name}: no sé a qué audiencia corresponde (el nombre debe contener devops, devs o direccion)")
            continue
        texto = p.read_text("utf-8")
        err = lambda m: errores.append(f"[{aud}] {m}")

        citados = set(HECHO.findall(texto))
        for hid in sorted(citados, key=lambda x: int(x[1:])):
            if hid not in hechos:
                err(f"cita {hid}, que no existe en hechos.json")
            elif aud not in hechos[hid]["audiencias"]:
                err(f"cita {hid} («{hechos[hid]['titulo'][:50]}»), que no está etiquetado para esta audiencia (fuga)")
        for hid, h in hechos.items():
            if aud in h["audiencias"] and hid not in citados:
                err(f"falta cubrir {hid} «{h['titulo'][:60]}»")

        en_codigo = False
        for n, linea in enumerate(texto.splitlines(), 1):
            if linea.strip().startswith("```"):
                en_codigo = not en_codigo
                if aud == "direccion" and en_codigo:
                    err(f"línea {n}: la vista de dirección no lleva bloques de código")
                continue
            if en_codigo:
                continue
            if re.match(r"^\s*(?:[-*]|\d+\.)\s+\S", linea):
                refs = REF.findall(linea)
                if not refs:
                    err(f"línea {n}: afirmación sin fuente: «{linea.strip()[:70]}»")
                for r in refs:
                    if r.startswith("commit ") and r.split()[1][:7] not in {s[:7] for s in shas}:
                        err(f"línea {n}: [{r}] no es un commit de esta feature")
                    if r.startswith("bitácora ") and raiz:
                        nombre = r.split(" ", 1)[1]
                        if not list(raiz.glob(f"*/docs/bitacora/{nombre}*")):
                            err(f"línea {n}: la entrada de bitácora «{nombre}» no existe")
                    if r.startswith("ADR-") and raiz and not list(raiz.glob(f"*/docs/architecture/adr/{r[4:]}-*.md")):
                        err(f"línea {n}: {r} no existe")
            for tok in TOKEN.findall(linea):
                if " " in tok or any(c in tok for c in "<>*{}$=()"):
                    continue
                if RUTA.match(tok):
                    ok = git_existe(repo, d["destino_completo"], tok) or (raiz and (raiz / tok).exists()) \
                        or (raiz and any((r / tok).exists() for r in raiz.iterdir() if r.is_dir()))
                    if not ok:
                        err(f"línea {n}: la ruta `{tok}` no existe en el commit {d['destino']} ni en los repos hermanos")
                elif NOMBRE_SECRETO.match(tok) and tok not in nombres_conocidos:
                    err(f"línea {n}: `{tok}` parece una variable o secreto y no figura en los hechos")
        for rx in SECRETOS:
            if rx.search(texto):
                err(f"contiene un patrón de secreto ({rx.pattern[:30]}…)")

    res = [f"Runbook {d['ticket']} · {d['repo']}@{d['destino']} · {len(d['hechos'])} hechos · vistas: "
           + ", ".join(Path(v).name for v in a.vistas)]
    res += [f"  ✗ {e}" for e in errores] or ["  ✓ cobertura, fuentes, existencia, secretos y forma: sin errores"]
    out = "\n".join(res)
    print(out)
    if a.salida:
        Path(a.salida).write_text(out + "\n", "utf-8")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
