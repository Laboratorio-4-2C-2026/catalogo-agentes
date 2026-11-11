#!/usr/bin/env python3
"""vigencia_adrs.py — ¿qué ADRs siguen siendo ciertos contra el repositorio?

Capa determinista de la auditoría de vigencia. Por cada ADR comprueba lo que
se puede comprobar sin interpretar la prosa:

  * estado declarado (propuesto / aceptado / reemplazado, total o en parte) y
    si una ratificación prometida venció sin que el ADR cambiara de estado;
  * coherencia de reemplazos: si A dice «reemplazado por X», X debería decir
    que reemplaza a A; y quién sigue citando como vigente a un ADR reemplazado;
  * enlaces relativos rotos;
  * rutas del repo citadas entre backticks que ya no existen;
  * variables de entorno citadas entre backticks sin rastro en código o config
    (se busca fuera de los .md, para que el propio ADR no se cuente a sí mismo);
  * marcadores abiertos: [por-verificar], [pendiente], [ratifica …].

Lo que NO hace: decidir si la decisión sigue siendo buena, ni si una frase en
prosa contradice al código. Para eso deja, por cada ADR «a revisar», las frases
exactas con la referencia que falló, para que la skill (una persona o un
modelo) las contraste.

Uso:
  python3 vigencia_adrs.py --adrs ~/Projects/vaiven/vaiven-direccion/docs/architecture/adr \\
                           --raiz ~/Projects/vaiven [--salida informe.md] [--json datos.json]
"""
import argparse
import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

HOY = date.today()
ANIO = HOY.year
EXT = r"(?:py|sh|mjs|js|jsx|ts|tsx|md|json|ya?ml|toml|sql|html|css|env)"
RUTA = re.compile(r"`((?:[A-Za-z0-9_.-]+/)+(?:[A-Za-z0-9_.-]+\." + EXT + r")?)`")
ENVVAR = re.compile(r"`([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)`")
ENLACE = re.compile(r"\]\(([^)\s]+)\)")
MARCADOR = re.compile(r"`?\[(por-verificar|pendiente|ratifica[^\]]*|verificar|TODO)[^\]]*\]`?", re.I)
FECHA = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\b")
ADR_REF = re.compile(r"(?:ADR-|adr/)?\b(00\d{2})\b(?:-[a-z0-9-]+\.md)?")
PLACEHOLDER = re.compile(r"[<>*{}~$]|\.\.\.|\bXXX\b")


def listar_repos(raiz):
    return sorted(p for p in Path(raiz).iterdir() if (p / ".git").exists())


def existe_en_raiz(cita, raiz, repos):
    c = cita.rstrip("/")
    if (raiz / c).exists():
        return True
    return any((r / c).exists() for r in repos)


def git_grep(repos, token):
    for r in repos:
        p = subprocess.run(["git", "-C", str(r), "grep", "-q", "-w", "-F", token, "--", ".", ":!*.md"], capture_output=True)
        if p.returncode == 0:
            return True
    return False


def encabezado(lineas):
    """Líneas de metadatos del ADR: hasta el primer '---' o '## ' tras el título."""
    out = []
    for l in lineas[1:]:
        if l.startswith("## ") or l.strip() == "---":
            break
        out.append(l)
    return out


def estado_de(head):
    txt, tomar = "", False
    for i, l in enumerate(head):
        if l.startswith("**Estado:**"):
            txt = l[len("**Estado:**"):].strip()
            j = i + 1
            while not txt and j < len(head) and j < i + 4:  # "**Estado:**" solo en su línea
                txt = head[j].strip()
                j += 1
            break
    return txt


def clasificar_estado(head, estado):
    h = "\n".join(head)
    reemplazado = re.search(r"\*\*Reemplazad[oa]([^*]*)\*\*", h)
    if reemplazado:
        return "reemplazado-en-parte" if "en parte" in reemplazado.group(1) else "reemplazado"
    if re.search(r"(?i)\bpropuest[oa]s?\b|\ba (definir|ratificar)\b", estado):
        return "propuesto"
    if re.search(r"(?i)\b(aceptad[oa]s?|decidid[oa]s?|ratificad[oa]s?)\b", estado):
        return "aceptado"
    return "sin-estado"


