"""Agente decisor sin IA: sugerencias para las piezas que agrega o modifica un PR.

- Skills relacionadas: piezas de cualquier grupo con texto parecido.
- Valores nuevos que parecen un error de tipeo de uno existente.
- Áreas que probablemente falten, según palabras clave.
- Descripciones y ejemplos de uso flojos.
- Aviso si el PR modifica piezas de otro grupo.

Uso: python scripts/decisor.py --base origin/main [--autor-pr usuario]
Escribe un informe en Markdown. Nunca modifica archivos ni falla el PR.
"""
import argparse
import difflib
import math
import re
import subprocess
from collections import Counter

from common import (CAMPOS_LISTA, CAMPOS_VALOR, RAIZ, archivo_ficha, cargar_yaml, clave_grupo,
                    como_lista, leer_ficha, piezas, slug, texto_ejemplo)

UMBRAL_RELACION = 0.22
MAX_RELACIONADAS = 3
NOMBRE = re.compile(r"^g(\d{2})-")

PALABRAS_VACIAS = set("""
a al algo ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre
era es esa ese eso esta este esto estos hace hacer hasta la las le les lo los mas me mi muy no o otra otro
para pero por que se ser si sin sobre su sus tambien te tiene todo tu un una uno unos y ya usar usa usando
skill skills agente agentes comando pieza piezas cada segun the and for with that this from into when use
uses using your you are can will not its any all
""".split())

# Palabras de actividad (no nombres de tecnologías: una skill de gestión puede
# mencionar Flutter sin ser de mobile). Hacen falta 2 distintas para sugerir.
PISTAS_AREA = {
    "qa": ["test", "tests", "testing", "prueba", "pruebas", "casos", "cobertura", "regresion"],
    "frontend": ["pantalla", "pantallas", "componente", "componentes", "interfaz", "estilos", "formulario"],
    "backend": ["api", "endpoint", "endpoints", "servidor", "migracion", "migraciones", "middleware"],
    "mobile": ["android", "ios", "celular", "apk", "emulador", "simulador"],
    "devops": ["docker", "pipeline", "deploy", "despliegue", "kubernetes", "contenedor", "infraestructura"],
    "documentacion": ["documenta", "documentar", "documentacion", "readme", "manual", "guia"],
    "gestion": ["ticket", "tickets", "sprint", "sprints", "estimacion", "backlog", "historias", "epica"],
    "diseno": ["figma", "diseno", "prototipo", "wireframe", "mockup", "maqueta"],
    "seguridad": ["seguridad", "vulnerabilidad", "vulnerabilidades", "owasp", "permisos", "credenciales"],
    "datos": ["datos", "etl", "sql", "dashboard", "metricas", "reporte", "reportes"],
}


def git(*args):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else ""


def palabras(texto):
    return [w for w in slug(texto).split("-") if len(w) > 2 and w not in PALABRAS_VACIAS and not w.isdigit()]


def cargar_piezas():
    todas = {}
    for tipo, carpeta in piezas():
        ruta, es_yml = archivo_ficha(carpeta)
        if not ruta:
            continue
        ficha, _ = leer_ficha(ruta, es_yml)
        if not ficha:
            continue
        meta = ficha.get("metadata") or {}
        ejemplo = texto_ejemplo(carpeta, ruta, es_yml) or ""
        nombre = carpeta.name
        texto = " ".join([NOMBRE.sub("", nombre)] * 2 + [str(ficha.get("description", "")), ejemplo,
                          " ".join(map(str, como_lista(meta.get("tecnologias")))),
                          " ".join(map(str, como_lista(meta.get("area"))))])
        todas[nombre] = {"carpeta": carpeta, "meta": meta, "descripcion": str(ficha.get("description", "")).strip(),
                         "ejemplo": ejemplo, "palabras": palabras(texto)}
    return todas


def vectores(todas):
    df = Counter()
    for p in todas.values():
        df.update(set(p["palabras"]))
    n = len(todas)
    for p in todas.values():
        tf = Counter(p["palabras"])
        v = {w: c * math.log((1 + n) / (1 + df[w])) for w, c in tf.items()}
        norma = math.sqrt(sum(x * x for x in v.values())) or 1.0
        p["vector"] = {w: x / norma for w, x in v.items()}


