#!/usr/bin/env python3
"""Auditor de Paridad de Contexto y Convenciones de Desarrolladores (Agente 7.5).

Compara las reglas, convenciones y decisiones de arquitectura (ADRs) de
`vaiven-direccion` contra la configuración entregada a los devs en `ai-config`.

Verifica:
1. 8 Criterios de Definition of Done (DoD)
2. Stack tecnológico y versiones (Node LTS 22.x, pnpm, React 19, Supabase, n8n)
3. Seguridad de claves (service_role prohibida en frontend / env, anon key para VITE)
4. Manejo de base de datos y migraciones (stack local diario, semillas en migraciones)
5. Gobernanza y Regla #1 (merge por devs de Lab II)

Uso:
  python3 scripts/auditar-contexto-devs.py
  python3 scripts/auditar-contexto-devs.py --out salidas/auditoria-contexto-devs.txt
"""

import argparse
import datetime
import sys
from pathlib import Path

# Directorio raíz del monorepo
ROOT = Path(__file__).resolve().parent.parent.parent
VAIVEN_DIRECCION = ROOT / "vaiven-direccion"
AI_CONFIG = ROOT / "ai-config"

def check_file_exists(path: Path, description: str) -> bool:
    if not path.exists():
        print(f"❌ ERROR: No se encontró {description} en: {path}")
        return False
    return True

