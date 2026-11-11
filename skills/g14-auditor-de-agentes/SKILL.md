---
name: g14-auditor-de-agentes
description: "Chequea con un script determinista, apto para pre-commit, la estructura e inventario de un repositorio de agentes según las convenciones de VaiVen (ficha, skill, disparo y fila de inventario con archivo de evidencia) y que no contenga código de producto. No valida el contenido de las evidencias ni el YAML completo, ni audita el kit de contexto de los devs."
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  - python
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-eficacia-de-agentes
  - g14-auditor-de-higiene-pre-entrega
---

# Auditor de agentes

Garantiza la gobernanza, integridad y auditabilidad del catálogo de agentes de **VaiVen**.

## El principio

Un agente existe cuando sus **4 piezas** están completas y verificadas:
1. **La Ficha** (`agentes/<id>-<slug>.md`)
2. **La Skill** (`.claude/skills/<slug>/SKILL.md`)
3. **El Disparo** (`hook` / `humano` / `evento` / `cron`)
4. **La Evidencia** (Fila en `inventario.md` + archivo en `salidas/`)

Además, vigila la regla de no escribir código de producto: este repositorio contiene únicamente herramientas, skills, scripts, fichas y artefactos de dirección. El código de producto pertenece exclusivamente a `vaiven-app`.

## El protocolo

**1. Ejecutar el script determinista de auditoría**

```bash
python3 scripts/auditar-agentes.py
```

Esto analizará el repositorio y actualizará el informe global en `salidas/reporte-auditoria-agentes.txt`.

**2. Verificar paridad estricta para integración o hooks**

```bash
python3 scripts/auditar-agentes.py --check
```

Si el comando retorna `0`, el script no encontró hallazgos en lo que chequea (estructura, inventario y extensiones prohibidas); no es una garantía sobre el contenido. Si retorna `1`, revisá los hallazgos impresos en consola y corregí la discrepancia antes de commitear.

**3. Reglas de validación aplicadas por el agente**

- **Ficha:** Debe existir en `agentes/`, estar formateada correctamente con la tabla de metadatos y contener el enlace a su skill en `.claude/skills/`.
- **Skill:** El archivo `.claude/skills/<slug>/SKILL.md` debe existir y contener un bloque frontmatter YAML válido con `name` y `description`.
- **Evidencia:** Los agentes marcados como `operando` deben contar con un archivo de salida en `salidas/` con tamaño mayor a 0 bytes. El script no valida su contenido: la evidencia específica de cada agente la revisa una persona.
- **Inventario:** Toda ficha en `agentes/` debe figurar clasificada en `inventario.md` (`Operando`, `En construcción` o `Descartados`).
- **Sin código de producto:** Ningún archivo del repositorio debe ser código fuente de aplicación (`.ts`, `.tsx`, `.js`, `.swift`, `.kt`, etc.) ni pertenecer a carpetas de producto (`src`, `app`, `components`).

## Enganche automático

El agente está integrado al `pre-commit` del equipo:

```bash
git config core.hooksPath scripts/githooks
```

## Ejemplo de uso

**Pedido:** Auditá si todos los agentes del inventario tienen ficha, skill y evidencia.

**Resultado:** Corre el script de auditoría y reporta por agente qué pieza falta o qué inconsistencia hay con el inventario; bloquea el commit si no hay paridad.
