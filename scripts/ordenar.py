"""Ordena las piezas que un PR subió en cualquier lugar del repo.

Para cada skill, agente o comando que el PR agrega o modifica y que no está
donde corresponde (skills/gNN-nombre/SKILL.md, agentes/gNN-nombre/gNN-nombre.md,
comandos/gNN-nombre/gNN-nombre.md), el bot:
- decide el tipo (metadata.tipo; si no está, SKILL.md es skill, un .md con
  "tools" es agente y una ruta con "command"/"comando" es comando),
- decide el grupo (metadata.grupo; si no está, el grupo de quien abrió el PR),
- arma el nombre gNN-nombre (sin guiones bajos ni prefijos repetidos),
- mueve la pieza con sus archivos de apoyo y actualiza name, tipo y grupo.

No inventa fichas: si un archivo no tiene frontmatter, lo informa y no lo toca.
Uso: python scripts/ordenar.py --base origin/main [--autor-pr usuario]
"""
import argparse
import re
import subprocess

from common import RAIZ, TIPOS, cargar_yaml, escribir_ficha, leer_ficha, slug

CARPETA_DE_TIPO = {v: k for k, v in TIPOS.items()}
IGNORAR = re.compile(r"^(\.github/|scripts/|sitio/|prompts/|_base/|README\.md$|CONTRIBUTING\.md$)", re.I)


def git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def grupo_de(usuario):
    if not usuario:
        return None
    for clave, lista in cargar_yaml(RAIZ / "integrantes.yml").items():
        if any(str(p.get("github", "")).lower() == usuario.lower() for p in lista or []):
            return "00" if clave == "catedra" else clave.replace("grupo-", "")
    return None


def ubicacion_correcta(rel, tipo, nombre):
    carpeta = CARPETA_DE_TIPO[tipo]
    archivo = "SKILL.md" if tipo == "skill" else f"{nombre}.md"
    return rel in (f"{carpeta}/{nombre}/{archivo}", f"{carpeta}/{nombre}/metadata.yml")


def es_pieza(archivo):
    if archivo.name == "SKILL.md":
        return True
    if archivo.suffix != ".md":
        return False
    ficha, _ = leer_ficha(archivo, False)
    return bool(ficha and ficha.get("name"))


def carpeta_propia(origen, ruta):
    """True si la carpeta de origen es solo de esta pieza (se mueve entera, con sus archivos de apoyo)."""
    if origen == RAIZ or origen.parent == RAIZ and origen.name in TIPOS:
        return False
    if ruta.name == "SKILL.md":
        return True
    otras = [a for a in origen.rglob("*.md") if a != ruta and es_pieza(a)]
    return not otras


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--autor-pr")
    args = parser.parse_args()

    cambiados = [c for c in git("diff", "--name-only", "--diff-filter=AMR", f"{args.base}...HEAD").split()
                 if not IGNORAR.match(c)]
    candidatos = sorted({c for c in cambiados if c.lower().endswith((".md", "metadata.yml"))
                         and not c.lower().endswith(("ejemplo.md",))})
    grupo_pr = grupo_de(args.autor_pr)
    movidas, avisos = [], []

    for rel in candidatos:
        ruta = RAIZ / rel
        if not ruta.exists():
            continue
        es_yml = ruta.name == "metadata.yml"
        ficha, cuerpo = leer_ficha(ruta, es_yml)
        partes = rel.split("/")
        # Un .md suelto dentro de la carpeta de una pieza (por ejemplo, un archivo de apoyo) no es una pieza.
        if ficha is None or not ficha.get("name"):
            if ruta.name == "SKILL.md" or (partes[0] not in TIPOS and len(partes) <= 2):
                avisos.append(f"- `{rel}` no tiene ficha (frontmatter con `name` y `description`). "
                              "Preparalo con el Prompt 1 de `prompts/`.")
            continue
        meta = ficha.get("metadata") if isinstance(ficha.get("metadata"), dict) else {}

        tipo = meta.get("tipo")
        if tipo not in CARPETA_DE_TIPO:
            if ruta.name == "SKILL.md":
                tipo = "skill"
            elif re.search(r"command|comando", rel, re.I):
                tipo = "comando"
            elif "tools" in ficha or re.search(r"agent", rel, re.I):
                tipo = "agente"
            else:
                tipo = "skill" if partes[0] == "skills" else "agente"

        grupo = str(meta.get("grupo") or "")
        if not re.fullmatch(r"\d{2}", grupo):
            m = re.match(r"^g(\d{2})-", str(ficha.get("name")))
            grupo = m.group(1) if m else (grupo_pr or "")
        if not re.fullmatch(r"\d{2}", grupo):
            avisos.append(f"- `{rel}`: no se pudo saber el grupo. Completá `metadata.grupo` en la ficha.")
            continue

        base = slug(str(ficha["name"]).replace("_", "-"))
        base = re.sub(r"^(g\d{2}-)+", "", base) or slug(ruta.parent.name)
        nombre = f"g{grupo}-{base}"[:64].rstrip("-")
        if ubicacion_correcta(rel, tipo, nombre) and ficha.get("name") == nombre:
            continue

        carpeta_destino = RAIZ / CARPETA_DE_TIPO[tipo] / nombre
        principal = "metadata.yml" if es_yml else ("SKILL.md" if tipo == "skill" else f"{nombre}.md")
        destino = carpeta_destino / principal
        if destino.exists() and destino.resolve() != ruta.resolve():
            avisos.append(f"- `{rel}`: ya existe `{destino.relative_to(RAIZ).as_posix()}`. Cambiá el `name` de la pieza.")
            continue

        origen = ruta.parent
        carpeta_destino.mkdir(parents=True, exist_ok=True)
        if carpeta_propia(origen, ruta) and origen.resolve() != carpeta_destino.resolve():
            for archivo in sorted(p for p in origen.rglob("*") if p.is_file()):
                nuevo = destino if archivo == ruta else carpeta_destino / archivo.relative_to(origen)
                nuevo.parent.mkdir(parents=True, exist_ok=True)
                git("mv", archivo.relative_to(RAIZ).as_posix(), nuevo.relative_to(RAIZ).as_posix())
        elif ruta.resolve() != destino.resolve():
            git("mv", rel, destino.relative_to(RAIZ).as_posix())

        ficha["name"] = nombre
        meta.setdefault("tipo", tipo)
        meta["grupo"] = grupo
        ficha["metadata"] = meta
        escribir_ficha(destino, es_yml, ficha, cuerpo)
        git("add", destino.relative_to(RAIZ).as_posix())
        movidas.append(f"- `{rel}` → `{destino.relative_to(RAIZ).as_posix()}` ({tipo})")

    if movidas or avisos:
        print("### Ordenamiento de piezas\n")
    if movidas:
        print("Piezas movidas a su lugar (el cambio ya está en este PR):\n")
        print("\n".join(movidas) + "\n")
    if avisos:
        print("No se pudieron ordenar:\n")
        print("\n".join(avisos) + "\n")


if __name__ == "__main__":
    main()
