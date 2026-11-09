#!/usr/bin/env python3
"""Convierte los documentos de la carpeta de conocimiento de Zest a texto buscable.

Uso:
    python3 build_index.py ~/zest-agentes/conocimiento

Lee .pptx, .docx, .pdf, .xlsx, .md y .txt (también en subcarpetas) y escribe:
    <carpeta>/_texto/<archivo>.md   texto de cada documento (por diapositiva, página u hoja)
    <carpeta>/_texto/INDICE.md      lista de documentos con fecha y primeras líneas

Solo reconvierte los archivos que cambiaron desde la última corrida.
Dependencias (una vez): python3 -m pip install --user python-pptx python-docx pypdf openpyxl
"""
import datetime as dt
import os
import sys

EXT = {".pptx", ".docx", ".pdf", ".xlsx", ".md", ".txt"}


def pptx_text(path):
    from pptx import Presentation
    out = []
    for n, slide in enumerate(Presentation(path).slides, 1):
        partes = [sh.text_frame.text.strip() for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
            partes.append("Notas: " + slide.notes_slide.notes_text_frame.text.strip())
        out.append(f"## Diapositiva {n}\n" + "\n".join(partes))
    return "\n\n".join(out)


def docx_text(path):
    import docx
    d = docx.Document(path)
    lineas = []
    for p in d.paragraphs:
        if not p.text.strip():
            continue
        estilo = (p.style.name or "").lower()
        prefijo = "## " if estilo.startswith("heading") or estilo.startswith("título") else ""
        lineas.append(prefijo + p.text.strip())
    for t in d.tables:
        for row in t.rows:
            lineas.append(" | ".join(c.text.strip() for c in row.cells))
    return "\n".join(lineas)


def pdf_text(path):
    from pypdf import PdfReader
    return "\n\n".join(f"## Página {n}\n{(pg.extract_text() or '').strip()}"
                       for n, pg in enumerate(PdfReader(path).pages, 1))


def xlsx_text(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        filas = []
        for row in ws.iter_rows(values_only=True):
            vals = ["" if v is None else str(v) for v in row]
            if any(vals):
                filas.append(" | ".join(vals))
        out.append(f"## Hoja {ws.title}\n" + "\n".join(filas[:500]))
    return "\n\n".join(out)


def plain_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


LECTORES = {".pptx": pptx_text, ".docx": docx_text, ".pdf": pdf_text, ".xlsx": xlsx_text,
            ".md": plain_text, ".txt": plain_text}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    base = os.path.expanduser(sys.argv[1])
    dest = os.path.join(base, "_texto")
    os.makedirs(dest, exist_ok=True)

    indice, errores = [], []
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext not in EXT or f.startswith(("~$", ".")):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, base)
            out = os.path.join(dest, rel.replace(os.sep, "__") + ".md")
            mtime = os.path.getmtime(src)
            try:
                if not os.path.exists(out) or os.path.getmtime(out) < mtime:
                    texto = LECTORES[ext](src)
                    with open(out, "w", encoding="utf-8") as fo:
                        fo.write(f"# {rel}\n\nFuente: {src}\n\n{texto}\n")
                with open(out, encoding="utf-8") as fi:
                    cuerpo = [l.strip() for l in fi.read().splitlines()[4:] if l.strip() and not l.startswith("## ")]
                fecha = dt.datetime.fromtimestamp(mtime).strftime("%d/%m/%y")
                indice.append(f"- **{rel}** ({fecha}) → `_texto/{os.path.basename(out)}`: {' '.join(cuerpo)[:160]}")
            except ImportError as e:
                errores.append(f"- {rel}: falta una librería ({e.name}). Instalar con pip y volver a correr.")
            except Exception as e:  # archivo dañado o protegido
                errores.append(f"- {rel}: no se pudo leer ({e.__class__.__name__}: {e})")

    with open(os.path.join(dest, "INDICE.md"), "w", encoding="utf-8") as fo:
        fo.write(f"# Índice de documentos de Zest\n\nActualizado: {dt.datetime.now():%d/%m/%y %H:%M}\n\n")
        fo.write("\n".join(indice) or "(Todavía no hay documentos en la carpeta.)")
        if errores:
            fo.write("\n\n## No se pudieron leer\n" + "\n".join(errores))
    print(f"{len(indice)} documentos indexados, {len(errores)} con problemas. Índice: {os.path.join(dest, 'INDICE.md')}")
    for e in errores:
        print(e)


if __name__ == "__main__":
    main()
