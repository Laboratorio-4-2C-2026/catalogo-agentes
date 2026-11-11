#!/usr/bin/env python3
"""Anota un diff unificado con el número de línea real de la versión nueva.

Usado por el agente 8.1 (code-reviewer-de-prs) para anclar comentarios de
revisión de GitHub a una línea exacta, sin contarla a ojo (regla del repo:
determinista antes que probabilístico para cálculos exactos).

Uso:
  gh pr diff <numero> --repo vaiven-austral/vaiven-app | python3 scripts/diff-line-map.py

Formato de salida, por archivo:
  === archivo: <path> ===
  [+123] línea agregada       -> existe en la versión nueva, línea 123
  [ 123] línea de contexto    -> existe en la versión nueva, línea 123
  [-old] línea eliminada      -> no existe en la versión nueva, no es un destino válido

Para un comentario de review de GitHub, usar el N de una línea "[+N]" o
"[ N]" como "line", y "RIGHT" como "side". Una línea "[-old]" nunca es un
destino válido para un comentario nuevo (no existe en el archivo resultante).
"""
import re
import sys

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")
FILE_RE = re.compile(r"^\+\+\+ b/(.+)$")


def main() -> None:
    new_line = None
    for raw in sys.stdin:
        line = raw.rstrip("\n")

        if line.startswith("diff --git"):
            new_line = None
            continue

        m_file = FILE_RE.match(line)
        if m_file:
            print(f"\n=== archivo: {m_file.group(1)} ===")
            continue

        if line.startswith("--- "):
            continue

        if line.startswith("\\ No newline at end of file"):
            continue

        m_hunk = HUNK_RE.match(line)
        if m_hunk:
            new_line = int(m_hunk.group(1))
            continue

        if new_line is None:
            continue

        if line.startswith("+") and not line.startswith("+++"):
            print(f"[+{new_line}] {line[1:]}")
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            print(f"[-old] {line[1:]}")
        else:
            content = line[1:] if line.startswith(" ") else line
            print(f"[ {new_line}] {content}")
            new_line += 1


if __name__ == "__main__":
    main()
