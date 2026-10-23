"""Revisor de fichas con IA (opcional): corre la skill g03-revisor-de-fichas en
modo PR sobre las piezas que agrega o modifica un PR, usando la API de Claude.

Solo corre si el repo tiene el secreto ANTHROPIC_API_KEY. Sin key no hace nada
y el resto de la revisión sigue igual. El modelo se elige con la variable del
repo REVISOR_MODELO (por defecto claude-opus-5-5).

Uso: python scripts/revisor_ia.py --base origin/main [--dry-run]
Escribe un informe en Markdown. Nunca modifica archivos ni falla el PR.
"""
import argparse
import os
import subprocess
import sys

from common import FRONTMATTER, RAIZ, archivo_ficha, leer_ficha, piezas

SKILL = "skills/g03-revisor-de-fichas/SKILL.md"
MODELO_POR_DEFECTO = "claude-opus-5-5"
# Modelos que aceptan el reintento automático en otro modelo si uno rechaza el pedido.
CON_FALLBACK = {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}


def git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def leer(ruta):
    return ruta.read_text(encoding="utf-8") if ruta.exists() else ""


def armar_pedido(base):
    instrucciones = FRONTMATTER.sub("", leer(RAIZ / SKILL), count=1).strip()
    if not instrucciones:
        return None, None, []

    cambiados = git("diff", "--name-only", f"{base}...HEAD").split()
    tocadas = sorted({c.split("/")[1] for c in cambiados
                      if c.split("/")[0] in ("skills", "agentes", "comandos") and len(c.split("/")) > 2})

    indice, detalle = [], []
    for _, carpeta in piezas():
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        desc = str((ficha or {}).get("description", "")).strip().replace("\n", " ")
        indice.append(f"- {carpeta.name}: {desc}")
        if carpeta.name in tocadas:
            archivos = "\n\n".join(f"--- {a.relative_to(RAIZ).as_posix()} ---\n{leer(a)}"
                                   for a in sorted(carpeta.rglob("*")) if a.is_file() and a.suffix in (".md", ".yml", ".yaml"))
            detalle.append(f"## Pieza a revisar: {carpeta.name}\n\n{archivos}")

    if not detalle:
        return instrucciones, None, tocadas

    sistema = (instrucciones + "\n\n---\n\nEstás corriendo en **modo PR**, dentro de una revisión automática. "
               "Respondé solo con el comentario, en Markdown, con una sección por pieza. "
               "No modifiques archivos.")
    usuario = ("# taxonomia.yml\n\n" + leer(RAIZ / "taxonomia.yml")
               + "\n\n# Todas las piezas del catálogo (nombre: description)\n\n" + "\n".join(indice)
               + "\n\n# Piezas que agrega o modifica este PR\n\n" + "\n\n".join(detalle))
    return sistema, usuario, tocadas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--dry-run", action="store_true", help="muestra el tamaño del pedido sin llamar a la API")
    args = parser.parse_args()

    clave = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not clave and not args.dry_run:
        return  # Sin API key: el revisor con IA está apagado y no se muestra nada.

    print("### Revisor de fichas con IA\n")
    sistema, usuario, tocadas = armar_pedido(args.base)
    if sistema is None:
        print(f"No se encontró `{SKILL}` en main. Se activa cuando esa skill esté en el catálogo.\n")
        return
    if usuario is None:
        print("Este PR no agrega ni modifica piezas.\n")
        return

    modelo = os.environ.get("REVISOR_MODELO", "").strip() or MODELO_POR_DEFECTO
    if args.dry_run:
        print(f"Modelo: `{modelo}` · piezas: {', '.join(tocadas)} · "
              f"pedido de ~{(len(sistema) + len(usuario)) // 4} tokens (estimado).\n")
        return

    import anthropic

    cliente = anthropic.Anthropic(api_key=clave)
    extra = {}
    if modelo in CON_FALLBACK:
        extra = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
    try:
        respuesta = cliente.beta.messages.create(
            model=modelo,
            max_tokens=16000,
            output_config={"effort": "medium"},
            cache_control={"type": "ephemeral"},
            system=sistema,
            messages=[{"role": "user", "content": usuario}],
            **extra,
        )
    except anthropic.AuthenticationError:
        print("La API key del repo no es válida. Revisá el secreto `ANTHROPIC_API_KEY`.\n")
        return
    except anthropic.NotFoundError:
        print(f"El modelo `{modelo}` no existe. Revisá la variable `REVISOR_MODELO`.\n")
        return
    except anthropic.RateLimitError:
        print("La API rechazó el pedido por límite de uso. Volvé a correr la revisión más tarde.\n")
        return
    except anthropic.APIStatusError as e:
        print(f"La API devolvió un error ({e.status_code}). La revisión con IA se saltea en este PR.\n")
        return
    except anthropic.APIConnectionError:
        print("No se pudo conectar con la API. La revisión con IA se saltea en este PR.\n")
        return

    if respuesta.stop_reason == "refusal":
        print("El modelo no pudo revisar este PR.\n")
        return
    texto = "\n".join(b.text for b in respuesta.content if b.type == "text").strip()
    print((texto or "El modelo no devolvió sugerencias.") + "\n")
    if respuesta.stop_reason == "max_tokens":
        print("_(La respuesta se cortó por largo: puede faltar alguna pieza.)_\n")
    print(f"<sub>Modelo: {respuesta.model}</sub>\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # La revisión con IA nunca debe frenar el PR.
        print(f"La revisión con IA falló ({type(e).__name__}). El resto de la revisión no se ve afectado.\n")
        sys.exit(0)
