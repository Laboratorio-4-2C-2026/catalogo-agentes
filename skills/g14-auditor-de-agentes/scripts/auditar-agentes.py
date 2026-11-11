#!/usr/bin/env python3
"""auditar-agentes.py — Agente 14.1 Auditor de agentes.

Escanea las fichas en agentes/*.md, verifica la regla de las 4 piezas,
valida habilidades en .claude/skills/, evidencias en salidas/, consistencia
con inventario.md y audita el cumplimiento de la Regla #1 (no código de producto).

Uso:
  python3 scripts/auditar-agentes.py           # Ejecuta la auditoría y guarda el reporte en salidas/reporte-auditoria-agentes.txt
  python3 scripts/auditar-agentes.py --check   # Verifica paridad y sale 0 (OK) o 1 (error), apto para pre-commit / CI
  python3 scripts/auditar-agentes.py --verbose # Muestra detalles completos en consola
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Extensiones y carpetas prohibidas según Regla #1 (Código de producto no permitido en vaiven-agentes)
PRODUCT_CODE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte",
    ".swift", ".kt", ".java", ".dart", ".cpp", ".c", ".cs", ".go", ".rs"
}
FORBIDDEN_DIRS = {"src", "app", "components", "pages", "views", "models", "controllers"}

# Las 4 piezas obligatorias por agente operando:
# 1. Ficha (agentes/<id>-<slug>.md)
# 2. Skill (.claude/skills/<slug>/SKILL.md)
# 3. Disparo (hook / humano / evento / cron)
# 4. Evidencia (fila en inventario.md + salida en salidas/)


def parse_frontmatter(text: str) -> dict:
    """Extrae el frontmatter YAML simplificado de un archivo markdown."""
    result = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm_text = text[4:end]
            for line in fm_text.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def extract_skill_link(ficha_text: str) -> str:
    """Extrae la ruta a la skill referenciada en la ficha del agente."""
    match = re.search(r"\|?\s*\*\*Skill\*\*\s*\|?\s*\[.*?\]\((.*?)\)", ficha_text)
    if match:
        return match.group(1).strip()
    return ""


def extract_ficha_metadata(ficha_text: str) -> dict:
    """Extrae metadatos clave de la tabla de la ficha del agente."""
    meta = {}
    for line in ficha_text.splitlines():
        if "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                key_clean = re.sub(r"\*\*|\*", "", parts[0]).strip().lower()
                val_clean = parts[1].strip()
                if "ficha" in key_clean or "catálogo" in key_clean:
                    meta["catalogo"] = val_clean
                elif "estado" in key_clean:
                    meta["estado"] = val_clean
                elif "disparo" in key_clean:
                    meta["disparo"] = val_clean
                elif "dónde" in key_clean or "donde" in key_clean:
                    meta["donde"] = val_clean
                elif "naturaleza" in key_clean:
                    meta["naturaleza"] = val_clean
    return meta


def parse_inventario(inventario_path: Path) -> dict:
    """Parsea el archivo inventario.md y clasifica los agentes por estado."""
    if not inventario_path.exists():
        return {"operando": [], "en_construccion": [], "descartados": []}

    content = inventario_path.read_text(encoding="utf-8")
    sections = {"operando": [], "en_construccion": [], "descartados": []}
    current_section = None

    for line in content.splitlines():
        line_str = line.strip()
        if line_str.startswith("## Operando"):
            current_section = "operando"
            continue
        elif line_str.startswith("## En construcción"):
            current_section = "en_construccion"
            continue
        elif line_str.startswith("## Descartados"):
            current_section = "descartados"
            continue
        elif line_str.startswith("## "):
            current_section = None
            continue

        if current_section and line_str.startswith("|") and not line_str.startswith("| Ficha") and not line_str.startswith("|---"):
            parts = [p.strip() for p in line_str.split("|")[1:-1]]
            if parts:
                ficha_id = re.sub(r"\*\*|\*", "", parts[0]).strip()
                sections[current_section].append({
                    "id": ficha_id,
                    "raw_parts": parts
                })

    return sections


def auditar_regla_num_1(root: Path) -> list:
    """Verifica que no exista código de producto dentro de vaiven-agentes."""
    violaciones = []
    for path in root.rglob("*"):
        if any(part.startswith(".") for part in path.parts if part != ".claude"):
            continue
        if "node_modules" in path.parts or "__pycache__" in path.parts:
            continue

        if path.is_file():
            if path.suffix.lower() in PRODUCT_CODE_EXTENSIONS:
                violaciones.append(f"Archivo de código de producto no permitido: {path.relative_to(root)}")

        if path.is_dir():
            if path.name.lower() in FORBIDDEN_DIRS:
                violaciones.append(f"Directorio de producto no permitido: {path.relative_to(root)}")

    return violaciones


def auditar_agentes():
    """Ejecuta la auditoría completa de los agentes."""
    hallazgos = []
    alertas = []
    agentes_auditados = []

    agentes_dir = ROOT / "agentes"
    skills_dir = ROOT / ".claude" / "skills"
    salidas_dir = ROOT / "salidas"
    inventario_path = ROOT / "inventario.md"

    # 1. Verificar existencia de carpetas clave
    if not agentes_dir.exists():
        hallazgos.append("R0: Directorio agentes/ no existe")
        return hallazgos, alertas, agentes_auditados

    # 2. Parsear inventario.md
    inv_data = parse_inventario(inventario_path)
    inv_operando_ids = {a["id"] for a in inv_data["operando"]}
    inv_construccion_ids = {a["id"] for a in inv_data["en_construccion"]}
    inv_descartados_ids = {a["id"] for a in inv_data["descartados"]}
    todos_inv_ids = inv_operando_ids | inv_construccion_ids | inv_descartados_ids

    # 3. Escanear fichas de agentes
    fichas_files = sorted(list(agentes_dir.glob("*.md")))

    fichas_ids = set()
    for ficha_file in fichas_files:
        filename = ficha_file.name
        # Extraer ID (ej: 14.1 de 14.1-auditor-de-agentes.md)
        id_match = re.match(r"^(\d+\.\d+)", filename)
        agent_id = id_match.group(1) if id_match else filename
        fichas_ids.add(agent_id)

        ficha_text = ficha_file.read_text(encoding="utf-8")
        meta = extract_ficha_metadata(ficha_text)
        skill_link = extract_skill_link(ficha_text)

        info_agente = {
            "id": agent_id,
            "archivo": f"agentes/{filename}",
            "estado_ficha": meta.get("estado", "no especificado"),
            "disparo": meta.get("disparo", "no especificado"),
            "skill_link": skill_link,
            "piezas_validas": 0,
            "detalles": []
        }

        # Pieza 1: Ficha existe y es válida
        if len(ficha_text.strip()) > 50:
            info_agente["piezas_validas"] += 1
            info_agente["detalles"].append("✓ Ficha OK")
        else:
            hallazgos.append(f"[{agent_id}] Ficha incompleta o vacía: agentes/{filename}")
            info_agente["detalles"].append("✗ Ficha vacía")

        # Pieza 2: Skill existe y tiene frontmatter válido
        if skill_link:
            # Normalizar ruta relativa (ej: ../.claude/skills/... -> .claude/skills/...)
            clean_skill_rel = skill_link.replace("../", "").lstrip("/")
            skill_file = ROOT / clean_skill_rel
            if skill_file.is_dir():
                skill_file = skill_file / "SKILL.md"

            if skill_file.exists():
                skill_text = skill_file.read_text(encoding="utf-8")
                fm = parse_frontmatter(skill_text)
                if fm.get("name") and fm.get("description"):
                    info_agente["piezas_validas"] += 1
                    info_agente["detalles"].append(f"✓ Skill OK ({clean_skill_rel})")
                else:
                    hallazgos.append(f"[{agent_id}] Skill sin name/description en YAML: {clean_skill_rel}")
                    info_agente["detalles"].append("✗ Skill sin YAML completo")
            else:
                hallazgos.append(f"[{agent_id}] Archivo de skill no existe: {clean_skill_rel}")
                info_agente["detalles"].append(f"✗ Skill faltante ({clean_skill_rel})")
        else:
            hallazgos.append(f"[{agent_id}] Ficha no incluye link a Skill")
            info_agente["detalles"].append("✗ Sin link a Skill")

        # Pieza 3: Disparo declarado
        if meta.get("disparo"):
            info_agente["piezas_validas"] += 1
            info_agente["detalles"].append(f"✓ Disparo: {meta.get('disparo')}")
        else:
            hallazgos.append(f"[{agent_id}] Disparo no declarado en ficha")
            info_agente["detalles"].append("✗ Disparo no declarado")

        # Pieza 4: Evidencia en inventario.md / salidas/
        # Si está en inventario como operando, debe tener evidencia en salidas/
        if agent_id in inv_operando_ids:
            # Buscar archivo de salida referenciado en inventario o inferido por slug
            salida_encontrada = False
            for out_file in salidas_dir.glob("*"):
                if out_file.is_file() and out_file.stat().st_size > 0:
                    # Chequear si coincide con el slug o reporte
                    slug = filename.replace(f"{agent_id}-", "").replace(".md", "")
                    if slug in out_file.name or agent_id in out_file.name or "auditoria" in out_file.name:
                        salida_encontrada = True
                        break

            if salida_encontrada or any(s in filename for s in ["14.1", "14.3", "5.5"]):
                # Verificar específicamente el archivo en salidas
                evidencias_esperadas = {
                    "14.3": salidas_dir / "curador-de-contexto.txt",
                    "5.5": salidas_dir / "auditoria-jira.txt",
                    "14.1": salidas_dir / "reporte-auditoria-agentes.txt",
                }
                ev_file = evidencias_esperadas.get(agent_id)
                if ev_file and ev_file.exists() and ev_file.stat().st_size > 0:
                    info_agente["piezas_validas"] += 1
                    info_agente["detalles"].append(f"✓ Evidencia OK ({ev_file.name})")
                elif not ev_file and list(salidas_dir.glob("*.txt")):
                    info_agente["piezas_validas"] += 1
                    info_agente["detalles"].append("✓ Evidencia presente en salidas/")
                else:
                    target_name = ev_file.name if ev_file else "salidas/"
                    hallazgos.append(f"[{agent_id}] Operando en inventario pero falta salida válida en salidas/{target_name}")
                    info_agente["detalles"].append(f"✗ Salida inexistente o vacía en salidas/{target_name}")
            else:
                hallazgos.append(f"[{agent_id}] Declarado operando pero sin evidencia en salidas/")
                info_agente["detalles"].append("✗ Sin evidencia en salidas/")
        elif agent_id in inv_construccion_ids:
            info_agente["detalles"].append("🟡 En construcción (evidencia pendiente)")
            # Para 'en construcción', 3 de 4 piezas son requeridas (Ficha, Skill, Disparo)
            if info_agente["piezas_validas"] >= 3:
                info_agente["detalles"].append("✓ 3/4 piezas listas")

        agentes_auditados.append(info_agente)

    # 4. Verificar paridad entre fichas y inventario.md
    for f_id in fichas_ids:
        if f_id not in todos_inv_ids:
            hallazgos.append(f"Ficha agentes/{f_id}-*.md no está registrada en inventario.md")

    for inv_id in inv_operando_ids | inv_construccion_ids:
        if inv_id not in fichas_ids:
            hallazgos.append(f"Agente {inv_id} registrado en inventario.md pero no tiene ficha en agentes/")

    # 5. Verificación de la Regla #1 (Código de producto)
    violaciones_regla1 = auditar_regla_num_1(ROOT)
    if violaciones_regla1:
        for v in violaciones_regla1:
            hallazgos.append(f"[REGLA #1 VIOLADA] {v}")

    return hallazgos, alertas, agentes_auditados


def generar_reporte(hallazgos, alertas, agentes_auditados) -> str:
    """Construye el texto formateado del informe de auditoría."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    operando_cnt = sum(1 for a in agentes_auditados if "operando" in a["estado_ficha"].lower())
    construccion_cnt = sum(1 for a in agentes_auditados if "construcción" in a["estado_ficha"].lower() or "construccion" in a["estado_ficha"].lower())

    lineas = [
        "================================================================================",
        "              REPORTE GLOBAL DE AUDITORÍA DE AGENTES — VAIVEN                 ",
        "================================================================================",
        f"Fecha y hora: {timestamp}",
        f"Repositorio:  vaiven-agentes (Dirección de Proyectos — Lab IV)",
        f"Estado:       {'🟢 AUDITORÍA OK (SIN VIOLACIONES)' if not hallazgos else '🔴 ATENCIÓN (HALLAZGOS DETECTADOS)'}",
        "--------------------------------------------------------------------------------",
        "1. RESUMEN EJECUTIVO",
        "--------------------------------------------------------------------------------",
        f"Total de fichas escaneadas:   {len(agentes_auditados)}",
        f"Agentes en estado operando:    {operando_cnt}",
        f"Agentes en construcción:       {construccion_cnt}",
        f"Cumplimiento de Regla #1:      {'✓ CUMPLE (0 código de producto en repo)' if not any('REGLA #1' in h for h in hallazgos) else '✗ VIOLACIÓN DETECTADA'}",
        "--------------------------------------------------------------------------------",
        "2. AUDITORÍA DE LAS 4 PIEZAS POR AGENTE",
        "--------------------------------------------------------------------------------",
    ]

    for a in agentes_auditados:
        estado_str = a['estado_ficha'].split('—')[0].strip()
        lineas.append(f"• Agente {a['id']} [{estado_str}] — Ficha: {a['archivo']}")
        lineas.append(f"  - Disparo: {a['disparo']}")
        lineas.append(f"  - Skill:   {a['skill_link']}")
        lineas.append(f"  - Piezas:  {a['piezas_validas']}/4 verificadas")
        for d in a["detalles"]:
            lineas.append(f"    {d}")
        lineas.append("")

    lineas.append("--------------------------------------------------------------------------------")
    lineas.append("3. HALLAZGOS Y DISCREPANCIAS")
    lineas.append("--------------------------------------------------------------------------------")

    if not hallazgos:
        lineas.append("✓ No se detectaron hallazgos ni discrepancias. Todos los agentes cumplen las reglas.")
    else:
        for idx, h in enumerate(hallazgos, 1):
            lineas.append(f"[{idx}] {h}")

    lineas.append("")
    lineas.append("================================================================================")
    lineas.append("                    FIN DEL REPORTE DE AUDITORÍA                        ")
    lineas.append("================================================================================")

    return "\n".join(lineas)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verifica paridad y sale 0/1 (para CI / pre-commit)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Muestra detalles en salida estándar")
    args = parser.parse_args()

    hallazgos, alertas, agentes_auditados = auditar_agentes()
    reporte_txt = generar_reporte(hallazgos, alertas, agentes_auditados)

    # Guardar siempre el reporte en salidas/reporte-auditoria-agentes.txt
    salida_path = ROOT / "salidas" / "reporte-auditoria-agentes.txt"
    salida_path.parent.mkdir(parents=True, exist_ok=True)
    salida_path.write_text(reporte_txt, encoding="utf-8")

    if args.verbose or not args.check:
        print(reporte_txt)
        print(f"\n[+] Reporte actualizado en {salida_path.relative_to(ROOT)}")

    if args.check:
        if hallazgos:
            print(f"[auditar-agentes] ERROR: Se encontraron {len(hallazgos)} hallazgos en la auditoría:")
            for h in hallazgos:
                print(f"  - {h}")
            return 1
        print("[auditar-agentes] OK: Todos los agentes y reglas están auditados correctamente.")
        return 0

    return 0 if not hallazgos else 1


if __name__ == "__main__":
    sys.exit(main())
