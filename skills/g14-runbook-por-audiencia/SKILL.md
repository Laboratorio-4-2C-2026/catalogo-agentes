---
name: g14-runbook-por-audiencia
description: Convierte una feature ya mergeada en tres runbooks (devops, devs nuevos y dirección entrante) a partir de los mismos hechos extraídos del diff (migraciones, workflows de n8n, secretos y credenciales por nombre, variables, dependencias, infraestructura) y los audita con un verificador que comprueba cobertura, fugas entre audiencias, fuentes y existencia de lo citado. Usala después de mergear una feature, cuando alguien más tiene que operarla, mantenerla o decidir sobre ella; no inventa pasos que el diff no respalde ni reemplaza al runbook de un spike de despliegue.
metadata:
  tipo: skill
  area:
  - devops
  - documentacion
  fase:
  - despliegue
  - mantenimiento
  tecnologias:
  - agnostico
  - git
  - python
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: probado
  relacionados:
  - g14-runbook-de-despliegue
  - g14-cierre-y-congelamiento
---

# Runbook por audiencia

Un mismo cambio lo lee gente distinta: quien lo despliega necesita el orden y el rollback; quien lo mantiene, cómo probarlo y dónde se rompe; quien hereda el proyecto, qué riesgo queda y qué decidir. Escribir tres documentos a mano los hace contradecirse. Acá salen de **una sola lista de hechos**.

No se confunde con `g14-runbook-de-despliegue`, que convierte **un spike** en **un instructivo** para un dev novato. Esta parte del **diff de una feature ya mergeada**.

## Protocolo

1. **Extraer los hechos** (determinista, sólo lee git):
   `python3 scripts/extraer_hechos.py --repo <vaiven-app> --merge <sha del merge del PR> --ticket SCRUM-N --salida salidas/runbook-por-audiencia/SCRUM-N/hechos.json`
   (o `--rango A..B`). Cada hecho tiene id `H#`, origen y las audiencias a las que sirve. De un secreto o una credencial se guarda **el nombre, nunca el valor**.
2. **Leer el contexto**: el mensaje de los commits, los ADRs citados y las entradas de bitácora relacionadas (en VaiVen, `docs/architecture/adr/` y `docs/bitacora/` de `vaiven-direccion`). El ticket de Jira sólo si está en el repo: la skill no usa la red.
3. **Redactar las tres vistas** (`devops.md`, `devs.md`, `direccion.md`) con las reglas de abajo.
4. **Verificar**:
   `python3 scripts/verificar_runbook.py --hechos hechos.json --repo <vaiven-app> --raiz <carpeta de repos> --vistas devops.md devs.md direccion.md --salida verificacion.txt`
   Sale con 1 si hay errores. Se corrige la vista o, si el error muestra que la matriz estaba mal, la matriz, y se vuelve a correr.

## La matriz de audiencias

| Hecho | Devops | Devs | Dirección |
|---|---|---|---|
| Migración | Sí | Sí | Sólo si es destructiva, crea un rol o lee secretos |
| Secreto de Vault (nombre) | Sí | Sí: lo carga en local | Sí: como riesgo |
| Workflow de n8n | Sí | Sí | Sí |
| Credencial de n8n (nombre) | Sí | No | Sí: como riesgo |
| Variable de entorno | Sí | Sí | No |
| Dependencias | No | Sí | No |
| Infraestructura | Sí | No | No |
| Código de la app tocado | No | Sí | No |

La matriz está en `extraer_hechos.py`; cambiarla es una decisión, no un retoque.

## Reglas de redacción

- **Cada paso o viñeta cita su fuente**: `[H#]`, `[ticket]`, `[ADR-NNNN]`, `[commit <sha>]` o `[bitácora <archivo>]`. Sin fuente no se escribe.
- **Ningún valor secreto**: sólo nombres; el valor se entrega por canal privado.
- **Devops**: qué cambia, despliegue en orden con el porqué del orden, comprobación observable, qué hacer si falla y cómo volver atrás. 🔴 en lo irreversible o en lo que falla en silencio.
- **Devs**: qué es, cómo probarlo en local, trampas conocidas (de la bitácora).
- **Dirección**: qué cambió, por qué, riesgos abiertos, qué decidir. **Sin bloques de código** y sin comandos.
- Una comprobación es algo que se observa («aparece una ejecución en n8n»), no «debería funcionar».

## Qué verifica el verificador

Cobertura (todo hecho de una audiencia está en su vista), fuga (una vista no cita hechos de otra), fuente de cada viñeta y existencia de lo citado (rutas en el commit de la feature, ADRs y bitácora en los repos), nombres de variables y secretos que figuren en los hechos, patrones de secreto y bloques de código en dirección.

## Límites

- Sólo ve lo que está en el diff. Lo que se hizo a mano en un panel sin dejar rastro en el repositorio no aparece; el runbook lo dice como «pendiente de comprobar», no lo inventa.
- Comprueba que lo citado exista y esté cubierto, **no que la prosa sea correcta ni que el runbook funcione**. Que alguien lo siga de punta a punta es una prueba humana distinta, y hasta que se haga figura como pendiente.
- Las afirmaciones de comportamiento de una herramienta (por ejemplo, que dos webhooks iguales chocan en n8n) vienen del conocimiento del modelo y se marcan para confirmar en la primera prueba humana.

## Ejemplo de uso

**Pedido:** Armá el runbook de SCRUM-67 para devops, devs y dirección.

**Resultado:** extrae 7 hechos del merge del PR, redacta las tres vistas citando cada uno, y el verificador las aprueba. En el primer borrador detectó una credencial sin cubrir y una fuga de secretos hacia devs: eso corrigió la matriz.

## Evidencia de uso

`salidas/runbook-por-audiencia/` (09/11/2026), sobre dos PRs reales de `vaiven-app`: SCRUM-135 (motor con Gemini por Vertex) y SCRUM-67 (disparo asincrónico por trigger y Vault). El primer borrador de SCRUM-67 falló (`verificacion-borrador-1.txt`) y tras corregir pasó; `prueba-negativa.txt` muestra que el verificador rechaza una ruta inventada, una variable desconocida, un secreto, código en dirección y una viñeta sin fuente. **Pendiente: que una persona de otro rol siga la vista que le toca.**
