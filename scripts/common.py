"""Funciones compartidas por los scripts del catálogo."""
import os
import re
import unicodedata
from pathlib import Path

import yaml

# Raíz del repo a revisar. En los workflows los scripts se toman de main y se
# apuntan a la rama del PR con CATALOGO_RAIZ.
RAIZ = Path(os.environ.get("CATALOGO_RAIZ") or Path(__file__).resolve().parent.parent).resolve()
TIPOS = {"skills": "skill", "agentes": "agente", "comandos": "comando"}
CAMPOS_LISTA = ["area", "fase", "tecnologias", "metodologia", "herramientas", "requiere"]
CAMPOS_VALOR = ["madurez"]
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)
EJEMPLO = re.compile(r"^##\s+Ejemplo de uso\s*$", re.M | re.I)


def slug(valor):
    """'Front-End' -> 'front-end', 'Diseño' -> 'diseno', 'Nest.js' -> 'nest-js'."""
    v = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode()
    v = re.sub(r"[\s_./]+", "-", v.lower().strip())
    v = re.sub(r"[^a-z0-9-]", "", v)
    return re.sub(r"-+", "-", v).strip("-")


def cargar_yaml(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        return {}
    return yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}


class _Dumper(yaml.SafeDumper):
    """Escribe entre comillas los textos que parecen números (ej: grupo "08"), para que ningún parser los lea como enteros."""


_Dumper.add_representer(str, lambda d, v: d.represent_scalar(
    "tag:yaml.org,2002:str", v, style='"' if re.fullmatch(r"[0-9]+", v) else None))


def volcar_yaml(datos):
    return yaml.dump(datos, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=1000)


def guardar_yaml(ruta, datos, encabezado=""):
    texto = volcar_yaml(datos)
    Path(ruta).write_text(encabezado + texto, encoding="utf-8")


def piezas():
    """Recorre todas las carpetas de piezas: devuelve (tipo, carpeta)."""
    for dir_tipo, tipo in TIPOS.items():
        base = RAIZ / dir_tipo
        if not base.is_dir():
            continue
        for carpeta in sorted(p for p in base.iterdir() if p.is_dir()):
            yield tipo, carpeta


def archivo_ficha(carpeta):
    """Devuelve (archivo que tiene la ficha, es_metadata_yml) o (None, False)."""
    if (carpeta / "SKILL.md").exists():
        return carpeta / "SKILL.md", False
    if (carpeta / "metadata.yml").exists():
        return carpeta / "metadata.yml", True
    md = carpeta / f"{carpeta.name}.md"
    if md.exists():
        return md, False
    return None, False


def leer_ficha(ruta, es_yml):
    """Devuelve (ficha, cuerpo). ficha es None si el archivo no tiene frontmatter."""
    texto = ruta.read_text(encoding="utf-8")
    if es_yml:
        return (yaml.safe_load(texto) or {}), None
    m = FRONTMATTER.match(texto)
    if not m:
        return None, texto
    return (yaml.safe_load(m.group(1)) or {}), texto[m.end():]


def escribir_ficha(ruta, es_yml, ficha, cuerpo):
    dump = volcar_yaml(ficha)
    ruta.write_text(dump if es_yml else f"---\n{dump}---\n{cuerpo}", encoding="utf-8")


def texto_ejemplo(carpeta, ruta, es_yml):
    """Devuelve el texto de la sección 'Ejemplo de uso', o None si no existe."""
    if es_yml:
        archivo = carpeta / "EJEMPLO.md"
        return archivo.read_text(encoding="utf-8").strip() if archivo.exists() else None
    texto = ruta.read_text(encoding="utf-8")
    m = EJEMPLO.search(texto)
    if not m:
        return None
    resto = texto[m.end():]
    fin = re.search(r"^##\s", resto, re.M)
    return (resto[: fin.start()] if fin else resto).strip()


def clave_grupo(grupo):
    return "catedra" if str(grupo) == "00" else f"grupo-{grupo}"


def como_lista(valor):
    if valor is None:
        return []
    return valor if isinstance(valor, list) else [valor]
