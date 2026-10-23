"""Controles automáticos de las fichas.

Uso: python scripts/validar.py [--base origin/main]
Escribe un informe en Markdown. Termina con error si alguna ficha no cumple.
"""
import argparse
import re
import subprocess
import sys

import yaml

from common import (CAMPOS_LISTA, CAMPOS_VALOR, RAIZ, archivo_ficha, cargar_yaml, clave_grupo,
                    como_lista, leer_ficha, piezas, slug, texto_ejemplo, FRONTMATTER)

NOMBRE = re.compile(r"^g(\d{2})-[a-z0-9]+(-[a-z0-9]+)*$")
OBLIGATORIOS = ["tipo", "area", "fase", "tecnologias", "herramientas", "requiere",
                "grupo", "autor", "responsables", "madurez"]


def git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def autor_en_base(base, ruta):
    """Lee el autor de la ficha tal como está en la rama base (None si la pieza es nueva)."""
    texto = git("show", f"{base}:{ruta.relative_to(RAIZ).as_posix()}")
    if texto is None:
        return None
    if ruta.suffix == ".yml":
        datos = yaml.safe_load(texto) or {}
    else:
        m = FRONTMATTER.match(texto)
        datos = yaml.safe_load(m.group(1)) if m else {}
    return ((datos or {}).get("metadata") or {}).get("autor")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="rama contra la que se compara, ej: origin/main")
    args = parser.parse_args()

    integrantes = cargar_yaml(RAIZ / "integrantes.yml")
    errores, nombres = [], {}

    for tipo, carpeta in piezas():
        nombre = carpeta.name
        def error(msg):
            errores.append(f"- `{carpeta.parent.name}/{nombre}`: {msg}")

        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            error("no tiene archivo principal (SKILL.md, metadata.yml o un .md con el mismo nombre).")
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        if ficha is None:
            error(f"`{ruta.name}` no empieza con un frontmatter entre líneas `---`.")
            continue

        m = NOMBRE.match(nombre)
        if not m or len(nombre) > 64:
            error("el nombre tiene que ser `gNN-nombre` (minúsculas, números y guiones, máximo 64 caracteres).")
        if ficha.get("name") != nombre:
            error(f"el campo `name` (`{ficha.get('name')}`) tiene que ser igual al nombre de la carpeta.")
        if nombre in nombres:
            error(f"ya existe otra pieza con este nombre en `{nombres[nombre]}`.")
        nombres[nombre] = carpeta.parent.name
        if not str(ficha.get("description") or "").strip():
            error("falta `description`.")

        meta = ficha.get("metadata")
        if not isinstance(meta, dict):
            error("falta el bloque `metadata`.")
            continue
        faltan = [c for c in OBLIGATORIOS if meta.get(c) in (None, "") or (c != "requiere" and meta.get(c) == [])]
        if faltan:
            error("faltan campos obligatorios: " + ", ".join(f"`{c}`" for c in faltan) + ".")
        if meta.get("tipo") and meta.get("tipo") != tipo:
            error(f"`tipo` dice `{meta.get('tipo')}` pero la pieza está en la carpeta de tipo `{tipo}`.")

        grupo = str(meta.get("grupo") or "")
        if not re.fullmatch(r"\d{2}", grupo):
            error("`grupo` tiene que ser un número de dos dígitos entre comillas, por ejemplo `\"03\"`.")
        elif m and m.group(1) != grupo:
            error(f"el prefijo `g{m.group(1)}` no coincide con `grupo: \"{grupo}\"`.")

        miembros = {str(p.get("github", "")).lower() for p in integrantes.get(clave_grupo(grupo), []) or []}
        autor = meta.get("autor")
        personas = [("autor", autor)] + [("colaborador", c) for c in como_lista(meta.get("colaboradores"))]
        if not re.fullmatch(r"\d{2}", grupo):
            personas = []
        for rol, persona in personas:
            if not persona:
                continue
            if not isinstance(persona, dict) or not persona.get("nombre") or not persona.get("github"):
                error(f"cada {rol} necesita `nombre` y `github`.")
            elif str(persona["github"]).lower() not in miembros:
                error(f"el {rol} `{persona['github']}` no figura en `integrantes.yml` como integrante de `{clave_grupo(grupo)}`. "
                      "Si es alguien nuevo, el bot lo suma solo cuando el usuario existe en GitHub: revisá cómo está escrito.")

        if args.base and isinstance(autor, dict):
            anterior = autor_en_base(args.base, ruta)
            if isinstance(anterior, dict) and anterior.get("github") != autor.get("github"):
                error(f"el autor no se puede cambiar (antes era `{anterior.get('github')}`). Sumá a la persona como colaborador.")

        for campo in CAMPOS_LISTA + CAMPOS_VALOR:
            for valor in como_lista(meta.get(campo)):
                if valor != slug(valor):
                    error(f"`{campo}` tiene `{valor}`: los valores van en minúsculas, sin acentos ni espacios.")

        if texto_ejemplo(carpeta, ruta, es_yml) is None:
            error("falta la sección `## Ejemplo de uso`" + (" (o el archivo EJEMPLO.md)." if es_yml else "."))

    print("### Controles automáticos\n")
    if errores:
        cosas = "cosa" if len(errores) == 1 else "cosas"
        print(f"Hay {len(errores)} {cosas} para corregir antes de aceptar el PR:\n")
        print("\n".join(errores) + "\n")
        sys.exit(1)
    cantidad = "pieza" if len(nombres) == 1 else "piezas"
    print(f"Todo en orden. Se revisaron {len(nombres)} {cantidad}.\n")


if __name__ == "__main__":
    main()
