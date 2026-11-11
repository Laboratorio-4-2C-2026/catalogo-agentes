#!/usr/bin/env python3
# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
"""Puente de MCPs: .mcp.json (Claude Code) → opencode.json (OpenCode).

Los dos formatos son incompatibles, así que un symlink no sirve:

    Claude    {"type":"stdio", "command":"x", "args":["a"], "env":{...}}
    OpenCode  {"type":"local",  "command":["x","a"],         "environment":{...}}

`command` es string+args en uno y un único array en el otro; `env` vs
`environment`. Este script hace la traducción y **mergea** en la clave "mcp" de
opencode.json sin tocar el resto del archivo (otras herramientas escriben ahí:
graphify, por ejemplo, agrega "plugin").

Fuente canónica = .mcp.json. Se edita ahí y se corre este script.

Uso:
  python3 scripts/sync-mcp.py --check   # ¿opencode.json al día? (exit 1 si no)
  python3 scripts/sync-mcp.py --write   # traducir y mergear

Solo stdlib.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".mcp.json"
DST = ROOT / "opencode.json"
SCHEMA = "https://opencode.ai/config.json"


def translate(name: str, spec: dict) -> dict:
    """Un servidor MCP de formato Claude Code al de OpenCode."""
    kind = spec.get("type", "stdio")

    if kind in ("http", "sse"):
        out = {"type": "remote", "url": spec["url"], "enabled": True}
        if spec.get("headers"):
            out["headers"] = spec["headers"]
        return out

    if kind != "stdio":
        sys.exit(f"[sync-mcp] ERROR: tipo de MCP no soportado en '{name}': {kind!r}")

    if "command" not in spec:
        sys.exit(f"[sync-mcp] ERROR: el MCP '{name}' no declara 'command'.")

    out = {
        "type": "local",
        # OpenCode espera comando y argumentos en un único array.
        "command": [spec["command"], *spec.get("args", [])],
        "enabled": True,
    }
    if spec.get("env"):
        # OpenCode la llama 'environment'. Los ${VAR} quedan tal cual: el que
        # los expande es el shell del usuario, no este script — así los secretos
        # nunca aterrizan en un archivo versionado.
        out["environment"] = dict(spec["env"])
    return out


def build() -> dict:
    if not SRC.exists():
        sys.exit(f"[sync-mcp] ERROR: no existe {SRC.relative_to(ROOT)}")
    servers = json.loads(SRC.read_text(encoding="utf-8")).get("mcpServers", {})

    # Merge: preservamos todo lo que ya haya en opencode.json (graphify escribe
    # "plugin" ahí) y solo reemplazamos la clave "mcp".
    current = {}
    if DST.exists():
        try:
            current = json.loads(DST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"[sync-mcp] ERROR: {DST.name} no es JSON válido: {exc}")

    current.setdefault("$schema", SCHEMA)
    current["mcp"] = {n: translate(n, s) for n, s in sorted(servers.items())}
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    # opencode.json es un artefacto LOCAL (gitignoreado): puede contener rutas
    # de la máquina de cada autor. Si no existe, este autor no usa OpenCode y no
    # hay nada que verificar — no le bloqueamos el commit por eso. Con --write
    # sí se crea: pedirlo explícitamente es justamente decir que lo vas a usar.
    if args.check and not DST.exists():
        print(f"[sync-mcp] {DST.name} no existe (este clon no usa OpenCode). Nada que verificar.")
        return 0

    expected = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    actual = DST.read_text(encoding="utf-8") if DST.exists() else None

    if actual == expected:
        print(f"[sync-mcp] OK: {DST.name} al día ({len(build()['mcp'])} MCP).")
        return 0

    if args.check:
        print(f"[sync-mcp] {DST.name} DESINCRONIZADO de .mcp.json.")
        print("  Corré `python3 scripts/sync-mcp.py --write`.")
        return 1

    DST.write_text(expected, encoding="utf-8")
    print(f"[sync-mcp] {DST.name} regenerado: {', '.join(build()['mcp']) or '(ninguno)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
