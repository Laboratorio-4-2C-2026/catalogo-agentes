# ARCHIVO COPIADO desde el repositorio de dirección por
# scripts/sync-vaiven-agentes.py — editalo allá, no acá.
import re

def markdown_a_jira_wiki(md: str) -> str:
    lineas = md.splitlines()
    salida = []
    en_codeblock = False
    
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        
        # Codeblocks
        if linea.strip().startswith("```"):
            if not en_codeblock:
                lang = linea.strip()[3:].strip()
                if lang:
                    salida.append(f"{{code:{lang}}}")
                else:
                    salida.append("{code}")
                en_codeblock = True
            else:
                salida.append("{code}")
                en_codeblock = False
            i += 1
            continue
            
        if en_codeblock:
            salida.append(linea)
            i += 1
            continue

        # Horizontal rules
        if re.match(r'^\s*---+\s*$', linea):
            salida.append("----")
            i += 1
            continue

        # Headings (importante: Jira usa h1., h2., h3., etc. porque # es lista numerada!)
        m_head = re.match(r'^(#{1,6})\s+(.*)$', linea)
        if m_head:
            nivel = len(m_head.group(1))
            texto_head = m_head.group(2).strip()
            # Limpiar bold dentro del heading si hay
            texto_head = re.sub(r'\*\*([^*]+)\*\*', r'\1', texto_head)
            salida.append(f"h{nivel}. {texto_head}")
            i += 1
            continue

        # Tablas markdown
        if linea.strip().startswith("|") and linea.strip().endswith("|"):
            # Si la siguiente línea es separador |---|---|
            if i + 1 < len(lineas) and re.match(r'^\s*\|[-|\s]+\|\s*$', lineas[i+1]):
                # Es header de tabla: convertir a || Col 1 || Col 2 ||
                cols = [c.strip() for c in linea.strip().strip('|').split('|')]
                salida.append("|| " + " || ".join(cols) + " ||")
                i += 2 # saltar header y separador
                continue
            elif re.match(r'^\s*\|[-|\s]+\|\s*$', linea):
                # Línea separadora suelta
                i += 1
                continue
            else:
                # Fila de datos: | val 1 | val 2 |
                # Limpiar negritas de markdown a jira dentro de celdas
                fila = linea
                # reemplazar **bold** con *bold*
                fila = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', fila)
                # reemplazar `code` con {{code}}
                fila = re.sub(r'`([^`]+)`', r'{{\1}}', fila)
                salida.append(fila)
                i += 1
                continue

        # Checkboxes: - [ ] CA-1: ... -> * [ ] ...
        linea_cb = re.sub(r'^\s*-\s*\[\s*\]\s*', '* ( ) ', linea)
        if linea_cb != linea:
            linea = linea_cb
        else:
            # Listas normales
            # - item -> * item
            #   - subitem -> ** subitem
            m_bullet = re.match(r'^(\s*)[-*•]\s+(.*)$', linea)
            if m_bullet:
                indent = len(m_bullet.group(1))
                nivel_bullet = "*" * (indent // 2 + 1)
                linea = f"{nivel_bullet} {m_bullet.group(2)}"
            else:
                # Listas numeradas: 1. item -> # item
                m_num = re.match(r'^(\s*)\d+\.\s+(.*)$', linea)
                if m_num:
                    indent = len(m_num.group(1))
                    nivel_num = "#" * (indent // 2 + 1)
                    linea = f"{nivel_num} {m_num.group(2)}"

        # Inline code: `code` -> {{code}}
        linea = re.sub(r'`([^`]+)`', r'{{\1}}', linea)

        # Bold: **bold** -> *bold*
        linea = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', linea)

        salida.append(linea)
        i += 1

    return "\n".join(salida)
