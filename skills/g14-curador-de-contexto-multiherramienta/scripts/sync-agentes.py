#!/usr/bin/env python3
# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
"""Sincronizador de espejos del entorno de agentes de ECHO.

Fuente canónica: CLAUDE.md + .claude/skills/ + .claude/agents/
Espejos generados: Cursor (.cursor/rules/), Antigravity (.agents/) y
OpenCode (AGENTS.md + .opencode/agents/ + .opencode/commands/).

Nota sobre OpenCode: sus skills NO se espejan — lee `.claude/skills/` de forma
nativa (verificado con `opencode agent list`, v1.18.18). Solo necesita los
subagentes y los slash commands.

Las adaptaciones por proveedor (p. ej. "subagente" → "regla de dominio") se
declaran en sync-agentes.json como reemplazos de texto EXACTO: si la fuente
cambia y un reemplazo deja de matchear, el script falla ruidosamente en vez de
generar un espejo silenciosamente desincronizado.

Uso:
  python3 scripts/sync-agentes.py --check   # ¿espejos al día? (exit 1 si no)
  python3 scripts/sync-agentes.py --write   # regenerar los espejos

Solo stdlib. El pre-commit de scripts/githooks/ corre --check.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "sync-agentes.json"

BANNER = (
    "<!-- ARCHIVO GENERADO desde {src} por scripts/sync-agentes.py — "
    "editá la fuente y corré `python3 scripts/sync-agentes.py --write`. -->"
)


def strip_frontmatter(text: str):
    """Devuelve (frontmatter_con_delimitadores, cuerpo)."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 5], text[end + 5 :]
    return "", text


def source_description(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        if line.startswith("description:"):
            return line[len("description:") :].strip()
    return ""


def render_frontmatter(spec, src_fm: str) -> str:
    lines = ["---"]
    for key, value in spec.items():
        if value == "$description":
            value = source_description(src_fm)
        elif value == "$description_yaml":
            # Las descripciones de los subagentes contienen ": " (p. ej. "…ni
            # DSP: eso es territorio humano"), que en YAML plano es un error de
            # parseo. OpenCode sí valida el YAML, así que este token emite un
            # escalar entrecomillado. $description se conserva sin tocar para
            # no alterar los espejos ya generados de Cursor.
            value = '"' + source_description(src_fm).replace('"', '\\"') + '"'
        if isinstance(value, bool):
            value = "true" if value else "false"
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render(source_rel: str, out_cfg: dict) -> str:
    src_text = (ROOT / source_rel).read_text(encoding="utf-8")
    src_fm, body = strip_frontmatter(src_text)
    body = body.lstrip("\n")

    for rep in out_cfg.get("replacements", []):
        if rep["from"] not in body:
            sys.exit(
                f"[sync-agentes] ERROR: un reemplazo declarado para "
                f"{out_cfg['path']} ya no matchea la fuente {source_rel}.\n"
                f"  Texto buscado (inicio): {rep['from'][:100]!r}\n"
                f"  Actualizá scripts/sync-agentes.json junto con la fuente."
            )
        body = body.replace(rep["from"], rep["to"])

    parts = []
    fm_spec = out_cfg.get("frontmatter")
    if fm_spec == "source":
        parts.append(src_fm.rstrip("\n"))
    elif isinstance(fm_spec, dict):
        parts.append(render_frontmatter(fm_spec, src_fm))
    parts.append(BANNER.format(src=source_rel))
    if out_cfg.get("prepend"):
        parts.append(out_cfg["prepend"].rstrip("\n"))
    # "body": false → el espejo NO copia el cuerpo de la fuente (caso de los
    # slash commands de OpenCode: son stubs que delegan en la skill, no copias
    # del protocolo). Los reemplazos se siguen validando contra la fuente, así
    # que el archivo igual se rompe ruidosamente si la fuente deriva.
    if out_cfg.get("body", True):
        parts.append(body.rstrip("\n") + "\n")
    else:
        parts[-1] = parts[-1].rstrip("\n") + "\n"
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="verificar paridad")
    mode.add_argument("--write", action="store_true", help="regenerar espejos")
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    stale, written = [], []

    for pair in config["pairs"]:
        source_rel = pair["source"]
        if not (ROOT / source_rel).exists():
            sys.exit(f"[sync-agentes] ERROR: fuente inexistente: {source_rel}")
        for out_cfg in pair["outputs"]:
            expected = render(source_rel, out_cfg)
            out_path = ROOT / out_cfg["path"]
            current = (
                out_path.read_text(encoding="utf-8") if out_path.exists() else None
            )
            if current == expected:
                continue
            if args.write:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(expected, encoding="utf-8")
                written.append(out_cfg["path"])
            else:
                stale.append(out_cfg["path"])

    if args.check:
        if stale:
            print("[sync-agentes] Espejos DESINCRONIZADOS respecto de la fuente canónica:")
            for path in stale:
                print(f"  - {path}")
            print(
                "\nCorré `python3 scripts/sync-agentes.py --write`, revisá el diff "
                "y volvé a stagear. (Los espejos no se editan a mano: editá la "
                "fuente en CLAUDE.md / .claude/ o los reemplazos en "
                "scripts/sync-agentes.json.)"
            )
            return 1
        print("[sync-agentes] OK: todos los espejos están sincronizados.")
        return 0

    if written:
        print("[sync-agentes] Espejos regenerados:")
        for path in written:
            print(f"  - {path}")
    else:
        print("[sync-agentes] Nada que regenerar: espejos ya sincronizados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
