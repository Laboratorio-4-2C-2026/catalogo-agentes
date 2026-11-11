#!/usr/bin/env python3
# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
"""auditar-jira.py — El sentido inverso de la sincronización: lee Jira y reporta
higiene del backlog.

Agente 5.5 del catálogo de la cátedra. Sin higiene no hay métrica: un burndown
sobre tickets sin estimar ni etiquetar no mide nada.

Cinco reglas, por issue del mapeo de sync-all-jira.py:
  R1  el archivo que define el ticket existe en el repositorio
  R2  la descripción publicada no está vacía (>= MIN_DESC caracteres)
  R3  todas las etiquetas canónicas del mapeo están puestas en el issue
  R4  la subtarea cuelga de un padre
  R5  el archivo declara horas asignadas o estimación, con número

Uso:
  python3 scripts/auditar-jira.py            # reporta y sale 0/1
  python3 scripts/auditar-jira.py --verbose  # lista también los que pasan

Credenciales en .env.jira (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN).
Solo stdlib.
"""

import argparse
import base64
import importlib.util
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_DESC = 200
TIMEOUT = 30


def contexto_ssl():
    """Contexto de verificación que funciona también con el Python de python.org.

    Esa instalación no usa el llavero del sistema y deja `cert.pem` vacío hasta
    que se corre `Install Certificates.command`, así que la verificación falla
    con CERTIFICATE_VERIFY_FAILED. Se prueba, en orden: los paths por defecto,
    certifi si está instalado, y el bundle del sistema de macOS.

    Nunca se desactiva la verificación: un token de Jira no viaja por un canal
    sin verificar.
    """
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) > 0:
        return ctx

    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass

    bundle = Path("/etc/ssl/cert.pem")
    if bundle.exists():
        return ssl.create_default_context(cafile=str(bundle))

    raise RuntimeError(
        "No se encontró un bundle de certificados. En macOS con Python de "
        "python.org, corré Applications/Python 3.x/Install Certificates.command"
    )


SSL_CTX = None


def cargar_mapeo():
    """MAPEO_COMPLETO vive en sync-all-jira.py, que tiene guiones en el nombre."""
    ruta = ROOT / "scripts" / "sync-all-jira.py"
    spec = importlib.util.spec_from_file_location("sync_all_jira", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MAPEO_COMPLETO


def cargar_credenciales():
    base_url = os.environ.get("JIRA_BASE_URL", "")
    email = os.environ.get("JIRA_EMAIL", "")
    token = os.environ.get("JIRA_API_TOKEN", "")

    for candidato in (ROOT / ".env.jira", ROOT / ".env"):
        if not candidato.exists():
            continue
        for linea in candidato.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k == "JIRA_BASE_URL" and not base_url:
                base_url = v
            elif k == "JIRA_EMAIL" and not email:
                email = v
            elif k == "JIRA_API_TOKEN" and not token:
                token = v

    return base_url.rstrip("/"), email, token


def traer_issue(base_url, auth_b64, key):
    url = f"{base_url}/rest/api/3/issue/{key}?fields=summary,labels,parent,issuetype,description"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth_b64}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8"))


def texto_de_adf(nodo) -> str:
    """Aplana un documento ADF a texto plano para poder medir su largo."""
    if isinstance(nodo, dict):
        propio = nodo.get("text", "")
        return propio + "".join(texto_de_adf(h) for h in nodo.get("content", []) or [])
    if isinstance(nodo, list):
        return "".join(texto_de_adf(h) for h in nodo)
    return ""


def auditar_issue(key, info, datos):
    """Devuelve la lista de reglas incumplidas. Vacía = pasa."""
    fallas = []
    campos = datos.get("fields", {}) or {}

    archivo = ROOT / info["file"]
    if not archivo.exists():
        fallas.append(f"R1 archivo inexistente: {info['file']}")
        contenido = ""
    else:
        contenido = archivo.read_text(encoding="utf-8")

    descripcion = texto_de_adf(campos.get("description")).strip()
    if len(descripcion) < MIN_DESC:
        fallas.append(f"R2 descripción de {len(descripcion)} caracteres (mínimo {MIN_DESC})")

    puestas = set(campos.get("labels") or [])
    faltantes = [e for e in info["labels"] if e not in puestas]
    if faltantes:
        fallas.append(f"R3 etiquetas faltantes: {', '.join(faltantes)}")

    tipo = ((campos.get("issuetype") or {}).get("name") or "").lower()
    es_subtarea = "/hito-3/" in info["file"]
    if es_subtarea and not campos.get("parent"):
        fallas.append(f"R4 subtarea sin padre (tipo en Jira: {tipo or 'desconocido'})")

    # Las tareas madre declaran las horas como "**Horas** | asignadas **6,0**";
    # los tickets, como "**Estimación**". Se aceptan las dos formas, y en las dos
    # tiene que haber un número de horas: la palabra sola no es una estimación.
    if contenido and not re.search(r"\*\*(Horas|Estimaci[óo]n)\*\*.{0,120}?\d+[,.]\d+",
                                   contenido, re.S):
        fallas.append("R5 el archivo no declara horas ni estimación")

    return fallas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="listar también los issues que pasan")
    args = parser.parse_args()

    base_url, email, token = cargar_credenciales()
    if not all([base_url, email, token]):
        print("Error: faltan credenciales (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN).",
              file=sys.stderr)
        print("Copiá .env.example a .env y completalo.", file=sys.stderr)
        return 2

    global SSL_CTX
    SSL_CTX = contexto_ssl()

    auth_b64 = base64.b64encode(f"{email}:{token}".encode()).decode()
    mapeo = cargar_mapeo()

    print(f"Auditoría de higiene — {len(mapeo)} issues en {base_url}\n")

    con_fallas, inalcanzables, limpios = {}, {}, 0

    for key, info in mapeo.items():
        try:
            datos = traer_issue(base_url, auth_b64, key)
        except urllib.error.HTTPError as e:
            inalcanzables[key] = f"HTTP {e.code}"
            continue
        except Exception as e:  # red, timeout, JSON roto
            inalcanzables[key] = str(e)
            continue

        fallas = auditar_issue(key, info, datos)
        if fallas:
            con_fallas[key] = fallas
        else:
            limpios += 1
            if args.verbose:
                print(f"  OK  {key}")

    if con_fallas:
        print("Issues con problemas de higiene:\n")
        for key, fallas in con_fallas.items():
            print(f"  {key}")
            for f in fallas:
                print(f"      - {f}")
        print()

    if inalcanzables:
        print("Issues que no se pudieron leer:\n")
        for key, motivo in inalcanzables.items():
            print(f"  {key}: {motivo}")
        print()

    print(f"Limpios: {limpios} | Con fallas: {len(con_fallas)} | Inalcanzables: {len(inalcanzables)}")
    return 0 if not con_fallas and not inalcanzables else 1


if __name__ == "__main__":
    sys.exit(main())