def similitud(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--autor-pr")
    args = parser.parse_args()

    todas = cargar_piezas()
    vectores(todas)
    valores = cargar_yaml(RAIZ / "taxonomia.yml").get("valores", {})

    cambiados = git("diff", "--name-only", f"{args.base}...HEAD").split()
    tocadas = sorted({c.split("/")[1] for c in cambiados
                      if c.split("/")[0] in ("skills", "agentes", "comandos") and len(c.split("/")) > 2})

    print("### Agente decisor (sugerencias)\n")
    bloques = []

    if args.autor_pr:
        integrantes = cargar_yaml(RAIZ / "integrantes.yml")
        grupo_pr = next((g for g, lista in integrantes.items()
                         if any(str(p.get("github", "")).lower() == args.autor_pr.lower() for p in lista or [])), None)
        ajenas = [n for n in tocadas if grupo_pr and NOMBRE.match(n) and clave_grupo(n[1:3]) != grupo_pr]
        if ajenas:
            bloques.append("⚠️ Este PR modifica piezas de otro grupo: " + ", ".join(f"`{n}`" for n in ajenas)
                           + ". Por acuerdo, cada grupo trabaja solo sobre las suyas.")

    for nombre in tocadas:
        p = todas.get(nombre)
        if not p:
            continue
        meta, items = p["meta"], []

        ya = set(como_lista(meta.get("relacionados")))
        parecidas = sorted(((similitud(p["vector"], o["vector"]), otro) for otro, o in todas.items()
                            if otro != nombre and otro not in ya), reverse=True)
        parecidas = [(s, o) for s, o in parecidas if s >= UMBRAL_RELACION][:MAX_RELACIONADAS]
        if parecidas:
            items.append("Skills parecidas que podrías sumar en `relacionados`: "
                         + ", ".join(f"`{o}`" for _, o in parecidas) + ".")
            for s, o in parecidas:
                if s >= 0.6:
                    items.append(f"Se parece mucho a `{o}`. Revisá que la `description` deje claro en qué se diferencia.")

        for campo in CAMPOS_LISTA + CAMPOS_VALOR:
            existentes = list(valores.get(campo) or {})
            for valor in como_lista(meta.get(campo)):
                if valor in existentes:
                    continue
                cerca = difflib.get_close_matches(str(valor), existentes, n=1, cutoff=0.8)
                if cerca:
                    items.append(f"`{campo}`: `{valor}` es un valor nuevo, pero se parece a `{cerca[0]}`. ¿Era ese?")

        texto = set(palabras(p["descripcion"] + " " + p["ejemplo"]))
        areas = set(como_lista(meta.get("area")))
        for area, pistas in PISTAS_AREA.items():
            if area not in areas and len(texto & set(pistas)) >= 2:
                items.append(f"Por lo que describe, quizás también corresponda `area: {area}`.")

        desc = p["descripcion"]
        if len(desc) < 60 or len(desc.split()) < 8:
            items.append("La `description` es muy corta: contá qué hace y cuándo usarla, en una o dos oraciones.")
        elif not re.search(r"\b(usar|úsala|usala|cuando|para)\b", desc, re.I):
            items.append("La `description` no dice cuándo usar la pieza (por ejemplo: \"Usar cuando…\").")

        ej = p["ejemplo"]
        if len(ej) < 80:
            items.append("El `Ejemplo de uso` es muy corto: mostrá un pedido concreto y qué devuelve.")
        elif not (re.search(r"pedido", ej, re.I) and re.search(r"resultado", ej, re.I)):
            items.append("Al `Ejemplo de uso` le conviene separar **Pedido** y **Resultado**.")

        bloques.append(f"**`{nombre}`**\n" + ("\n".join(f"- {i}" for i in items) if items else "- Sin sugerencias."))

    if not tocadas and not bloques:
        print("Este PR no agrega ni modifica piezas.\n")
    else:
        print("\n\n".join(bloques) + "\n")
        print("Son sugerencias: el grupo decide si las aplica. Nunca se fusionan ni se borran piezas.\n")


if __name__ == "__main__":
    main()
