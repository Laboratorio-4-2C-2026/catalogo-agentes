"""Suma a integrantes.yml los autores y colaboradores de las fichas que todavía no figuran.

Para cada persona (autor o colaborador) de cada ficha:
- Si ya figura en algún grupo de integrantes.yml, no hace nada.
- Si no figura en ningún grupo, la agrega al grupo de la pieza (grupo-NN, o
  catedra para g00) con su nombre y usuario de GitHub, siempre que ese usuario
  exista en GitHub (se consulta con la CLI gh si está disponible).

Corre en cada PR antes de los controles, y el bot guarda el cambio en la rama
del PR. Escribe un informe en Markdown.
"""
import re
import subprocess


from common import RAIZ, archivo_ficha, cargar_yaml, clave_grupo, como_lista, leer_ficha, piezas, volcar_yaml

ENCABEZADO = ("# Integrantes de cada grupo: nombre y usuario de GitHub.\n"
              "# De acá salen el control de autores y la vista de avance por alumno.\n"
              "# La clave es \"grupo-NN\" (dos dígitos). El material de la cátedra usa \"catedra\" (prefijo g00).\n"
              "# Los autores y colaboradores nuevos los suma solo el bot al revisar cada PR.\n\n")


def existe_en_github(usuario):
    """True si el usuario existe; None si no se pudo consultar (sin gh o sin red)."""
    try:
        r = subprocess.run(["gh", "api", f"users/{usuario}"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode == 0:
        return True
    return False if "Not Found" in (r.stdout + r.stderr) else None


def main():
    ruta = RAIZ / "integrantes.yml"
    integrantes = cargar_yaml(ruta)
    conocidos = {str(p.get("github", "")).lower() for lista in integrantes.values() for p in (lista or [])}
    agregados, rechazados = [], []

    for _, carpeta in piezas():
        archivo, es_yml = archivo_ficha(carpeta)
        if not archivo:
            continue
        ficha, _ = leer_ficha(archivo, es_yml)
        meta = (ficha or {}).get("metadata") or {}
        grupo = str(meta.get("grupo") or "")
        if not re.fullmatch(r"\d{2}", grupo):
            continue
        for persona in [meta.get("autor")] + como_lista(meta.get("colaboradores")):
            if not isinstance(persona, dict) or not persona.get("github") or not persona.get("nombre"):
                continue
            usuario = str(persona["github"]).strip().lstrip("@")
            if usuario.lower() in conocidos:
                continue
            existe = existe_en_github(usuario)
            if existe is False:
                rechazados.append(f"- `{usuario}` (en `{carpeta.name}`): ese usuario no existe en GitHub. Revisá cómo está escrito.")
                continue
            clave = clave_grupo(grupo)
            integrantes.setdefault(clave, [])
            if integrantes[clave] is None:
                integrantes[clave] = []
            integrantes[clave].append({"nombre": str(persona["nombre"]).strip(), "github": usuario})
            conocidos.add(usuario.lower())
            agregados.append(f"- **{persona['nombre']}** (`{usuario}`) en `{clave}`, por `{carpeta.name}`.")

    if agregados:
        orden = sorted(integrantes, key=lambda k: (k != "catedra", k))
        texto = volcar_yaml({k: integrantes[k] for k in orden})
        ruta.write_text(ENCABEZADO + re.sub(r"\n(?=grupo-|catedra)", "\n\n", texto), encoding="utf-8", newline="\n")

    if agregados or rechazados:
        print("### Integrantes\n")
    if agregados:
        print("Se sumaron a `integrantes.yml` (el cambio ya está en este PR):\n")
        print("\n".join(agregados) + "\n")
    if rechazados:
        print("No se sumaron:\n")
        print("\n".join(rechazados) + "\n")


if __name__ == "__main__":
    main()
