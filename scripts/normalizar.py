"""Unifica cómo están escritos los valores de las fichas.

Corrige los archivos en el lugar (Front-End -> frontend, ReactJS -> react) y
escribe por pantalla un informe en Markdown para el comentario del PR.
"""
from common import (CAMPOS_LISTA, CAMPOS_VALOR, RAIZ, archivo_ficha, cargar_yaml,
                    como_lista, escribir_ficha, leer_ficha, piezas, slug)


def main():
    taxonomia = cargar_yaml(RAIZ / "taxonomia.yml")
    valores = taxonomia.get("valores", {})
    alias = taxonomia.get("alias", {})
    corregidos, nuevos = [], []

    for _, carpeta in piezas():
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, cuerpo = leer_ficha(ruta, es_yml)
        meta = (ficha or {}).get("metadata")
        if not isinstance(meta, dict):
            continue
        cambio = False
        for campo in CAMPOS_LISTA + CAMPOS_VALOR:
            if meta.get(campo) is None:
                continue
            resultado = []
            for original in como_lista(meta[campo]):
                valor = slug(original)
                valor = (alias.get(campo) or {}).get(valor, valor)
                if valor != original:
                    corregidos.append(f"- `{carpeta.name}` · {campo}: `{original}` → `{valor}`")
                if valor not in (valores.get(campo) or {}):
                    nuevos.append(f"- `{carpeta.name}` · {campo}: `{valor}`")
                if valor and valor not in resultado:
                    resultado.append(valor)
            final = resultado[0] if campo in CAMPOS_VALOR and resultado else resultado
            if final != meta[campo]:
                meta[campo] = final
                cambio = True
        if cambio:
            escribir_ficha(ruta, es_yml, ficha, cuerpo)

    print("### Normalización de valores\n")
    if corregidos:
        print("Corregido automáticamente en este PR:\n")
        print("\n".join(corregidos) + "\n")
    else:
        print("No hubo nada que corregir.\n")
    if nuevos:
        print("Valores nuevos (se suman a las listas cuando se acepte el PR):\n")
        print("\n".join(sorted(set(nuevos))) + "\n")


if __name__ == "__main__":
    main()
