#!/usr/bin/env python3
# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
"""
formatear-para-jira.py — Transforma tickets y tareas de Markdown del repositorio
en descripciones limpias, humanas y listas para pegar en Jira (sin links relativos rotos,
sin asteriscos sueltos y sin metadatos redundantes).

Uso:
  python3 scripts/formatear-para-jira.py docs/planning/tickets/tarea-1-armado-inicial-de-la-app.md
  python3 scripts/formatear-para-jira.py docs/planning/tickets/hito-3/H3-1.1-proyecto-levanta-compila-despliega.md --clipboard
  python3 scripts/formatear-para-jira.py --ticket H3-1.1 -c
"""

import sys
import os
import re
import argparse
import subprocess

def limpiar_enlaces_markdown(texto: str) -> str:
    """
    Convierte enlaces markdown locales [Texto](../archivo.md) o [ADR-0011](../../...)
    en texto limpio y legible para Jira.
    """
    # 1. Limpiar enlaces con backticks dentro: [`H3-1.1`](...) -> H3-1.1
    texto = re.sub(r'\[`([^`]+)`\]\([^)]+\)', r'\1', texto)
    
    # 2. Limpiar enlaces normales con rutas relativas a .md: [Texto](../ruta.md) -> Texto
    def limpiar_texto_enlace(match):
        label = match.group(1).strip()
        # Si el label es una ruta tipo `diseño/sistema-de-diseño.md` o `sistema-de-diseño.md`
        if label.endswith('.md'):
            label = label.replace('.md', '').split('/')[-1].replace('-', ' ')
        return label

    texto = re.sub(r'\[([^\]]+)\]\([^)]+\.md(?:#[^)]*)?\)', limpiar_texto_enlace, texto)
    
    # 3. Limpiar cualquier otro enlace relativo que empiece con . o /
    texto = re.sub(r'\[([^\]]+)\]\(\.\.?[^)]*\)', r'\1', texto)
    
    return texto

def procesar_tarea_padre(contenido: str) -> str:
    """
    Procesa un archivo tarea-N-*.md y genera una descripción limpia de User Story/Tarea para Jira.
    """
    lineas = contenido.splitlines()
    
    # Extraer "Qué construye" / Objetivo
    que_construye = ""
    for i, l in enumerate(lineas):
        if "Qué construye." in l:
            que_construye = l.replace("**Qué construye.**", "").replace("Qué construye.", "").strip()
            if not que_construye and i + 1 < len(lineas):
                que_construye = lineas[i+1].strip()
            break

    if not que_construye:
        m = re.search(r'### Objetivo del módulo\s*\n(.*?)(?=\n###|\n##|\Z)', contenido, re.DOTALL)
        if m:
            que_construye = m.group(1).strip()

    # Extraer subtareas
    subtareas = []
    tabla_match = re.search(r'\| ID \| Ticket \|.*?\n\|[-| ]+\n(.*?)(?=\n\n|\n##|\Z)', contenido, re.DOTALL)
    if tabla_match:
        for fila in tabla_match.group(1).strip().splitlines():
            partes = [p.strip() for p in fila.split('|') if p.strip()]
            if len(partes) >= 2:
                ticket_id = re.sub(r'[`\[\]\(\)]', '', partes[0])
                ticket_id = ticket_id.split('.md')[0].split('/')[-1]
                nombre = re.sub(r'[`\*]', '', partes[1])
                horas = partes[2].replace('*', '').strip() if len(partes) > 2 else ""
                horas_str = f" ({horas} h)" if horas and not horas.endswith('h') else (f" ({horas})" if horas else "")
                subtareas.append(f"1. **{ticket_id}**: {nombre}{horas_str}")
    elif "### Subtareas incluidas" in contenido:
        m = re.search(r'### Subtareas incluidas\s*\n(.*?)(?=\n###|\n##|\Z)', contenido, re.DOTALL)
        if m:
            subtareas = [l.strip() for l in m.group(1).strip().splitlines() if l.strip()]

    # Dependencias / Contexto
    dependencias = ""
    m_dep = re.search(r'\|\s*\*\*Depende de\*\*\s*\|\s*(.*?)\s*\|', contenido)
    if m_dep:
        dep_raw = limpiar_enlaces_markdown(m_dep.group(1))
        dependencias = f"- **Dependencias:** {dep_raw}"
    elif "- Requiere" in contenido:
        m_req = re.search(r'(-\s*Requiere.*?)(?=\n\n|\n- Es el|\n###|\Z)', contenido, re.DOTALL)
        if m_req:
            dependencias = m_req.group(1).strip()
    
    m_desb = re.search(r'\|\s*\*\*Desbloquea\*\*\s*\|\s*(.*?)\s*\|', contenido)
    desbloquea = ""
    if m_desb:
        desb_raw = limpiar_enlaces_markdown(m_desb.group(1))
        desbloquea = f"- **Desbloquea:** {desb_raw}"
    elif "- Es el cimiento" in contenido:
        m_cim = re.search(r'(-\s*Es el cimiento.*?)(?=\n\n|\n###|\Z)', contenido, re.DOTALL)
        if m_cim:
            desbloquea = m_cim.group(1).strip()

    salida = []
    salida.append("### Objetivo del módulo")
    salida.append(limpiar_enlaces_markdown(que_construye or "Construir las funcionalidades asignadas a este módulo."))
    salida.append("")
    
    if subtareas:
        salida.append("### Subtareas incluidas")
        for st in subtareas:
            salida.append(limpiar_enlaces_markdown(st))
        salida.append("")

    if dependencias or desbloquea:
        salida.append("### Contexto y Dependencias")
        if dependencias:
            salida.append(dependencias)
        if desbloquea:
            salida.append(desbloquea)
        salida.append("")

    return "\n".join(salida).strip()