def fechas_en(texto):
    out = []
    for d, m, y in FECHA.findall(texto):
        try:
            out.append(date(int(y) if y else ANIO, int(m), int(d)))
        except ValueError:
            pass
    return out


def auditar(adr_dir, raiz):
    raiz = Path(raiz)
    repos = listar_repos(raiz)
    adrs = {}
    for f in sorted(Path(adr_dir).glob("[0-9][0-9][0-9][0-9]-*.md")):
        t = f.read_text("utf-8", "replace")
        lineas = t.splitlines()
        head = encabezado(lineas)
        estado = estado_de(head)
        a = {"id": f.name[:4], "archivo": f.name, "titulo": lineas[0].lstrip("# ").strip(),
             "estado_texto": estado[:160], "estado": clasificar_estado(head, estado), "hallazgos": [], "para_contrastar": [],
             "_texto": t, "_head": head, "_f": f}
        adrs[a["id"]] = a

    # reemplazos declarados en el encabezado
    reemplaza, reemplazado_por = {}, {}
    for a in adrs.values():
        h = "\n".join(a["_head"])
        for m in re.finditer(r"\*\*(Reemplaza|Reemplazad[oa][^*]*)\*\*:?([^\n]*(?:\n(?!\*\*)[^\n]*)?)", h):
            refs = {r for r in ADR_REF.findall(m.group(2)) if r in adrs and r != a["id"]}
            destino = reemplaza if m.group(1) == "Reemplaza" else reemplazado_por
            destino.setdefault(a["id"], set()).update(refs)

    for a in adrs.values():
        H = a["hallazgos"]
        t, f = a["_texto"], a["_f"]
        # ratificación vencida
        if a["estado"] == "propuesto":
            fs = fechas_en(a["estado_texto"])
            if fs and max(fs) < HOY:
                H.append({"tipo": "ratificacion-vencida", "detalle": f"Sigue «propuesto»; la última fecha del estado era {max(fs).isoformat()} ({(HOY - max(fs)).days} días).",
                          "cita": a["estado_texto"]})
            elif not fs:
                H.append({"tipo": "sin-estado-final", "detalle": "Sigue «propuesto» sin fecha de ratificación.", "cita": a["estado_texto"]})
        # reemplazos
        for destino in reemplazado_por.get(a["id"], ()):
            if a["id"] not in reemplaza.get(destino, ()):
                H.append({"tipo": "reemplazo-sin-reciproco", "detalle": f"Dice que lo reemplaza ADR-{destino}, pero ADR-{destino} no declara que reemplaza a ADR-{a['id']}.", "cita": ""})
        # citas a ADRs reemplazados
        for otro in {r for r in ADR_REF.findall(t.split("## ", 1)[-1]) if r in adrs and r != a["id"]}:
            if adrs[otro]["estado"] == "reemplazado" and otro not in reemplaza.get(a["id"], ()) and not re.search(r"(?i)reemplaz", t):
                H.append({"tipo": "cita-adr-reemplazado", "detalle": f"Cita ADR-{otro}, que figura reemplazado, sin mencionar el reemplazo.", "cita": ""})
        # enlaces
        for l in sorted(set(ENLACE.findall(t))):
            if l.startswith(("http", "#", "mailto:")) or not re.search(r"[./]", l):
                continue
            if not (f.parent / l.split("#")[0]).resolve().exists():
                H.append({"tipo": "enlace-roto", "detalle": f"Enlace relativo inexistente: {l}", "cita": l})
        # rutas y variables entre backticks
        cuerpo = t.split("\n", 1)[1]
        for linea in cuerpo.splitlines():
            sin_externos = re.sub(r"\[[^\]]*\]\(http[^)]*\)", "", linea)  # el texto de un enlace a otro sitio no es una ruta nuestra
            for ruta in RUTA.findall(sin_externos):
                if PLACEHOLDER.search(ruta) or ruta.startswith(("http", "/", "./", "../")) or ruta.rstrip("/").count("/") == 0:
                    continue
                if not existe_en_raiz(ruta, raiz, repos) and not any((b / ruta.rstrip("/")).exists() for b in f.resolve().parents):
                    H.append({"tipo": "ruta-ausente", "detalle": f"`{ruta}` no existe en ningún repo.", "cita": linea.strip()[:240]})
            for v in ENVVAR.findall(linea):
                if not git_grep(repos, v):
                    H.append({"tipo": "variable-sin-rastro", "detalle": f"`{v}` no aparece en código ni config (fuera de .md).", "cita": linea.strip()[:240]})
        # marcadores abiertos
        for m in MARCADOR.finditer(t):
            H.append({"tipo": "marcador-abierto", "detalle": m.group(0).strip("`")[:120], "cita": ""})
        # dedupe
        vistos, unicos = set(), []
        for h in H:
            k = (h["tipo"], h["detalle"])
            if k not in vistos:
                vistos.add(k)
                unicos.append(h)
        a["hallazgos"] = unicos
        duros = [h for h in unicos if h["tipo"] in ("ruta-ausente", "variable-sin-rastro", "enlace-roto", "cita-adr-reemplazado", "reemplazo-sin-reciproco")]
        if a["estado"].startswith("reemplazado"):
            a["veredicto"] = a["estado"]
        elif duros:
            a["veredicto"] = "a-revisar"
            a["para_contrastar"] = sorted({h["cita"] for h in duros if h["cita"]})[:6]
        elif a["estado"] == "propuesto":
            a["veredicto"] = "vigente-sin-ratificar"
        else:
            a["veredicto"] = "vigente"
    return list(adrs.values())


