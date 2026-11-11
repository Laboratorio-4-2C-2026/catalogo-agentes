#!/usr/bin/env python3
"""e2e-preflight.py — Precondiciones del Tester E2E local (9.2).

Verifica que la máquina tenga lo necesario para levantar vaiven-app completo en
local (frontend + Supabase en Docker + n8n) y, por cada faltante, imprime el
paso exacto para resolverlo. No instala ni modifica nada.

Uso:
  python scripts/e2e-preflight.py                       # Chequea todo y guía
  python scripts/e2e-preflight.py --app C:\\ruta\\vaiven-app  # Ruta del clon a probar
  python scripts/e2e-preflight.py --check               # Sale 0 si no falta nada bloqueante, 1 si falta algo
"""

import argparse
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_DEFAULT = ROOT.parent / "vaiven-app"

# Puertos que el stack ocupa: Supabase API/DB/Studio, n8n y Vite.
PUERTOS = {
    54321: "Supabase API (supabase start)",
    54322: "Supabase Postgres",
    54323: "Supabase Studio",
    5678: "n8n",
    5173: "Vite (pnpm dev)",
}

OK, FALTA, AVISO = "OK   ", "FALTA", "AVISO"


def correr(cmd: list, timeout: int = 20) -> tuple:
    """Corre un comando y devuelve (código, salida). Código -1 si no se pudo ejecutar."""
    exe = shutil.which(cmd[0])
    if not exe:
        return -1, ""
    try:
        r = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (subprocess.TimeoutExpired, OSError):
        return -1, ""


