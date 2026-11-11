---
name: g07-demo-video
description: "Graba videos de demo de una app web con Playwright y screencast por CDP: carátula y placas con el estilo que pida el usuario, subtítulos quemados y .srt, partes aceleradas en vez de cortadas, tope de duración y versión sin subtítulos con guion para narrar en vivo, grabando siempre desde la rama principal en un worktree y un stack aparte. Usar cuando se pida un video, una demo o una grabación de un flujo de la app. Pide al inicio el flujo, la duración, el estilo y cómo levantar y sembrar el entorno."
metadata:
  tipo: skill
  area:
  - documentacion
  - frontend
  fase:
  - revision
  tecnologias:
  - playwright
  - nodejs
  - docker
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Videos de demo

Sale de grabar las demos de sprint de un proyecto real. Documento vivo: cada video nuevo que descubra algo general lo agrega.

Resultado: un MP4 1920×1080 a 30 fps, con carátula, placas de transición, subtítulos quemados y un `.srt` al lado.

En `assets/ejemplo/` hay una implementación completa de un proyecto: `record.mjs` (captura, subtítulos, placas, aceleración y export), `seed.mjs`, `reset.ps1` y `compose.demo.yml`. Sirve de base: el motor de `record.mjs` se reusa, y el guion, el estilo, los datos y el reset se adaptan al proyecto.

---

## 1. Qué preguntar antes de empezar

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje**. Son las cosas que cambian el guion y el entorno:

1. **Duración**: objetivo y máximo. Sin dato, 55 s con tope de 60 s.
2. **Flujo**: qué pasos, en qué orden, con cuántos usuarios, y qué partes importan menos (esas se aceleran, no se cortan).
3. **Carátula y estilo**: imagen que abre el video, colores, fuentes y si las placas llevan algún elemento gráfico. Las placas copian el estilo de la carátula (§6).
4. **Para qué se usa**: no es lo mismo un video que se explica solo (subtítulos quemados, ritmo ágil) que uno que alguien narra en vivo (sin subtítulos, más lento, §4). Si hay varias versiones del mismo flujo, preguntar cuál es la base.
5. **Idioma de los subtítulos**: el de la interfaz, salvo que se pida otro.
6. **Entorno**: cómo se levanta el back (por ejemplo un `docker-compose.yml`), en qué puerto y origen tiene que correr el front para que el CORS lo acepte, y cómo se crean los datos de la demo (por API desde base vacía, como en `assets/ejemplo/seed.mjs`).
7. **Dónde guardar**: una carpeta ignorada por git, y cómo se organizan las versiones (por ejemplo `<carpeta>/demo/<sprint>/<versión>/`). Si es un retoque de un video existente, se regraba sobre la misma versión; si cambia el objetivo, es una versión nueva al lado.

**Siempre se graba desde la rama principal actualizada**, nunca desde la rama en la que se esté trabajando. Si el flujo pedido todavía no está ahí, no se graba: avisar y ofrecer grabar lo que sí está.

Antes de armar el guion hay que recorrer el flujo en la app y mirarlo, no deducirlo del código:

- **Pantallas provisorias o vacías en el medio**: si una ruta intermedia no aporta nada, se entra directo a la de destino. Si la app protege rutas y redirige al login devolviendo a la ruta pedida, un `goto` a la ruta final evita el paso intermedio.
- **Acciones que terminan sin confirmación visible**: si al completar algo no aparece aviso ni cambio en pantalla, el subtítulo tiene que decir que quedó hecho.

---

## 2. Dónde va todo

```
<carpeta>/demo/<sprint>/<versión>/   ← carpeta ignorada por git
  app/                               worktree con el código que se graba
  record.mjs  seed.mjs  reset.*  compose.demo.yml
  output/<nombre>.mp4 + .srt
```

`<carpeta>/demo/` guarda además las imágenes de carátula compartidas. Los `output/` de versiones anteriores no se borran: sirven para comparar.

---

## 3. Preparar el entorno

```bash
# a. Código a grabar: un worktree de la rama principal actualizada
git fetch origin
git worktree add --detach <carpeta>/demo/<sprint>/<versión>/app origin/<rama principal>

# b. Herramientas, en la carpeta de la versión
npm init -y && npm i playwright ffmpeg-static @fontsource/<fuente>
npx playwright install chromium

# c. Dependencias del front del worktree
cd app/<carpeta del front> && npm ci

# d. Base nueva + datos, front levantado, y a grabar
./reset.sh            # o el equivalente del proyecto
npx vite --port <puerto que acepta el CORS> --strictPort
node record.mjs
```

