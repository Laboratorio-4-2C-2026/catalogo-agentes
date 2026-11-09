#!/usr/bin/env python3
"""Convierte los agentes y skills del grupo 02 (Zest) de Multica al formato del Catálogo Común de Agentes.

Uso:
    python3 to_catalog.py export snapshot.json
        Baja de Multica los agentes del grupo con sus skills (contenido y archivos de apoyo).
        Nunca exporta configuración MCP, variables de entorno ni tokens.

    python3 to_catalog.py plantilla snapshot.json fichas.json [<copia-del-catalogo>] [--todas]
        Genera fichas.json con una entrada por pieza para completar (clasificación y ejemplo de uso).
        Con la copia del catálogo, marca incluir:false las piezas que ya están en origin/main o en ramas g02-* de
        PRs abiertos (no se duplican). Con --todas incluye todo (para actualizar piezas).
        Si un agente y una skill tendrían el mismo nombre, el agente lleva el sufijo -agent (el catálogo no
        permite repetir nombres entre agentes y skills).

    python3 to_catalog.py build snapshot.json fichas.json <copia-del-catalogo> [--actualizar]
        Escribe agentes/g02-*/g02-*.md y skills/g02-*/SKILL.md (con sus archivos) en la copia del catálogo.
        Sin --actualizar, no toca piezas que ya existen (las informa como "ya existe").
        Con --actualizar, reemplaza las instrucciones y conserva autor y colaboradores de la ficha existente.
        Imprime la tabla de resultados en Markdown.

Reglas del catálogo (CONTRIBUTING.md y prompts/1-preparar-piezas.md): las instrucciones no se modifican;
solo cambian el nombre, la ubicación, la ficha y se agrega "## Ejemplo de uso".
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

import yaml

GRUPO = "02"
PREFIJO = f"g{GRUPO}-"
FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)
SECRETO = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
                     r"\"private_key\"\s*:|xox[baprs]-[A-Za-z0-9-]{10,})")
CAMPOS_META = ["area", "fase", "tecnologias", "metodologia", "herramientas", "requiere", "madurez", "relacionados"]


# ---------- utilidades ----------

def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-")
    s = s[len(PREFIJO):] if s.startswith(PREFIJO) else s
    return (PREFIJO + s)[:64].rstrip("-")


def cli(*args):
    out = subprocess.run(["multica", *args, "--output", "json"], capture_output=True, text=True, check=True).stdout
    data = json.loads(out or "null")
    if isinstance(data, dict) and "id" not in data:
        for k in ("agents", "skills", "members", "data", "items"):
            if isinstance(data.get(k), list):
                return data[k]
        if isinstance(data.get("skill"), dict):
            return data["skill"]
    return data


def split_front(text):
    m = FRONT.match(text or "")
    if not m:
        return {}, text or ""
    try:
        return yaml.safe_load(m.group(1)) or {}, text[m.end():]
    except yaml.YAMLError:
        return {}, text[m.end():]


def dump_front(front, body):
    y = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
    return f"---\n{y}---\n{body.lstrip()}"


# ---------- export ----------

def export(path):
    members = cli("workspace", "member", "list") or []
    agents, skills = [], {}
    for a in cli("agent", "list") or []:
        full = cli("agent", "get", a["id"]) or a
        if full.get("archived_at") or full.get("status") == "archived":
            continue
        for k in ("mcp_config", "custom_env", "runtime_config", "custom_args", "conversation_starters"):
            full.pop(k, None)
        try:
            ligadas = cli("agent", "skills", "list", a["id"]) or []
        except subprocess.CalledProcessError:
            ligadas = full.get("skills") or []
        full["skills"] = [{"id": s.get("id"), "name": s.get("name")} for s in ligadas]
        for s in full["skills"]:
            if s["id"] and s["id"] not in skills:
                det = cli("skill", "get", s["id"], "--with-content") or {}
                skills[s["id"]] = {k: det.get(k) for k in ("id", "name", "description", "content", "created_by", "files")}
        agents.append({k: full.get(k) for k in ("id", "name", "description", "instructions", "owner_id", "skills", "model")})
    snap = {"members": members, "agents": agents, "skills": list(skills.values())}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    print(f"{len(agents)} agentes y {len(skills)} skills exportados a {path}")


# ---------- autores ----------

def integrantes(catalogo):
    with open(os.path.join(catalogo, "integrantes.yml"), encoding="utf-8") as f:
        return (yaml.safe_load(f) or {}).get(f"grupo-{GRUPO}") or []


def resolver_persona(user_id, members, grupo):
    """user_id de Multica -> {nombre, github} del grupo, o None si no se puede identificar."""
    m = next((x for x in members if (x.get("user_id") or (x.get("user") or {}).get("id") or x.get("id")) == user_id), None)
    if not m:
        return None
    user = m.get("user") if isinstance(m.get("user"), dict) else {}
    nombre = norm(m.get("name") or user.get("name"))
    email = norm(m.get("email") or user.get("email"))
    local = email.split("@")[0]
    for p in grupo:
        pn, gh = norm(p["nombre"]), norm(p["github"])
        partes = pn.split()
        if nombre == pn or (gh and (gh == local or gh in nombre.replace(" ", ""))):
            return p
        if partes and nombre and all(t in nombre for t in partes[:1]) and partes[-1][:5] in (nombre + local):
            return p
        if partes and partes[-1][:6] in local:
            return p
    return None


# ---------- plantilla ----------

def ya_publicadas(catalogo):
    """Nombres g02-* que ya están en origin/main o en ramas g02-* remotas (PRs abiertos)."""
    def git(*a):
        return subprocess.run(["git", "-C", catalogo, *a], capture_output=True, text=True).stdout
    git("fetch", "-q", "origin")
    refs = ["origin/main"] + git("for-each-ref", "--format=%(refname:short)", f"refs/remotes/origin/g{GRUPO}-*").split()
    nombres = set()
    for ref in refs:
        for carpeta in ("agentes", "skills"):
            for linea in git("ls-tree", "--name-only", ref, carpeta + "/").split():
                n = os.path.basename(linea)
                if n.startswith(PREFIJO):
                    nombres.add(n)
    return nombres


def plantilla(snap_path, out, catalogo=None, todas=False):
    snap = json.load(open(snap_path, encoding="utf-8"))
    vacio = {"name": "", "description": "", "area": [], "fase": [], "tecnologias": [], "metodologia": ["scrum"],
             "herramientas": ["claude-code"], "requiere": [], "madurez": "experimental", "relacionados": [],
             "colaboradores": [], "ejemplo": {"pedido": "", "resultado": ""}, "incluir": True}
    fichas = {"agentes": {}, "skills": {}}
    skill_slugs = {slug(s["name"]) for s in snap["skills"]}
    ya = ya_publicadas(catalogo) if catalogo and not todas else set()
    omitidas = []
    for a in snap["agents"]:
        n = slug(a["name"])
        if n in skill_slugs:  # agente y skill no pueden compartir nombre en el catálogo
            n = (n + "-agent")[:64].rstrip("-")
        fichas["agentes"][a["name"]] = {**vacio, "name": n, "incluir": n not in ya}
        if n in ya:
            omitidas.append(n)
    for s in snap["skills"]:
        n = slug(s["name"])
        fichas["skills"][s["name"]] = {**vacio, "name": n, "incluir": n not in ya}
        if n in ya:
            omitidas.append(n)
    if omitidas:
        print("Ya publicadas o en un PR abierto (incluir:false): " + ", ".join(omitidas))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(fichas, f, ensure_ascii=False, indent=2)
    print(f"Plantilla con {len(fichas['agentes'])} agentes y {len(fichas['skills'])} skills en {out}")


# ---------- build ----------

def metadata(tipo, ficha, autor, existente=None):
    meta = {"tipo": tipo}
    for c in CAMPOS_META:
        v = ficha.get(c)
        if c == "madurez":
            meta[c] = v or "experimental"
        elif v is not None:
            meta[c] = v if isinstance(v, list) else [v]
    meta["grupo"] = GRUPO
    if existente and existente.get("autor"):
        meta["autor"] = existente["autor"]
        colabs = list(existente.get("colaboradores") or [])
        for c in ficha.get("colaboradores") or []:
            if c.get("github") not in {x.get("github") for x in colabs}:
                colabs.append(c)
        if colabs:
            meta["colaboradores"] = colabs
        meta["responsables"] = existente.get("responsables") or [meta["autor"]["github"]]
    else:
        if autor:
            meta["autor"] = {"nombre": autor["nombre"], "github": autor["github"]}
            meta["responsables"] = [autor["github"]]
        if ficha.get("colaboradores"):
            meta["colaboradores"] = ficha["colaboradores"]
    orden = ["tipo", "area", "fase", "tecnologias", "metodologia", "herramientas", "requiere", "grupo",
             "autor", "colaboradores", "responsables", "madurez", "relacionados"]
    return {k: meta[k] for k in orden if k in meta}


def ejemplo(ficha):
    e = ficha.get("ejemplo") or {}
    if not (e.get("pedido") and e.get("resultado")):
        return None
    return f"\n\n## Ejemplo de uso\n**Pedido:** {e['pedido'].strip()}\n**Resultado:** {e['resultado'].strip()}\n"


def build(snap_path, fichas_path, catalogo, actualizar=False):
    snap = json.load(open(snap_path, encoding="utf-8"))
    fichas = json.load(open(fichas_path, encoding="utf-8"))
    grupo = integrantes(catalogo)
    members = snap.get("members") or []
    filas, avisos = [], []
    nuevos_nombres = {}  # nombre original de skill -> nombre del catálogo

    def check(nombre, ficha):
        faltan = [c for c in ("description", "area", "fase", "tecnologias") if not ficha.get(c)]
        if not ejemplo(ficha):
            faltan.append("ejemplo de uso")
        if not re.match(r"^g\d{2}-[a-z0-9]+(-[a-z0-9]+)*$", ficha.get("name", "")) or len(ficha["name"]) > 64:
            faltan.append("name válido")
        if faltan:
            avisos.append(f"- `{nombre}`: falta completar {', '.join(faltan)} en fichas.json (no se generó).")
            return False
        return True

    for s in snap["skills"]:
        f = fichas["skills"].get(s["name"])
        if f and f.get("incluir", True):
            nuevos_nombres[s["name"]] = f.get("name") or slug(s["name"])

    def escribir(tipo, nombre_original, ficha, cuerpo, autor_id, archivos=()):
        nombre = ficha["name"]
        carpeta = os.path.abspath(os.path.join(catalogo, "skills" if tipo == "skill" else "agentes", nombre))
        principal = os.path.join(carpeta, "SKILL.md" if tipo == "skill" else f"{nombre}.md")
        existente = None
        if os.path.exists(principal):
            if not actualizar:
                filas.append([nombre, tipo, "—", "—", "ya existe (no se tocó; usar --actualizar)"])
                return
            existente = (split_front(open(principal, encoding="utf-8").read())[0].get("metadata") or {})
        autor = resolver_persona(autor_id, members, grupo)
        front = {"name": nombre, "description": ficha["description"].strip()}
        if tipo == "agente":
            sk = [nuevos_nombres[x] for x in ficha.get("_skills", []) if x in nuevos_nombres]
            if sk:
                front["skills"] = sk
        front["metadata"] = metadata(tipo, ficha, autor, existente)
        texto = dump_front(front, cuerpo.rstrip() + ejemplo(ficha))
        todo = texto + "".join(c for _, c in archivos)
        if SECRETO.search(todo):
            avisos.append(f"- `{nombre}`: parece contener una clave o token. No se generó: revisalo a mano.")
            return
        os.makedirs(carpeta, exist_ok=True)
        with open(principal, "w", encoding="utf-8") as fo:
            fo.write(texto)
        for rel, contenido in archivos:
            destino = os.path.normpath(os.path.join(carpeta, rel))
            if os.path.basename(rel) == "SKILL.md":
                continue
            if not destino.startswith(carpeta + os.sep):
                avisos.append(f"- `{nombre}`: el archivo `{rel}` apunta fuera de la carpeta de la pieza y no se copió.")
                continue
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(destino, "w", encoding="utf-8") as fo:
                fo.write(contenido)
        faltan_arch = [rel for rel, _ in archivos if os.path.basename(rel) != "SKILL.md"
                       and not os.path.exists(os.path.join(carpeta, rel))]
        if faltan_arch:
            avisos.append(f"- `{nombre}`: no se escribieron los archivos de apoyo {faltan_arch}. No subir así.")
        dudas = []
        if not (existente or autor):
            dudas.append("falta autor")
        if ficha.get("madurez", "experimental") == "experimental":
            dudas.append("madurez sin confirmar")
        dudas.append("ejemplo generado")
        if tipo == "agente":
            viejos = [x for x in ficha.get("_skills", []) if x in nuevos_nombres and x in cuerpo]
            if viejos:
                dudas.append("referencia a revisar: " + ", ".join(viejos))
        m = front["metadata"]
        filas.append([nombre, tipo, (m.get("autor") or {}).get("nombre", "—"),
                      ", ".join(c["nombre"] for c in m.get("colaboradores", [])) or "—", "; ".join(dudas)])

    for s in snap["skills"]:
        f = fichas["skills"].get(s["name"])
        if not f or not f.get("incluir", True) or not check(s["name"], f):
            continue
        _, cuerpo = split_front(s.get("content") or "")
        archivos = [(x["path"], x.get("content") or "") for x in (s.get("files") or []) if x.get("path")]
        escribir("skill", s["name"], f, cuerpo, s.get("created_by"), archivos)

    for a in snap["agents"]:
        f = fichas["agentes"].get(a["name"])
        if not f or not f.get("incluir", True) or not check(a["name"], f):
            continue
        f = {**f, "_skills": [s["name"] for s in a.get("skills") or [] if s.get("name")]}
        cuerpo = f"# {a['name']}\n\n{(a.get('instructions') or '').strip()}\n"
        escribir("agente", a["name"], f, cuerpo, a.get("owner_id"))

    print("| nombre | tipo | autor | colaboradores | dudas |\n|---|---|---|---|---|")
    for fila in filas:
        print("| " + " | ".join(fila) + " |")
    por_autor = {}
    for fila in filas:
        por_autor[fila[2]] = por_autor.get(fila[2], 0) + 1
    print("\n**Piezas por autor:** " + ", ".join(f"{k}: {v}" for k, v in por_autor.items()))
    if avisos:
        print("\n**Para revisar:**\n" + "\n".join(avisos))


def main():
    a = sys.argv[1:]
    if a[:1] == ["export"] and len(a) >= 2:
        export(a[1])
    elif a[:1] == ["plantilla"] and len(a) >= 3:
        pos = [x for x in a[3:] if not x.startswith("--")]
        plantilla(a[1], a[2], os.path.expanduser(pos[0]) if pos else None, "--todas" in a)
    elif a[:1] == ["build"] and len(a) >= 4:
        build(a[1], a[2], os.path.abspath(os.path.expanduser(a[3])), "--actualizar" in a)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
