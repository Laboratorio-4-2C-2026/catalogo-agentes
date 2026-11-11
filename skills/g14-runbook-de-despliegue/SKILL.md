---
name: g14-runbook-de-despliegue
description: Genera el instructivo paso a paso para que un dev sin experiencia levante un entorno en la nube (base Supabase, token de servicio del motor, n8n detrás de Caddy en una VM) con una comprobación observable al final de cada parte. Usala después de un spike de despliegue, cuando hay que convertir lo que se corrió en un runbook que otro pueda repetir sin preguntar.
metadata:
  tipo: skill
  area:
  - devops
  - documentacion
  fase:
  - despliegue
  tecnologias:
  - n8n
  - supabase
  - docker
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "14"
  autor:
    nombre: Anapaola Borda
    github: AnaB2
  colaboradores: []
  responsables:
  - AnaB2
  madurez: probado
  relacionados: []
---

# Runbook de despliegue

Convertís una corrida real de despliegue en un instructivo que un dev repite solo. El instructivo **no inventa pasos**: cada uno salió de una corrida con su salida, y cada parte termina en algo que se puede comprobar con un comando o una pantalla.

Caso de origen: el entorno `dev` de VaiVen (Supabase en São Paulo, n8n + Caddy en una VM `e2-small` de GCP, un JWT de rol propio para el motor). Instructivo resultante en `docs/qa/spike-despliegue-dev/instructivo.md`; trabas y tiempos reales en el `README.md` de esa carpeta; ajuste del proxy para la API de n8n en `docs/qa/spike-n8n-api-kpis/`.

## Entrada

1. El registro del spike: comandos corridos, salidas, tiempos y **trabas con su error exacto**. Sin eso no hay runbook, hay una receta supuesta.
2. Los archivos de despliegue que el spike dejó (compose, proxy, scripts de carga). Plantillas de ejemplo en `plantillas/`.
3. Quién ejecuta cada parte (por ejemplo, «dev de datos») y qué permisos necesita de antemano.

## Estructura del instructivo

- **Encabezado:** las partes en orden y quién hace cada una. Qué se hace en panel web y qué en terminal, y por qué la terminal (sólo lo que la UI no permite: migraciones, firma de tokens, importar credenciales).
- **Requisitos previos:** herramientas con el comando de instalación para Linux **y** Mac (en VaiVen el primer borrador asumía Mac: `pbpaste`, un CLI global; en Ubuntu limpio no andaba). Roles de nube que tiene que dar el owner.
- **Una sección por parte**, pasos numerados, con captura del panel donde hay una casilla que marcar.
- **Cierre de cada parte:** una comprobación con su resultado esperado exacto (`200`/`403`, «la lista muestra tres miembros», «`select name from vault.secrets` devuelve los dos nombres»).
- **Comprobaciones finales** del entorno entero, incluida la que demuestra que lo que no tiene que estar expuesto no responde.

## Reglas que el instructivo hace cumplir

1. **Ningún valor real** en el instructivo, el repo ni el ticket. Valores entre `<…>`; los secretos viajan por el canal privado y en la máquina viven fuera de cualquier repo (en VaiVen, `~/secretos-vaiven/` con `chmod 700`).
2. **Un secreto nunca va por argumento** de un comando (queda en el historial): se pega con `read -rs` a un archivo, se usa y el archivo se borra.
3. **El orden importa y se dice por qué.** En VaiVen la semilla de datos se carga al final, con el motor ya escuchando: si entra antes, sus filas quedan sin procesar.
4. **«Listo» es una respuesta concreta, no el healthcheck.** n8n responde `200` en el healthz antes de activar el workflow; listo es el `403` del webhook sin secreto (un `404` = todavía arrancando).
5. **Marcá con 🔴 lo irreversible o lo que rompe en el acto**: revocar la clave legacy que firma el token del motor, borrar el volumen de certificados (Let's Encrypt limita la reemisión), dejar en el SQL Editor una consulta guardada con un secreto.
6. **La cuenta administradora se crea desde la UI y se comprueba.** En VaiVen el alta del owner de n8n por API devolvió `200` sin grabarse y la instancia quedó con el formulario abierto ~22 h; a los segundos del certificado ya había un scanner.
7. **Lo que la UI no puede, va por script** y el script falla fuerte (`set -euo pipefail`, `assert` de que no quedó una URL local).
8. **Si algo se cuelga, el instructivo dice qué no tocar** («no abras el firewall: avisá en el ticket, casi siempre falta el rol de IAP»).

## Patrón de red usado (n8n en VM)

- n8n **sin puertos publicados**; delante Caddy en 80/443 con certificado automático. Sin dominio propio: `<ip-con-guiones>.sslip.io` con IP **estática**.
- `basic_auth` sobre el editor; excluidos `/webhook/*`, `/webhook-test/*` y, si se lee la API pública, `/api/*` con Swagger apagado.
- VM sin cuenta de servicio, casillas HTTP/HTTPS tildadas, `.env` con `chmod 600`.

## Plantillas de apoyo (`plantillas/`)

| Archivo | Qué es |
|---|---|
| `docker-compose.yml` | n8n + Caddy; valores desde `.env`, que no se versiona |
| `Caddyfile` | Proxy con basic auth en el editor y webhooks/API abiertos |
| `firmar-token-motor.py` | Firma HS256 de un JWT de rol propio leyendo el secreto **desde archivo** y el vencimiento por argumento (ISO con zona; rechaza uno ya vencido). Ajustá `role` |
| `cargar-en-n8n.sh` | Importa credenciales y workflow en la VM por stdin y borra los archivos aunque falle (`trap` de limpieza armado antes del primer paso) |

## Qué NO hacer

- No escribir un paso que no se corrió. Lo no probado va marcado `[por-verificar]` y fuera del camino principal.
- No copiar valores de `.env`, tokens ni contraseñas a ningún archivo del runbook.
- No resolver una traba de red abriendo el firewall a `0.0.0.0/0`: la decisión de acceso es humana.
- No declarar el entorno listo sin las comprobaciones finales corridas y su salida guardada.

## Ejemplo de uso

**Pedido:** Con el registro del spike de ayer, armá el instructivo para que el dev de datos levante Supabase, firme el token del motor y deje n8n andando en la VM.

**Resultado:** Devuelve un instructivo en tres partes con pasos numerados, requisitos para Linux y Mac, alertas 🔴 en los pasos irreversibles y una comprobación con resultado esperado al final de cada parte (por ejemplo, `200` en `juicios` y `403` en `perfiles` con el token del motor).