- **El front va en el origen que acepta el CORS del back.** Si no, cada pedido falla y el video muestra errores.
- **El stack de la demo va aparte** (`docker compose -p <proyecto>-demo …`) y su base **no publica el puerto** al host, que puede estar ocupado por otro proyecto. Eso lo resuelve un override como `assets/ejemplo/compose.demo.yml`. Nunca frenar contenedores ajenos: revisar con `docker compose ls` y `docker ps` antes de tocar nada.
- **Si `git fetch` falla**, no grabar con refs viejas sin decirlo: avisar y acordar cómo seguir.

**Si estás en Windows:**
- `npm` puede no bajar el binario nativo de rolldown (bug de dependencias opcionales). Se instala a mano con la versión exacta que pide `node_modules/rolldown/package.json`, como `@rolldown/binding-win32-x64-msvc@<versión>` con `--no-save`.
- Si `git fetch` falla con "SSL certificate problem", `git -c http.sslBackend=schannel fetch origin` usa el almacén de certificados de Windows.
- `Get-Content` y `Set-Content` de PowerShell 5.1 rompen los acentos de los `.mjs`: editar con las herramientas de archivos o con node.

---

## 4. El guion

Todo el guion vive en el bloque de escenas de `record.mjs`; el resto del archivo no se toca salvo que cambie el estilo.

- **Subtítulos**: uno por acción, en tercera persona y en el idioma de la interfaz. Van abajo y se corren solos arriba mientras haya un aviso en pantalla. Cada uno queda un mínimo de ~0,3 s por palabra, medido en tiempo de video.
- **Lo que importa menos se acelera, no se corta**: `fast(2.5, ...)` envuelve, por ejemplo, los logins. La aceleración no descuadra los subtítulos ni el `.srt`.
- **Placas**: `card(SLIDES.x)` las abre y `card(null)` las cierra. Una placa abierta sobrevive a `page.goto`, que es lo que tapa el cambio de usuario.
- **Cambio de usuario**: placa → limpiar donde la app guarda la sesión (`sessionStorage`, `localStorage` o cookies; mirarlo en el código o preguntarlo) → `goto` a la ruta donde arranca el segundo usuario.
- **Ritmo**: `DEMO_PACE` multiplica todas las pausas y es la perilla para estirar o acortar el video entero de manera pareja. Ajustar de a poco: parte del tiempo es espera de red y no escala, así que subir el factor rinde menos de lo proporcional (de 1,35 a 2,05 llevó un video de 69 s a 91 s).
- **Versión para narrar en vivo**: `DEMO_SUBTITLES=0` no dibuja los subtítulos, pero los textos del guion se siguen registrando y salen en el `.srt` y en un `<nombre>-guion.md` con el minuto y la duración de cada escena: es la chuleta de quien presenta. Sin texto en pantalla que marque el ritmo, cada escena necesita una pausa mínima propia (`DEMO_HOLD`, ~3,8 s), y los logins se aceleran menos porque también se narran.
- **Si se pasa del máximo, el script corta con error** y no exporta. Es a propósito.

---

## 5. Revisar antes de entregar — obligatorio

Nunca entregar un video sin haberlo mirado. Sacar cuadros con ffmpeg y **leerlos**:

```bash
ff=$(node -e "process.stdout.write(require('ffmpeg-static'))")
"$ff" -v error -y -ss 1 -i output/demo.mp4 -vf "fps=1/3,scale=640:-1,tile=3x3" review/sheet-%d.png   # panorama
"$ff" -v error -y -ss 22.1 -t 0.6 -i output/demo.mp4 -vf "fps=10,scale=640:-1,tile=3x2" review/x.png  # un momento puntual
```

Checklist:

- [ ] La carátula es el primer cuadro y se ve entera.
- [ ] Ninguna placa tiene el cursor encima ni recorta sus elementos gráficos.
- [ ] Ningún subtítulo tapa algo que el espectador tiene que ver: aviso, botón del modal, última opción de un desplegable.
- [ ] Cada subtítulo se alcanza a leer.
- [ ] Los avisos de confirmación aparecen y se ven completos.
- [ ] La duración está dentro de lo pedido.
- [ ] Borrar `review/` antes de entregar.

Entregar el MP4 (y el `.srt`, si se pidió), decir de qué commit de la rama principal salió y qué queda corriendo (back y front, con sus puertos).

---

## 6. Estilo de las placas

Sale de la carátula y hay que mantenerlo en todas las placas: color de fondo, tipografía y peso del título y de la bajada, colores de acento, elementos gráficos y alineación. En `assets/ejemplo/record.mjs` el estilo está en el CSS de `#demo-card` y en el bloque `SLIDES`: se cambian ahí.

