"""e2e_comun.py — Piezas compartidas por los scripts del Tester E2E local (9.2).

Lo usan `e2e-flujos-base.py` y los guiones por ticket de `e2e/tickets/`. No se ejecuta solo.
Todo corre contra el stack LOCAL de vaiven-app; ningún helper imprime contraseñas ni claves.
"""

import base64
import json
import re
import secrets
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent.parent
PASA, FALLA, AVISO, NO_PROBADO = "PASA", "FALLA", "AVISO", "NO PROBADO"

# PNG de 1x1 px: alcanza para el campo de fotos de la donación.
FOTO_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)
GRUPOS = ("Activas", "En proceso", "Vencidas", "Completadas")


class Informe:
    """Pasos sueltos (flujos base). Cada paso: estado, nombre, detalle."""

    def __init__(self):
        self.filas = []

    def anotar(self, estado, paso, detalle=""):
        self.filas.append((estado, paso, detalle))
        print(f"[{estado:<10}] {paso}" + (f" — {detalle}" if detalle else ""))

    def cuenta(self, estado):
        return sum(1 for e, _, _ in self.filas if e == estado)

    def hay_fallas(self):
        return self.cuenta(FALLA) > 0

    def escribir(self, ruta: Path, titulo: str, subtitulo: str):
        lineas = [f"# {titulo}", "", subtitulo, "",
                  f"**{self.cuenta(PASA)} pasan · {self.cuenta(FALLA)} fallan · {self.cuenta(AVISO)} avisos**", "",
                  "| Resultado | Paso | Detalle |", "|---|---|---|"]
        lineas += [f"| {e} | {p} | {d} |" for e, p, d in self.filas]
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


class InformeCriterios:
    """Un bloque por criterio de aceptación: texto del ticket, veredicto y pasos ejecutados."""

    def __init__(self):
        self.criterios = []

    def criterio(self, numero, texto, estado, pasos, detalle=""):
        self.criterios.append((numero, texto, estado, pasos, detalle))
        print(f"[{estado:<10}] Criterio {numero}: {texto[:90]}" + (f" — {detalle}" if detalle else ""))

    def cuenta(self, estado):
        return sum(1 for c in self.criterios if c[2] == estado)

    def hay_fallas(self):
        return self.cuenta(FALLA) > 0

    def escribir(self, ruta: Path, titulo: str, subtitulo: str):
        lineas = [f"# {titulo}", "", subtitulo, "",
                  f"**{self.cuenta(PASA)} pasan · {self.cuenta(FALLA)} fallan · {self.cuenta(NO_PROBADO)} no probados**",
                  "", "| # | Criterio | Resultado |", "|---|---|---|"]
        lineas += [f"| {n} | {t} | {e} |" for n, t, e, _, _ in self.criterios]
        for n, t, e, pasos, d in self.criterios:
            lineas += ["", f"### Criterio {n} — {e}", f"> {t}", "", "Pasos ejecutados:"]
            lineas += [f"{i}. {p}" for i, p in enumerate(pasos, 1)]
            if d:
                lineas += ["", f"Detalle: {d}"]
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def sello() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H%M")


def carpeta_salidas(etiqueta: str) -> Path:
    """Carpeta del PR (salidas/e2e/<etiqueta>/), por ejemplo salidas/e2e/pr-74/."""
    if not re.fullmatch(r"[\w.\-]+", etiqueta):
        raise SystemExit("La etiqueta solo puede tener letras, números, punto, guion y guion bajo (por ejemplo pr-74).")
    c = ROOT / "salidas" / "e2e" / etiqueta
    c.mkdir(parents=True, exist_ok=True)
    return c


def archivo_unico(carpeta: Path, nombre: str, marca: str) -> Path:
    """Ruta <marca>-<nombre> borrando antes las corridas anteriores del mismo tipo: queda la última, no el historial."""
    for viejo in carpeta.glob(f"*-{nombre}"):
        viejo.unlink()
    return carpeta / f"{marca}-{nombre}"


def guardar_captura(page, etiqueta: str, nombre: str, marca: str, **opciones) -> Path:
    """Guarda una captura FUERA del repo (carpeta temporal del sistema) y avisa la ruta.

    Las capturas no se versionan: la skill las muestra en el chat y el informe en texto no las enlaza.
    La línea `CAPTURA: <ruta>` es la que la skill usa para encontrarlas.
    """
    carpeta = Path(tempfile.gettempdir()) / "vaiven-e2e" / etiqueta
    carpeta.mkdir(parents=True, exist_ok=True)
    for vieja in carpeta.glob(f"*-{nombre}"):
        vieja.unlink()
    ruta = carpeta / f"{marca}-{nombre}"
    page.screenshot(path=str(ruta), **opciones)
    print(f"CAPTURA: {ruta}")
    return ruta