def procesar_subticket(contenido: str) -> str:
    """
    Procesa un archivo H3-N.M-*.md y genera una descripción limpia, técnica y humana para Jira.
    """
    # 1. Extraer objetivo
    objetivo = ""
    m_obj = re.search(r'>\s*\*\*En una línea\.\*\*\s*(.*?)(?=\n\n|\n---|\Z)', contenido, re.DOTALL)
    if m_obj:
        objetivo = m_obj.group(1).strip().replace('\n', ' ')
    else:
        m_obj2 = re.search(r'### Objetivo\s*\n(.*?)(?=\n###|\n---|\Z)', contenido, re.DOTALL)
        if m_obj2:
            objetivo = m_obj2.group(1).strip()

    # 2. Extraer secciones
    def extraer_seccion(regex_header, texto_completo):
        m = re.search(rf'##+ \s*{regex_header}\s*\n(.*?)(?=\n##+ |\Z)', texto_completo, re.DOTALL)
        if not m:
            return ""
        sec = m.group(1).strip()
        sec = re.sub(r'\n---+\s*$', '', sec).strip()
        return sec

    sec_guia = extraer_seccion(r'1\.\s*Qué hay que hacer.*?', contenido)
    sec_pruebas = extraer_seccion(r'2\.\s*Cómo probarlo.*?', contenido)
    sec_ca = extraer_seccion(r'3\.\s*Criterios de aceptación.*?', contenido)
    sec_dod = extraer_seccion(r'4\.\s*Definition of Done.*?', contenido)
    sec_alcance = extraer_seccion(r'5\.\s*Alcance.*?', contenido)

    # Evidencia requerida
    evidencia_texto = ""
    if "Evidencia para el PR:" in sec_dod:
        evidencia_texto = sec_dod.split("Evidencia para el PR:")[-1].strip()
    elif "Evidencia requerida" in sec_dod:
        evidencia_texto = sec_dod.split("Evidencia requerida")[-1].strip()
        if evidencia_texto.startswith(":") or evidencia_texto.startswith("para el PR:"):
            evidencia_texto = re.sub(r'^[^:\n]*:\s*', '', evidencia_texto).strip()

    salida = []
    
    if objetivo:
        salida.append("### Objetivo")
        salida.append(limpiar_enlaces_markdown(objetivo))
        salida.append("\n---\n")

    if sec_guia:
        salida.append("### 1. Guía de implementación")
        guia_limpia = re.sub(r'>\s*🎨\s*\*\*Mockup visual.*?\!\[.*?\]\([^)]+\)', '', sec_guia, flags=re.DOTALL)
        salida.append(limpiar_enlaces_markdown(guia_limpia.strip()))
        salida.append("\n---\n")

    if sec_pruebas:
        salida.append("### 2. Cómo probarlo localmente")
        salida.append(limpiar_enlaces_markdown(sec_pruebas))
        salida.append("\n---\n")

    if sec_ca:
        salida.append("### 3. Criterios de aceptación")
        ca_limpio = limpiar_enlaces_markdown(sec_ca)
        ca_limpio = re.sub(r'- \[[ xX]\] \*\*CA-\d+:\*\*', '- [ ]', ca_limpio)
        ca_limpio = re.sub(r'- \[[ xX]\]', '- [ ]', ca_limpio)
        salida.append(ca_limpio)
        salida.append("\n---\n")

    if evidencia_texto:
        salida.append("### 4. Evidencia requerida para el PR")
        ev_limpia = re.sub(r'^\*\*\s*$', '', evidencia_texto, flags=re.MULTILINE)
        salida.append(limpiar_enlaces_markdown(ev_limpia.strip()))
        salida.append("\n---\n")

    if sec_alcance:
        salida.append("### 5. Alcance y Decisiones técnicas")
        alcance_limpio = limpiar_enlaces_markdown(sec_alcance)
        alcance_limpio = re.sub(r'^[ \t]*[-•*]\s*\*\*Decisión[^:]*:\*\*', '- **Decisión técnica:**', alcance_limpio, flags=re.MULTILINE)
        alcance_limpio = re.sub(r'^[ \t]*[-•*]\s*\*\*Referencia[^:]*:\*\*', '- **Referencia:**', alcance_limpio, flags=re.MULTILINE)
        salida.append(alcance_limpio)

    res = "\n".join(salida)
    res = re.sub(r'(\n---\n\s*)+', '\n\n---\n\n', res)
    return res.strip()