Si el usuario no da estilo, usar uno neutro (fondo claro, una sola tipografía sans, un color de acento) y mostrar la carátula antes de grabar el video entero.

La fuente va embebida en base64 desde `@fontsource/<fuente>`: el Chromium headless no tiene instaladas las fuentes de Google.

---

## 7. Trampas que ya costaron una regrabación

- **El screencast solo manda cuadros cuando cambia la pantalla.** Una placa quieta al inicio no genera ninguno: el primer cuadro se fuerza con `page.screenshot`.
- **El reloj de pared no coincide con el del video** de Playwright (arranca tarde y rellena al cerrar). Por eso se captura por CDP, donde cada cuadro trae su `metadata.timestamp`.
- **Los selectores por label o por rol enganchan de más.** `getByLabel('Contraseña')` también agarra el botón "Mostrar contraseña" (va con `{ exact: true }`), y `getByRole('listitem')` sin acotar agarra los ítems de la barra lateral (acotar al contenedor, filtrado por su heading).
- **Los avisos tipo toast suelen salir abajo al centro**, justo donde van los subtítulos: el subtítulo tiene que correrse.
- **Los desplegables que se abren hacia abajo** dejan su última opción detrás del subtítulo: elegir una opción que quede visible.
- **Cada grabación deja datos escritos**: correr el reset antes de cada corrida, siempre.
- **`docker compose down -v` solo del proyecto de la demo.** Confirmar con `docker compose ls` que no se está tocando otro.
- **El `page.goto` detrás de una placa deja cuadros en blanco** (la página vieja se descarga antes de que la nueva vuelva a pintar la placa): se nota como un corte. Durante la navegación va `capturing = false`, y se retoma con un `page.screenshot` de la placa ya pintada (ya está en el ejemplo).
- **Lo que vence con el tiempo se ve vacío al grabar**: si la app tiene presencia o actividad que expira (por ejemplo participantes de una sesión), los datos sembrados aparecen vacíos. El script tiene que mantenerlos vivos durante toda la toma (por ejemplo mandando heartbeats de otros usuarios).
- **Recortar pausas rinde más de lo que parece**: cada `wait` se paga también en los subtítulos que esperan su mínimo. Ajustar de a poco y regrabar.
- **El primer acceso puede encontrar a Vite transformando y optimizando**, y tardar más que el timeout normal: antes de capturar va un `goto` de precalentamiento con timeout largo. Si no, la toma muere esperando el formulario de login.
- **El entorno puede estar levantado por otra sesión**: antes de arrancar, mirar quién ocupa los puertos del front y del back y qué contenedores corren. Si el front que ya corre sirve un commit equivalente, se usa tal cual y no se frena nada; y como el reset borra el volumen de la demo, si ese stack lo levantó otro hay que preguntar antes de tirarlo.
- **Una versión nueva puede reusar el worktree de otra** cuando graba el mismo commit: alcanza con que su reset apunte al compose de esa carpeta. Ahorra un `npm ci` completo.

---

## 8. Los scripts de ejemplo

En `assets/ejemplo/`, de un proyecto real (con Windows y PowerShell). Se copian a la carpeta de la versión nueva y se adaptan:

- `record.mjs`: captura, subtítulos, placas, aceleración y export. Se editan el bloque `SLIDES`, el CSS de las placas y el guion de escenas (marcado con `── GUION ──`). Lo demás sale de variables de entorno: `APP_URL`, `DEMO_NAME` (nombre de los archivos), `DEMO_MAX_SECONDS` (tope, 60 por defecto) y `DEMO_COVER` (ruta de la carátula, que siempre hay que pasar).
- `seed.mjs`: usuarios y datos de la demo cargados por la API. Se reescribe con los datos que pida el flujo.
- `reset.ps1`: base nueva + `seed.mjs`. En macOS o Linux se reescribe como `reset.sh` con los mismos pasos.
- `compose.demo.yml`: override para no publicar el puerto de la base.

## Ejemplo de uso

**Pedido:** "Grabame una demo de 60 segundos del flujo de invitar a alguien a un grupo y que lo acepte, para mostrar en la review del sprint."
**Resultado:** pregunta el estilo, la carátula y cómo levantar y sembrar el entorno, y arma un worktree de la rama principal con un stack aparte. Recorre el flujo, escribe el guion con dos usuarios y los logins acelerados, graba y revisa cuadros con ffmpeg. Entrega el MP4 con subtítulos y su `.srt`, diciendo de qué commit salió.