def informe(adrs, fecha):
    cuenta = {}
    for a in adrs:
        cuenta[a["veredicto"]] = cuenta.get(a["veredicto"], 0) + 1
    L = [f"# Vigencia de ADRs — {fecha}", "", f"ADRs auditados: **{len(adrs)}**.", "", "| Veredicto | ADRs |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(cuenta.items(), key=lambda x: -x[1])]
    L += ["", "`vigente-sin-ratificar`: no se encontró nada roto, pero el ADR sigue «propuesto». "
          "`a-revisar`: una referencia verificable falló; la frase exacta está abajo para que alguien la contraste.", "",
          "| ADR | Título | Estado declarado | Veredicto | Hallazgos |", "|---|---|---|---|---|"]
    for a in adrs:
        L.append(f"| {a['id']} | {a['titulo'][:60].replace('|', '/')} | {a['estado']} | **{a['veredicto']}** | {len(a['hallazgos'])} |")
    for a in adrs:
        if not a["hallazgos"]:
            continue
        L += ["", f"### ADR-{a['id']} — {a['veredicto']}", f"Estado escrito: «{a['estado_texto']}»", ""]
        for h in a["hallazgos"]:
            L.append(f"- **{h['tipo']}** — {h['detalle']}")
            if h["cita"] and h["tipo"] in ("ruta-ausente", "variable-sin-rastro"):
                L.append(f"  - Frase: «{h['cita']}»")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adrs", required=True)
    ap.add_argument("--raiz", required=True, help="carpeta que contiene los repos (para resolver rutas y buscar variables)")
    ap.add_argument("--salida")
    ap.add_argument("--json")
    a = ap.parse_args()
    adrs = auditar(a.adrs, a.raiz)
    txt = informe(adrs, datetime.now().strftime("%Y-%m-%d"))
    print(txt)
    if a.salida:
        Path(a.salida).write_text(txt, "utf-8")
    if a.json:
        limpio = [{k: v for k, v in x.items() if not k.startswith("_")} for x in adrs]
        Path(a.json).write_text(json.dumps(limpio, indent=2, ensure_ascii=False), "utf-8")


if __name__ == "__main__":
    main()
