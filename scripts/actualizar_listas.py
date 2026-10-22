"""Suma a taxonomia.yml los valores nuevos que ya están en uso y actualiza las
listas de categorías del README.md y del CONTRIBUTING.md.

Corre solo, después de aceptar un PR.
"""
import re
from collections import Counter

from common import (CAMPOS_LISTA, CAMPOS_VALOR, RAIZ, archivo_ficha, cargar_yaml, como_lista,
                    guardar_yaml, leer_ficha, piezas)

ENCABEZADO = ("# Valores comunes de las fichas del catálogo.\n"
              "# Lo actualiza solo el workflow al aceptar un PR: no hace falta editarlo a mano.\n"
              "# 'alias' convierte variantes conocidas en el valor oficial (ej: reactjs -> react).\n\n")
MARCAS = re.compile(r"(<!-- LISTAS:INICIO -->)(.*?)(<!-- LISTAS:FIN -->)", re.S)


def main():
    taxonomia = cargar_yaml(RAIZ / "taxonomia.yml")
    valores = taxonomia.setdefault("valores", {})
    taxonomia.setdefault("alias", {})
    uso = {campo: Counter() for campo in CAMPOS_LISTA + CAMPOS_VALOR}

    for _, carpeta in piezas():
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        meta = (ficha or {}).get("metadata") or {}
        for campo in uso:
            for valor in como_lista(meta.get(campo)):
                uso[campo][valor] += 1

    agregados = 0
    for campo, contador in uso.items():
        lista = valores.get(campo) or {}
        for valor in sorted(contador):
            if valor not in lista:
                lista[valor] = ""
                agregados += 1
        valores[campo] = lista
    guardar_yaml(RAIZ / "taxonomia.yml", taxonomia, ENCABEZADO)

    filas = ["| Campo | Valores (cantidad de piezas que lo usan) |", "|---|---|"]
    for campo in CAMPOS_LISTA + CAMPOS_VALOR:
        items = [f"`{v}` ({uso[campo][v]})" for v in (valores.get(campo) or {})]
        filas.append(f"| `{campo}` | {', '.join(items) or '—'} |")
    tabla = "\n" + "\n".join(filas) + "\n"

    for nombre in ("README.md", "CONTRIBUTING.md"):
        ruta = RAIZ / nombre
        if ruta.exists():
            texto = ruta.read_text(encoding="utf-8")
            ruta.write_text(MARCAS.sub(lambda m: m.group(1) + tabla + m.group(3), texto), encoding="utf-8")

    print(f"Listas actualizadas. Valores nuevos agregados: {agregados}.")


if __name__ == "__main__":
    main()