def procesar_archivo(ruta: str) -> str:
    if not os.path.exists(ruta):
        print(f"Error: No existe el archivo {ruta}", file=sys.stderr)
        sys.exit(1)
        
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()

    nombre = os.path.basename(ruta)
    if nombre.startswith("tarea-"):
        return procesar_tarea_padre(contenido)
    else:
        return procesar_subticket(contenido)

def copiar_al_portapapeles(texto: str):
    try:
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(texto.encode('utf-8'))
        print("✓ Texto copiado al portapapeles con éxito (listo para pegar en Jira).", file=sys.stderr)
    except Exception as e:
        print(f"No se pudo copiar automáticamente al portapapeles: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Formatea tickets de Markdown para Jira.")
    parser.add_argument("archivo", nargs="?", help="Ruta al archivo Markdown (.md)")
    parser.add_argument("--ticket", "-t", help="ID del ticket (ej. H3-1.1 o tarea-1)")
    parser.add_argument("--clipboard", "-c", action="store_true", help="Copiar el resultado directamente al portapapeles (pbcopy)")
    
    args = parser.parse_args()

    ruta = args.archivo
    if not ruta and args.ticket:
        t_id = args.ticket
        base_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "planning", "tickets")
        
        # Buscar en tareas
        if os.path.exists(base_dir):
            for f in os.listdir(base_dir):
                if f.startswith(f"{t_id}-") or f == f"{t_id}.md":
                    ruta = os.path.join(base_dir, f)
                    break
                    
        # Buscar en hito-3
        if not ruta:
            h3_dir = os.path.join(base_dir, "hito-3")
            if os.path.exists(h3_dir):
                for f in os.listdir(h3_dir):
                    if f.startswith(f"{t_id}-") or f.startswith(t_id):
                        ruta = os.path.join(h3_dir, f)
                        break

    if not ruta:
        parser.print_help()
        sys.exit(1)

    resultado = procesar_archivo(ruta)
    print(resultado)

    if args.clipboard:
        copiar_al_portapapeles(resultado)

if __name__ == "__main__":
    main()