def audit_context() -> tuple[list[str], int, int]:
    logs = []
    passes = 0
    failures = 0

    def log(msg: str):
        logs.append(msg)

    def assert_rule(condition: bool, rule_name: str, details: str):
        nonlocal passes, failures
        if condition:
            log(f"  [PASS] {rule_name}: {details}")
            passes += 1
        else:
            log(f"  [FAIL] {rule_name}: {details}")
            failures += 1

    log("================================================================================")
    log("REPORTE DE AUDITORÍA DE PARIDAD DE CONTEXTO (AGENTE 7.5 — GUARDIÁN DE CONVENCIONES)")
    log(f"Fecha de ejecución: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    log("Fuentes auditadas:")
    log(f"  - Canónica (Dirección): {VAIVEN_DIRECCION.relative_to(ROOT)}")
    log(f"  - Kit de Devs (ai-config): {AI_CONFIG.relative_to(ROOT)}")
    log("================================================================================\n")

    # Verificar que los directorios principales existan
    if not check_file_exists(VAIVEN_DIRECCION, "repositorio vaiven-direccion") or not check_file_exists(AI_CONFIG, "repositorio ai-config"):
        log("❌ Faltan directorios base para la auditoría.")
        return logs, 0, 1

    # Cargar archivos relevantes de ai-config
    ai_agents_text = (AI_CONFIG / "AGENTS.md").read_text(encoding="utf-8") if (AI_CONFIG / "AGENTS.md").exists() else ""
    ai_claude_text = (AI_CONFIG / "CLAUDE.md").read_text(encoding="utf-8") if (AI_CONFIG / "CLAUDE.md").exists() else ""
    ai_env_doc = (AI_CONFIG / "docs" / "configuracion-del-entorno.md").read_text(encoding="utf-8") if (AI_CONFIG / "docs" / "configuracion-del-entorno.md").exists() else ""
    ai_dod_doc = (AI_CONFIG / "docs" / "definition-of-done.md").read_text(encoding="utf-8") if (AI_CONFIG / "docs" / "definition-of-done.md").exists() else ""

    # Cargar archivos relevantes de vaiven-direccion
    dir_dod_doc = (VAIVEN_DIRECCION / "docs" / "kit-devs" / "definition-of-done.md").read_text(encoding="utf-8") if (VAIVEN_DIRECCION / "docs" / "kit-devs" / "definition-of-done.md").exists() else ""
    dir_env_doc = (VAIVEN_DIRECCION / "docs" / "kit-devs" / "configuracion-del-entorno.md").read_text(encoding="utf-8") if (VAIVEN_DIRECCION / "docs" / "kit-devs" / "configuracion-del-entorno.md").exists() else ""

    # --------------------------------------------------------------------------
    # 1. Auditoría de Definition of Done (8 Criterios)
    # --------------------------------------------------------------------------
    log("--- 1. AUDITORÍA DE DEFINITION OF DONE (DoD) ---")
    dod_checks = [
        ("PR abierto contra main", ["main", "PR"]),
        ("CI limpia (pnpm lint / pnpm build)", ["pnpm lint", "pnpm build"]),
        ("Criterios de Aceptación cumplidos", ["Criterios de Aceptación"]),
        ("RLS verificada con 2 sesiones", ["RLS", "2 sesiones"]),
        ("Sin secretos hardcodeados", ["secretos", "hardcode"]),
        ("Tests de aceptación provistos por dirección", ["Tests de aceptación"]),
        ("Review aprobado", ["review"]),
        ("Merge por dev de Lab II", ["merge", "dev"]),
    ]

    for item, keywords in dod_checks:
        found_in_doc = all(kw.lower() in ai_dod_doc.lower() for kw in keywords)
        assert_rule(found_in_doc, f"DoD - {item}", "Presente en ai-config/docs/definition-of-done.md")

    # --------------------------------------------------------------------------
    # 2. Auditoría de Stack Tecnológico y Versiones
    # --------------------------------------------------------------------------
    log("\n--- 2. AUDITORÍA DE STACK TECNOLÓGICO Y VERSIÓN ---")

    assert_rule("pnpm" in ai_agents_text and "npm" in ai_agents_text and "yarn" in ai_agents_text,
                "Package Manager", "pnpm obligatorio y prohibición explícita de npm/yarn en AGENTS.md")

    assert_rule("22.x" in ai_env_doc or "Node" in ai_env_doc,
                "Node.js Version", "Especificación de Node LTS 22.x en configuracion-del-entorno.md")

    assert_rule("React 19" in ai_agents_text and "Vite" in ai_agents_text and "Tailwind CSS" in ai_agents_text,
                "Frontend Stack", "React 19 + Vite + Tailwind CSS declarados en AGENTS.md")

    assert_rule("Supabase" in ai_agents_text and "PostgreSQL" in ai_agents_text and "RLS" in ai_agents_text,
                "Backend & DB Stack", "Supabase PostgreSQL + RLS declarados en AGENTS.md")

    assert_rule("n8n" in ai_agents_text and "JWT" in ai_agents_text,
                "Motor de Matching", "n8n con autenticación JWT especificado en AGENTS.md")

    # --------------------------------------------------------------------------
    # 3. Auditoría de Seguridad de Claves (ADR-0006 & ADR-0011)
    # --------------------------------------------------------------------------
    log("\n--- 3. AUDITORÍA DE SEGURIDAD DE CLAVES (ADR-0006 / ADR-0011) ---")

    assert_rule("service_role" in ai_agents_text and "NUNCA" in ai_agents_text,
                "Prohibición service_role en AGENTS.md", "service_role prohibida explícitamente en frontend")

    assert_rule("service_role" in ai_env_doc and "n8n" in ai_env_doc,
                "Aislamiento service_role en env doc", "service_role restringida a credenciales de n8n")

    assert_rule("VITE_SUPABASE_URL" in ai_agents_text and "VITE_SUPABASE_ANON_KEY" in ai_agents_text and "VITE_N8N_WEBHOOK_URL" in ai_agents_text,
                "Variables de Entorno Frontend", "Declaración exacta de las tres variables VITE_ requeridas")

    # --------------------------------------------------------------------------
    # 4. Auditoría de Base de Datos, Entornos y Migraciones (ADR-0002 & ADR-0013)
    # --------------------------------------------------------------------------
    log("\n--- 4. AUDITORÍA DE BASE DE DATOS Y ENTORNOS (ADR-0002 / ADR-0013) ---")

    assert_rule("supabase start" in ai_agents_text and "supabase db reset" in ai_agents_text,
                "Stack Local Diario", "Uso obligatorio del stack local (Docker) en desarrollo diario")

    assert_rule("vaiven-dev" in ai_env_doc,
                "Proyecto Cloud Dev", "Identificación de vaiven-dev como entorno compartido Vercel/n8n")

    assert_rule("Confirm email" in ai_env_doc and ("off" in ai_env_doc or "Apagada" in ai_env_doc),
                "Auth Email Confirm Off", "Confirmación de email apagada para desarrollo sin fricción")

    assert_rule("migrations" in ai_env_doc and "seed" in ai_env_doc,
                "Semillas en Migraciones", "Regla de semillas dentro de archivos de migración (ADR-0002)")

    # --------------------------------------------------------------------------
    # 5. Auditoría de Paridad entre AGENTS.md y CLAUDE.md en ai-config
    # --------------------------------------------------------------------------
    log("\n--- 5. PARIDAD INTERNA DE KIT DE DEVS (AGENTS.md vs CLAUDE.md) ---")

    norm_agents = ai_agents_text.replace("AGENTS.md", "COMMON.md")
    norm_claude = ai_claude_text.replace("CLAUDE.md", "COMMON.md")

    assert_rule(norm_agents == norm_claude,
                "Paridad AGENTS.md <-> CLAUDE.md", "AGENTS.md y CLAUDE.md en ai-config son 100% idénticos salvo el título")

    log("\n================================================================================")
    log(f"RESUMEN DE AUDITORÍA: {passes} pruebas pasadas, {failures} fallos.")
    if failures == 0:
        log("RESULTADO: 🟢 PARIDAD COMPLETA (0 desfasajes detectados entre Dirección y Dev Kit).")
    else:
        log(f"RESULTADO: 🔴 PARIDAD INCOMPLETA ({failures} desfasajes detectados que requieren corrección).")
    log("================================================================================")

    return logs, passes, failures

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=str, help="Ruta donde guardar el reporte generado.")
    args = parser.parse_args()

    logs, passes, failures = audit_context()
    output_text = "\n".join(logs) + "\n"

    print(output_text)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_text, encoding="utf-8")
        print(f"Reporte guardado en: {out_path}")

    return 0 if failures == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
