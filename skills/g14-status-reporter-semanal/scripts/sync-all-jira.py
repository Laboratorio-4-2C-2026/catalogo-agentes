#!/usr/bin/env python3
# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
"""
sync-all-jira.py — Sincroniza todas las Tareas y Subtareas en Jira con formato limpio
(Jira Wiki Markup) y etiquetas enriquecidas (front, back, n8n, db, auth, ui, etc.).
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.error
import importlib.util
from pathlib import Path

# Cargar formateadores
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

script_formateador = ROOT / "scripts" / "formatear-para-jira.py"
spec = importlib.util.spec_from_file_location("formatear_para_jira", script_formateador)
formateador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(formateador)
procesar_archivo = formateador.procesar_archivo

from md_to_jira import markdown_a_jira_wiki

MAPEO_COMPLETO = {
    # TAREAS MADRE
    "SCRUM-9": {
        "file": "docs/planning/tickets/tarea-1-armado-inicial-de-la-app.md",
        "labels": ["app", "front", "ui", "auth", "sprint-1"]
    },
    "SCRUM-10": {
        "file": "docs/planning/tickets/tarea-2-login-y-reglas-de-acceso.md",
        "labels": ["datos-motor", "back", "db", "auth", "rls", "sprint-1"]
    },
    "SCRUM-11": {
        "file": "docs/planning/tickets/tarea-3-formularios-de-publicacion-con-categoria-y-zona.md",
        "labels": ["app", "front", "ui", "forms", "db", "sprint-1"]
    },
    "SCRUM-12": {
        "file": "docs/planning/tickets/tarea-4-motor-de-matching-primera-version.md",
        "labels": ["datos-motor", "back", "n8n", "matching", "sprint-1"]
    },
    "SCRUM-13": {
        "file": "docs/planning/tickets/tarea-5-fotos-y-listado-de-publicaciones.md",
        "labels": ["app", "front", "ui", "storage", "sprint-2"]
    },
    "SCRUM-14": {
        "file": "docs/planning/tickets/tarea-6-estados-de-una-publicacion.md",
        "labels": ["datos-motor", "back", "db", "business-logic", "sprint-2"]
    },
    "SCRUM-15": {
        "file": "docs/planning/tickets/tarea-7-filtro-por-categoria-y-etiquetas.md",
        "labels": ["app", "front", "ui", "filters", "sprint-2"]
    },
    "SCRUM-16": {
        "file": "docs/planning/tickets/tarea-8-plataforma-y-integracion-continua.md",
        "labels": ["datos-motor", "back", "db", "storage", "ci", "devops", "sprint-2"]
    },

    # SUBTAREAS TAREA 1
    "SCRUM-17": {
        "file": "docs/planning/tickets/hito-3/H3-1.1-proyecto-levanta-compila-despliega.md",
        "labels": ["app", "front", "infra-dev", "vercel"]
    },
    "SCRUM-18": {
        "file": "docs/planning/tickets/hito-3/H3-1.2-sesion-y-rutas-protegidas.md",
        "labels": ["app", "front", "auth", "n8n", "routes"]
    },
    "SCRUM-19": {
        "file": "docs/planning/tickets/hito-3/H3-1.3-base-de-componentes.md",
        "labels": ["app", "front", "ui", "design-system", "tailwind"]
    },
    "SCRUM-20": {
        "file": "docs/planning/tickets/hito-3/H3-1.4-shell-encabezado-y-barra.md",
        "labels": ["app", "front", "ui", "navigation", "layout"]
    },

    # SUBTAREAS TAREA 2
    "SCRUM-21": {
        "file": "docs/planning/tickets/hito-3/H3-2.1-registro-inicio-y-cierre-de-sesion.md",
        "labels": ["datos-motor", "front", "auth", "supabase-auth"]
    },
    "SCRUM-22": {
        "file": "docs/planning/tickets/hito-3/H3-2.2-fila-en-perfiles.md",
        "labels": ["datos-motor", "back", "db", "auth", "triggers"]
    },
    "SCRUM-23": {
        "file": "docs/planning/tickets/hito-3/H3-2.3-piso-de-rls.md",
        "labels": ["datos-motor", "back", "db", "rls", "security"]
    },
    "SCRUM-24": {
        "file": "docs/planning/tickets/hito-3/H3-2.4-politicas-del-resto-de-tablas.md",
        "labels": ["datos-motor", "back", "db", "rls", "security"]
    },

    # SUBTAREAS TAREA 3
    "SCRUM-25": {
        "file": "docs/planning/tickets/hito-3/H3-3.1-selectores-categoria-y-zona.md",
        "labels": ["app", "front", "ui", "db", "select"]
    },
    "SCRUM-26": {
        "file": "docs/planning/tickets/hito-3/H3-3.2-formulario-de-necesidad.md",
        "labels": ["app", "front", "ui", "db", "forms"]
    },
    "SCRUM-27": {
        "file": "docs/planning/tickets/hito-3/H3-3.3-formulario-de-donacion.md",
        "labels": ["app", "front", "ui", "db", "forms"]
    },

    # SUBTAREAS TAREA 4
    "SCRUM-28": {
        "file": "docs/planning/tickets/hito-3/H3-4.1-workflow-porteado.md",
        "labels": ["datos-motor", "back", "n8n", "webhook"]
    },
    "SCRUM-29": {
        "file": "docs/planning/tickets/hito-3/H3-4.2-motor-lee-publicaciones.md",
        "labels": ["datos-motor", "back", "n8n", "db", "auth"]
    },
    "SCRUM-30": {
        "file": "docs/planning/tickets/hito-3/H3-4.3-nodo-de-la-aritmetica.md",
        "labels": ["datos-motor", "back", "n8n", "matching", "algorithms"]
    },
    "SCRUM-31": {
        "file": "docs/planning/tickets/hito-3/H3-4.4-puntaje-en-pantalla.md",
        "labels": ["datos-motor", "front", "ui", "n8n", "matching"]
    },
    "SCRUM-32": {
        "file": "docs/planning/tickets/hito-3/H3-4.5-corrida-contra-datos-reales.md",
        "labels": ["datos-motor", "back", "n8n", "qa", "testing"]
    },

    # SUBTAREAS TAREA 5
    "SCRUM-33": {
        "file": "docs/planning/tickets/hito-3/H3-5.1-listado-de-publicaciones.md",
        "labels": ["app", "front", "ui", "feed", "cards"]
    },
    "SCRUM-34": {
        "file": "docs/planning/tickets/hito-3/H3-5.2-subida-de-fotos.md",
        "labels": ["app", "front", "storage", "db", "upload"]
    },
    "SCRUM-35": {
        "file": "docs/planning/tickets/hito-3/H3-5.3-mostrar-fotos.md",
        "labels": ["app", "front", "ui", "storage", "images"]
    },

    # SUBTAREAS TAREA 6
    "SCRUM-36": {
        "file": "docs/planning/tickets/hito-3/H3-6.1-transiciones-de-estado.md",
        "labels": ["datos-motor", "back", "db", "rls", "business-logic"]
    },
    "SCRUM-37": {
        "file": "docs/planning/tickets/hito-3/H3-6.2-vencimiento-derivado.md",
        "labels": ["datos-motor", "back", "db", "sql"]
    },
    "SCRUM-38": {
        "file": "docs/planning/tickets/hito-3/H3-6.3-chip-de-estado.md",
        "labels": ["datos-motor", "front", "ui", "badge"]
    },

    # SUBTAREAS TAREA 7
    "SCRUM-39": {
        "file": "docs/planning/tickets/hito-3/H3-7.1-filtro-por-categoria.md",
        "labels": ["app", "front", "ui", "filters"]
    },
    "SCRUM-40": {
        "file": "docs/planning/tickets/hito-3/H3-7.2-campo-de-etiquetas.md",
        "labels": ["app", "front", "ui", "db", "tags"]
    },
    "SCRUM-41": {
        "file": "docs/planning/tickets/hito-3/H3-7.3-filtro-por-etiqueta.md",
        "labels": ["app", "front", "ui", "filters", "tags"]
    },

    # SUBTAREAS TAREA 8
    "SCRUM-42": {
        "file": "docs/planning/tickets/hito-3/H3-8.1-bucket-y-politicas.md",
        "labels": ["datos-motor", "back", "storage", "db", "security"]
    },
    "SCRUM-43": {
        "file": "docs/planning/tickets/hito-3/H3-8.2-tabla-de-etiquetas.md",
        "labels": ["datos-motor", "back", "db", "tags"]
    },
    "SCRUM-44": {
        "file": "docs/planning/tickets/hito-3/H3-8.3-normalizacion-de-nombres.md",
        "labels": ["datos-motor", "back", "db", "triggers", "sql"]
    },
    "SCRUM-45": {
        "file": "docs/planning/tickets/hito-3/H3-8.4-lint-y-build-en-cada-pr.md",
        "labels": ["datos-motor", "ci", "devops", "github-actions"]
    }
}

def cargar_config():
    base_url = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
    email = os.environ.get("JIRA_EMAIL", "").strip()
    token = os.environ.get("JIRA_API_TOKEN", "").strip()

    env_jira = ROOT / ".env.jira"
    if env_jira.exists():
        for line in env_jira.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k == "JIRA_BASE_URL" and not base_url:
                base_url = v.rstrip("/")
            elif k == "JIRA_EMAIL" and not email:
                email = v
            elif k == "JIRA_API_TOKEN" and not token:
                token = v

    return base_url, email, token

def actualizar_issue_completo(base_url, auth_b64, ctx, issue_key, descripcion_jira, labels):
    url = f"{base_url}/rest/api/2/issue/{issue_key}"
    payload = {
        "fields": {
            "description": descripcion_jira,
            "labels": labels
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_b64}"
        },
        method="PUT"
    )
    
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            if resp.status in (200, 204):
                print(f"✓ {issue_key:8s} | Etiquetas: {labels}")
                return True
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='ignore')
        print(f"✗ {issue_key:8s} | Error {e.code}: {err}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ {issue_key:8s} | Error de conexión: {e}", file=sys.stderr)
        return False

def main():
    base_url, email, token = cargar_config()
    if not base_url or not email or not token:
        print("Error: Credenciales no configuradas.", file=sys.stderr)
        sys.exit(1)

    auth_str = f"{email}:{token}"
    auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

    import ssl
    # Verificación TLS por defecto. Si en macOS falla con CERTIFICATE_VERIFY_FAILED, no se desactiva:
    # correr «Install Certificates.command» de python.org o exportar SSL_CERT_FILE=$(python3 -m certifi).
    ctx = ssl.create_default_context()

    print(f"Iniciando sincronización de {len(MAPEO_COMPLETO)} tickets en Jira ({base_url})...\n")

    exitos = 0
    errores = 0

    for issue_key, info in MAPEO_COMPLETO.items():
        rel_file = info["file"]
        labels = info["labels"]
        abs_path = ROOT / rel_file

        if not abs_path.exists():
            print(f"✗ {issue_key:8s} | No existe archivo {rel_file}", file=sys.stderr)
            errores += 1
            continue

        try:
            desc_limpia = procesar_archivo(str(abs_path))
            desc_jira = markdown_a_jira_wiki(desc_limpia)
            ok = actualizar_issue_completo(base_url, auth_b64, ctx, issue_key, desc_jira, labels)
            if ok:
                exitos += 1
            else:
                errores += 1
        except Exception as e:
            print(f"✗ {issue_key:8s} | Error procesando: {e}", file=sys.stderr)
            errores += 1

    print(f"\n--- Resumen ---")
    print(f"Total procesados: {len(MAPEO_COMPLETO)}")
    print(f"Exitosos: {exitos}")
    print(f"Fallidos: {errores}")

if __name__ == "__main__":
    main()
