"""Genera panel.html con el avance de cada estudiante hacia las 10 skills.

Lo corre la cátedra en su computadora: python scripts/generar_panel.py
El archivo no se sube al repo (está en .gitignore).
"""
import html
from collections import Counter

from common import RAIZ, archivo_ficha, cargar_yaml, como_lista, leer_ficha, piezas

META = 10


def main():
    integrantes = cargar_yaml(RAIZ / "integrantes.yml")
    como_autor, colaboraciones = Counter(), Counter()
    for _, carpeta in piezas():
        if carpeta.name.startswith("g00-"):
            continue
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        meta = (ficha or {}).get("metadata") or {}
        autor = meta.get("autor")
        if isinstance(autor, dict):
            como_autor[autor.get("github")] += 1
        for c in como_lista(meta.get("colaboradores")):
            if isinstance(c, dict):
                colaboraciones[c.get("github")] += 1

    bloques = []
    for grupo, lista in integrantes.items():
        if grupo == "catedra":
            continue
        filas, completos = [], 0
        for p in lista or []:
            n = como_autor[p["github"]]
            completos += n >= META
            estado = "Completo" if n >= META else f"Faltan {META - n}"
            filas.append(
                f"<tr><td>{html.escape(p['nombre'])}</td><td><code>{html.escape(p['github'])}</code></td>"
                f"<td class=n>{n}</td><td><div class=bar><span style='width:{min(100, n * 10)}%'></span></div></td>"
                f"<td class=n>{colaboraciones[p['github']]}</td><td class={'ok' if n >= META else 'no'}>{estado}</td></tr>")
        total = sum(como_autor[p["github"]] for p in lista or [])
        bloques.append(f"<h2>{html.escape(grupo)} · {total} piezas · {completos} de {len(lista or [])} estudiantes completos</h2>"
                       "<table><tr><th>Estudiante</th><th>GitHub</th><th>Como autor</th><th>Avance</th>"
                       "<th>Colaboraciones</th><th>Estado</th></tr>" + "".join(filas) + "</table>")

    pagina = ("<!doctype html><html lang=es><meta charset=utf-8><title>Panel de seguimiento</title><style>"
              "body{font:15px/1.5 system-ui,sans-serif;max-width:1000px;margin:24px auto;padding:0 16px}"
              "table{border-collapse:collapse;width:100%;margin-bottom:24px}td,th{border-bottom:1px solid #ddd;padding:6px 8px;text-align:left}"
              ".n{text-align:right}.bar{width:120px;height:8px;background:#eee;border-radius:4px;overflow:hidden}"
              ".bar span{display:block;height:100%;background:#2e55c8}.ok{color:#1f7a4d;font-weight:600}.no{color:#8a5a00;font-weight:600}"
              "</style><h1>Panel de seguimiento de la cátedra</h1>" + "".join(bloques) + "</html>")
    (RAIZ / "panel.html").write_text(pagina, encoding="utf-8")
    print("Panel generado: panel.html")


if __name__ == "__main__":
    main()