def sha_probado(app: Path) -> str:
    """SHA corto del commit que se probó (para que el informe diga contra qué versión corrió)."""
    r = subprocess.run(["git", "-C", str(app), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() or "desconocido"


def solo_localhost(url: str):
    if not re.match(r"^http://(localhost|127\.0\.0\.1)(:\d+)?$", url):
        raise SystemExit("Solo se prueba contra localhost.")


def entorno_local(app: Path) -> tuple:
    """Devuelve (api_url, anon_key) del stack local, sin imprimirlos."""
    npx = shutil.which("npx")
    r = subprocess.run([npx, "--yes", "supabase", "status", "-o", "env"], cwd=app,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    valores = dict(re.findall(r'^(\w+)="?([^"\n]*)"?$', r.stdout, re.M))
    if "API_URL" not in valores or "ANON_KEY" not in valores:
        raise SystemExit("No pude leer el stack local. ¿Corrió 'supabase start' en " + str(app) + "?")
    if not valores["API_URL"].startswith("http://127.0.0.1"):
        raise SystemExit("El stack no es local; no sigo.")
    return valores["API_URL"], valores["ANON_KEY"]


def rest(api, anon, metodo, ruta, token=None, cuerpo=None):
    req = urllib.request.Request(api + ruta, method=metodo,
                                 data=json.dumps(cuerpo).encode() if cuerpo is not None else None)
    req.add_header("apikey", anon)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + (token or anon))
    if metodo == "PATCH":
        req.add_header("Prefer", "return=representation")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            texto = r.read().decode()
            return r.status, (json.loads(texto) if texto else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]


def crear_usuario(api, anon, etiqueta):
    email = f"qa-e2e-{int(time.time())}-{etiqueta}@example.test"
    clave = "E2e-" + secrets.token_urlsafe(12)
    estado, cuerpo = rest(api, anon, "POST", "/auth/v1/signup", cuerpo={"email": email, "password": clave})
    token = cuerpo.get("access_token") if isinstance(cuerpo, dict) else None
    return {"email": email, "clave": clave, "token": token, "ok": estado == 200 and bool(token)}


def pub_por_titulo(api, anon, usuario, titulo):
    """Fila de publicaciones (id, estado, vence_en) del usuario con ese título, o None."""
    est, filas = rest(api, anon, "GET", "/rest/v1/publicaciones?select=id,estado,vence_en&titulo=eq." +
                      urllib.parse.quote(titulo), token=usuario["token"])
    return filas[0] if est == 200 and filas else None


def login(page, url, usuario) -> bool:
    page.goto(url + "/login")
    page.get_by_placeholder("tu@email.com").fill(usuario["email"])
    page.locator("input[type=password]").fill(usuario["clave"])
    page.get_by_role("button", name="Ingresar").click()
    try:
        page.wait_for_url("**/feed", timeout=10000)
        return True
    except PWTimeout:
        return False


def _ubicacion(page):
    """Los tres selects de ubicación son los últimos del formulario."""
    sel = page.locator("select")
    n = sel.count()
    sel.nth(n - 3).select_option("AMBA")
    page.wait_for_timeout(400)
    sel.nth(n - 2).select_option("Quilmes")
    page.wait_for_timeout(400)
    sel.nth(n - 1).select_option("Bernal")


def publicar_necesidad(page, url, titulo) -> bool:
    page.goto(url + "/publicar/necesidad")
    page.get_by_placeholder("Ej: Notebook para cursar").fill(titulo)
    sel = page.locator("select")
    sel.nth(0).select_option(label="Tecnología")
    sel.nth(1).select_option(label="Alta")
    _ubicacion(page)
    page.get_by_placeholder("Contanos brevemente tu situación...").fill(
        "Necesito una notebook para cursar la carrera; la mía se rompió.")
    page.get_by_role("button", name=re.compile("Publicar necesidad")).click()
    try:
        page.wait_for_url("**/feed", timeout=15000)
        return True
    except PWTimeout:
        return False


def publicar_donacion(page, url, titulo):
    """Devuelve el aviso de la app sobre las fotos ('' si no hubo) para no confundirlo con un fallo."""
    page.goto(url + "/publicar/donacion")
    page.get_by_placeholder("Ej: Mantas de invierno 1½ plaza").fill(titulo)
    sel = page.locator("select")
    sel.nth(0).select_option(label="Hogar y menaje")
    sel.nth(1).select_option(label="Buen estado")
    _ubicacion(page)
    page.get_by_placeholder(re.compile("Detalles sobre el retiro")).fill(
        "Dos mantas de lana en buen estado. Retiro por la tarde.")
    page.locator("input[type=file]").set_input_files({"name": "foto.png", "mimeType": "image/png", "buffer": FOTO_PNG})
    page.get_by_role("button", name=re.compile("Publicar donación")).click()
    page.wait_for_timeout(4000)
    if "/feed" in page.url:
        return ""
    m = re.search(r"problema con las fotos[^\n]*", page.locator("body").inner_text())
    return m.group(0) if m else "la app no redirigió a /feed"


def grupos_historial(page) -> list:
    """Lee /historial y devuelve [(grupo, cantidad, [líneas del bloque])] en el orden en que se muestran."""
    lineas = [l.strip() for l in page.locator("main").inner_text().splitlines() if l.strip()]
    bloques, actual = [], None
    for l in lineas:
        m = re.fullmatch(r"(Activas|En proceso|Vencidas|Completadas)\s*·\s*(\d+)", l)
        if m:
            actual = [m.group(1), int(m.group(2)), []]
            bloques.append(actual)
        elif actual is not None:
            actual[2].append(l)
    return [tuple(b) for b in bloques]


def etiquetas_de_tipo(page) -> int:
    """Cuenta las etiquetas de tipo (NECESIDAD / DONACIÓN) que se ven en la pantalla actual."""
    return sum(1 for l in page.locator("main").inner_text().splitlines() if l.strip() in ("NECESIDAD", "DONACIÓN"))
