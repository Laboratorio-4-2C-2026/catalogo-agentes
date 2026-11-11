---
name: g14-demo-orquestada
description: Guía para diseñar una sesión de capacitación de 45 minutos sobre trabajo con subagentes (guion, tiempos, qué se muestra y cómo se disecciona el resultado). La práctica en vivo usa un ejercicio ajeno al producto del equipo, en una carpeta descartable cuyo código no se entrega ni se reutiliza. No genera prompts que construyan el producto. Usala para capacitar a desarrolladores nuevos en prompting y orquestación.
metadata:
  tipo: skill
  area:
  - ia
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - otra
  requiere: []
  grupo: "14"
  autor:
    nombre: Anapaola Borda
    github: AnaB2
  colaboradores: []
  responsables:
  - AnaB2
  madurez: usado-en-proyecto
  relacionados: []
---

# Demo orquestada (sesión de capacitación sobre subagentes)

Mostrás a los devs, en vivo, qué hace un agente orquestador con subagentes cuando las decisiones **ya están escritas** y tiene contra qué verificarse. El mensaje no es «la IA programa sola»: es *el agente no decidió nada; fue rápido porque tenía un contrato*.

**Límite de esta skill:** el ejercicio en vivo **no es el producto del equipo**. Si quien dirige no puede escribir código de producto, tampoco lo hace a través de un agente en una demo. Caso de origen: VaiVen, agosto 2026; esta versión reemplaza el ejercicio original por uno ajeno al producto.

## El ejercicio de práctica

Elegí algo **ajeno al dominio del producto**, chico y verificable, con un mini-contrato escrito por vos antes de la clase (una página: dos o tres decisiones con su porqué y criterios numerados). Ejemplo que funciona:

> **Agenda de préstamos de libros de un club de lectura**: una CLI que lee un CSV de préstamos, marca los vencidos y genera un resumen en Markdown. Contrato: «un préstamo vence a los 14 días», «el resumen ordena por días de atraso», «los socios se identifican por número, nunca por nombre».

Condiciones operativas:

1. Todo se escribe en una carpeta descartable fuera de cualquier repo (`~/demo-subagentes/`), sin `git remote`.
2. Se borra en pantalla como último acto.
3. Ni una línea llega a nadie: los devs se llevan un cheat sheet de una cara, no código.

## Qué tiene que traer el prompt del orquestador

Lo escribís vos para el ejercicio, en la clase se pega sin explicarlo. Lo aprendido en el ensayo:

- **Tabla «qué leer y para qué»**: una sección del contrato por tema. Se apunta al documento, no se lo resume.
- **Tres subagentes gordos**, no muchos finos (en el ensayo, dieciséis subagentes se quedaron sin sesión antes de la mitad). Ej.: lectura del CSV · reglas de vencimiento · resumen. Cada uno con un archivo de estado propio y un handshake de una línea (`LISTO/<subagente>.txt`).
- **Regla de honestidad**: una fila dice `[verificado]` sólo con el comando y su salida pegados; si no, `[falla]`. En el ensayo un `HTTP 500` quedó anotado «Completado».
- **Mínimos numerados** como criterio de aceptación (ej.: 3 vencidos en el CSV de prueba, orden correcto).
- **Reloj**: 10 minutos por subagente; vencido, `[falla]` y se sigue.

## Guion de 45 minutos

| Minuto | Qué pasa |
|---|---|
| **0'** | Se pega el prompt y se lanza: «son cien líneas y ninguna es código». |
| **0'–5'** | Cuatro palabras: **modelo**, **agente** (tiene manos), **MCP** (enchufes hacia afuera), **skill** (receta escrita una vez). |
| **5'–20'** | Tres movimientos, con material del run: apuntá el contexto, no lo describas · pedí de a un paso verificable · exigí evidencia. |
| **20'–30'** | Abrir lo que ellos ya tienen en su proyecto (instrucciones del repo, plantilla de ticket, DoD). Marco antes del reveal: lo que van a ver es un juguete sin review ni tests. |
| **30'–40'** | Reveal y **disección**: preguntarle al agente «¿por qué 14 días?», «¿por qué número y no nombre?». Tiene que responder citando el contrato; se abre al lado. Mostrar un `[falla]` honesto vale más que un verde. |
| **40'–45'** | Qué pueden hacer el lunes en su propio trabajo, cheat sheet, y el borrado en pantalla. |

## Precalentado

- [ ] Ensayo completo una vez y borrado.
- [ ] CSV de prueba con los casos que muestran el rango (vencidos, al día, borde de 14 días).
- [ ] Pantalla partida: izquierda el run, derecha lo que explicás.

## Qué NO hacer

- No usar el producto del equipo, su repo, su esquema ni sus tickets como ejercicio.
- No prometer que el código se comparte.
- No tapar en silencio lo que falló en vivo: es material de la disección.

## Ejemplo de uso

**Pedido:** Armame la sesión de capacitación del jueves para los dos devs nuevos: quiero mostrarles cómo se trabaja con subagentes.

**Resultado:** Devuelve el mini-contrato de un ejercicio ajeno al producto, los puntos que tiene que cubrir el prompt del orquestador, el checklist de precalentado y el guion minuto a minuto con las preguntas de disección y el borrado final de la carpeta descartable.