def version(salida: str) -> tuple:
    m = re.search(r"(\d+)\.(\d+)", salida)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def puerto_ocupado(puerto: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", puerto)) == 0


def chequear(app: Path) -> list:
    """Devuelve una lista de (estado, nombre, detalle/guía, bloqueante)."""
    r = []

    cod, out = correr(["node", "--version"])
    if cod == 0 and version(out) >= (20, 0):
        r.append((OK, "Node", out, False))
    else:
        r.append((FALTA, "Node >= 20", "Instalalo desde https://nodejs.org (LTS) y reabrí la terminal.", True))

    cod, out = correr(["pnpm", "--version"])
    if cod == 0:
        lock = app / "pnpm-lock.yaml"
        m = re.search(r"lockfileVersion:\s*'?(\d+)", lock.read_text(encoding="utf-8")[:200]) if lock.exists() else None
        if m and int(m.group(1)) >= 9 and version(out)[0] < 9:
            r.append((AVISO, "pnpm desactualizado", f"Tenés pnpm {out} pero el lockfile es v{m.group(1)} y pide pnpm >= 9. "
                      "No hace falta instalar nada: usá 'npx pnpm@9.15.9 install --frozen-lockfile' (y 'npx pnpm@9.15.9 dev').", False))
        else:
            r.append((OK, "pnpm", out, False))
    else:
        r.append((FALTA, "pnpm", "Corré: npm install -g pnpm   (o: corepack enable)", True))

    cod, out = correr([sys.executable, "-c", "import playwright; print('ok')"])
    if cod == 0:
        r.append((OK, "Playwright para Python", "instalado", False))
    else:
        r.append((FALTA, "Playwright para Python",
                  "Corré: pip install playwright   y después: python -m playwright install chromium", True))

    cod, out = correr(["gh", "auth", "status"])
    if cod == 0:
        r.append((OK, "GitHub CLI autenticado", "gh auth status sin errores", False))
    elif cod == -1:
        r.append((FALTA, "GitHub CLI", "Instalalo desde https://cli.github.com y corré: gh auth login", True))
    else:
        r.append((FALTA, "GitHub CLI sin sesión", "Corré: gh auth login   (cuenta con acceso a vaiven-austral)", True))

    cod, out = correr(["docker", "--version"])
    if cod != 0:
        r.append((FALTA, "Docker", "Instalá Docker Desktop (https://www.docker.com/products/docker-desktop) y reiniciá.", True))
    else:
        cod, out = correr(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=30)
        # Con el daemon apagado `docker info` puede salir con 0 y escribir el error: se exige una versión.
        if cod == 0 and re.fullmatch(r"\d+\.\d+[\w.\-+]*", out):
            r.append((OK, "Docker corriendo", f"servidor {out}", False))
        else:
            r.append((FALTA, "Docker instalado pero apagado", "Abrí Docker Desktop y esperá a que diga 'running'. Después volvé a correr este chequeo.", True))

    cod, out = correr(["supabase", "--version"])
    if cod == 0:
        r.append((OK, "Supabase CLI", out, False))
    else:
        cod2, out2 = correr(["npx", "--version"])
        guia = ("No está instalado, pero no hace falta instalarlo: la skill puede usar 'npx supabase' (descarga la primera vez). "
                "Si preferís instalarlo: scoop install supabase  (o https://supabase.com/docs/guides/local-development/cli/getting-started).")
        r.append((AVISO if cod2 == 0 else FALTA, "Supabase CLI", guia, cod2 != 0))

    if app.exists() and (app / "package.json").exists():
        r.append((OK, "Clon de vaiven-app", str(app), False))
        if (app / "supabase" / "config.toml").exists():
            r.append((OK, "supabase/config.toml en vaiven-app", "stack local configurado", False))
        else:
            r.append((FALTA, "supabase/config.toml", f"No está en {app}. ¿Rama equivocada?", True))
        if (app / "node_modules").exists():
            r.append((OK, "Dependencias de vaiven-app", "node_modules presente", False))
        else:
            r.append((AVISO, "Dependencias de vaiven-app", f"Corré: pnpm install   (dentro de {app})", False))
        if (app / ".env").exists():
            r.append((OK, ".env de vaiven-app", "presente (no se imprime su contenido)", False))
        else:
            r.append((FALTA, ".env de vaiven-app", "Copiá .env.example a .env. Debe apuntar al stack LOCAL (http://127.0.0.1:54321), no a vaiven-dev.", True))
    else:
        r.append((FALTA, "Clon de vaiven-app", f"No encontré {app}. Clonalo (git clone https://github.com/vaiven-austral/vaiven-app) o pasá --app <ruta>.", True))

    n8n_datos = ROOT.parent / "n8n-data-vaiven"
    if n8n_datos.exists():
        r.append((OK, "Datos de n8n (motor de matching)", "carpeta n8n-data-vaiven presente: workflow y credenciales locales ya configurados", False))
    else:
        r.append((AVISO, "Datos de n8n", "No hay n8n configurado en esta máquina. Los flujos sin motor se pueden probar igual; "
                        "para el matching hay que importar vaiven-app/n8n/workflows/matching-v3.json y crear las credenciales locales.", False))

    ocupados = [f"{p} ({n})" for p, n in PUERTOS.items() if puerto_ocupado(p)]
    if ocupados:
        r.append((AVISO, "Puertos ya en uso", "Ocupados: " + ", ".join(ocupados) + ". Si es el stack de una corrida anterior, bajalo antes de empezar.", False))
    else:
        r.append((OK, "Puertos libres", ", ".join(str(p) for p in PUERTOS), False))

    return r


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, default=APP_DEFAULT, help="Ruta del clon de vaiven-app a probar")
    ap.add_argument("--check", action="store_true", help="Sale 1 si falta algo bloqueante")
    args = ap.parse_args()

    resultados = chequear(args.app.resolve())
    for estado, nombre, detalle, _ in resultados:
        print(f"[{estado}] {nombre}: {detalle}")

    bloqueantes = [n for e, n, _, b in resultados if e == FALTA and b]
    print()
    if bloqueantes:
        print(f"Faltan {len(bloqueantes)} requisitos bloqueantes: " + "; ".join(bloqueantes))
        return 1 if args.check else 0
    print("Todo lo bloqueante está resuelto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
