---
name: g16-eureka-post-deploy
description: 'Agente de GitHub Actions que corre después de cada deploy a producción en Vercel y verifica que la configuración que no vive en el código (signer del contrato, proxy, Marketplace, bloque de deploy, variables públicas) coincida con la cadena. Un script determinista mide y el agente, en otro job sin acceso a Vercel, explica qué se rompe. Mantiene un único issue vivo.'
metadata:
  tipo: agente
  area:
  - devops
  - seguridad
  fase:
  - despliegue
  tecnologias:
  - nextjs
  - solidity
  herramientas:
  - claude-code
  requiere:
  - github
  - vercel
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  colaboradores:
  - nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - ValentinoGianuzzo
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-incidentes
  - g13-checklist-pre-deploy
  - g01-env-config-drift-auditor
---
# eureka-post-deploy

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-post-deploy`. Los archivos de esta carpeta (`.github/workflows/eureka-post-deploy.yml`, `scripts/postDeployCheck.mjs`, `scripts/validatePostDeploy.mjs`, `scripts/postDeployMessages.mjs`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: verificar la configuración después de cada
deploy a producción.

Varias cosas que hacen falta para registrar una patente no viven en el código:
el signer del contrato, la dirección del proxy y del Marketplace, el bloque de
deploy. Si alguna queda mal, el deploy sale verde y producción se rompe en
silencio. Con EP-58, además, cada intento fallido paga una subida a Arweave
antes de revertir.

Dos jobs separados a propósito. El primero baja de Vercel solo las variables
públicas que mide, corre un script determinista y valida su salida contra una
lista cerrada antes de subirla. El segundo, el del agente, no ve nada de
Vercel: recibe únicamente ese JSON ya validado.

Lo que sí toca el primer job es VERCEL_TOKEN, el mismo secreto que usa
deploy.yml. El `if` que lo limita a master no alcanza como frontera: está en
este mismo archivo, que se puede editar en una rama. La frontera de verdad es
un GitHub Environment con los secretos de Vercel restringidos a master, que
tiene que configurar un admin del repo para este workflow y para deploy.yml
(ver docs/AGENTES.md).

Mantiene un único issue vivo (etiqueta `post-deploy`): lo abre o actualiza
cuando hay errores y lo cierra cuando un deploy posterior sale limpio.
```

## Cómo corre

- **Se dispara:** cuando termina el workflow «Deploy to Vercel (Production)» (`workflow_run`), solo en `master`.
- **Herramientas del agente:** Read,Write,Glob,Grep, con un tope de 15 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - Los secretos `VERCEL_TOKEN`, `VERCEL_ORG_ID` y `VERCEL_PROJECT_ID`, idealmente en un GitHub Environment restringido a la rama por defecto (ver el comentario del workflow).
  - `scripts/postDeployCheck.mjs`, `scripts/validatePostDeploy.mjs` y `scripts/postDeployMessages.mjs` (incluidos): miden la configuración contra Avalanche Fuji y validan la salida contra una lista cerrada de textos. Las direcciones y chequeos son los de Eureka.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-post-deploy.yml`.

```text
Sos el verificador post-deploy de Eureka. Acaba de salir un deploy
a producción y algunos chequeos de configuración fallaron.

Leé `post-deploy.json` en la raíz del workspace. Tiene cada
chequeo con su estado (ok, aviso, error, no_verificable), un
detalle y los datos públicos que se midieron. Para entender qué
hace cada pieza podés leer `.github/copilot-instructions.md` y, si
existe, `contracts/DEPLOYMENTS.md`.

**No inventes nada.** Solo podés hablar de los chequeos que están
en el JSON. No supongas valores de variables que no aparecen.

Escribí `post-deploy-report.md`:
1. Una línea: qué deja de funcionar en producción por estos
   errores, en términos de usuario ("nadie puede registrar una
   patente", "las compras revierten").
2. Una sección por cada chequeo en `error`, con: qué no coincide
   (con las direcciones o valores del JSON), por qué rompe, y el
   paso exacto para corregirlo y quién lo hace (variable en Vercel
   → quien administra el proyecto de Vercel; transacción on-chain
   como `setSigner` → el owner del contrato, con el comando de
   `cast` o el script de contracts/script/ si existe).
3. Si hay chequeos en `aviso` o `no_verificable`, una lista corta
   al final, una línea cada uno.

En castellano y breve. Sin título: el issue ya lo tiene. Sin
imágenes, HTML ni links fuera de github.com: el paso que publica
los saca.
```

## Ejemplo de uso

**Pedido:** Un deploy a producción sale verde, pero la variable con la dirección del proxy del registro quedó apuntando a la implementación vieja.

**Resultado:** Abre o actualiza el issue con la etiqueta `post-deploy`: una línea con qué deja de funcionar en producción, una sección por cada chequeo en error con qué no coincide y cómo arreglarlo, y la tabla de chequeos del script. Cuando un deploy posterior sale limpio, cierra el issue.
