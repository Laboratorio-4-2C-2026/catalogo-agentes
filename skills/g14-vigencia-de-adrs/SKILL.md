---
name: g14-vigencia-de-adrs
description: Audita si los ADRs de un proyecto siguen siendo ciertos contra el repositorio, con un script que comprueba estado y ratificaciones vencidas, reemplazos sin recíproco, enlaces rotos, rutas y variables de entorno citadas que ya no existen y marcadores abiertos, y deja las frases exactas a contrastar a mano. Usala al cerrar el proyecto o antes de un traspaso, cuando hay que saber qué decisiones siguen vigentes; no redacta ADRs (eso es g14-redactor-de-adrs) ni juzga si una decisión fue buena.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - mantenimiento
  - revision
  tecnologias:
  - agnostico
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
  - g14-redactor-de-adrs
---

# Vigencia de ADRs

Un ADR se escribe una vez y se cita para siempre. Con el tiempo, el entorno cambia, la mitigación que describía deja de existir o la ratificación nunca llega. Esta skill separa lo que se puede comprobar de lo que requiere criterio.

## Protocolo

1. **Capa determinista.** `python3 scripts/vigencia_adrs.py --adrs <carpeta de ADRs> --raiz <carpeta con los repos> --salida vigencia.md --json vigencia.json`
2. **Capa de criterio** (la hace la persona o el modelo, y sólo para los `a-revisar`): abrí cada frase que el informe cita junto a la referencia que falló y resolvé una de tres: *el ADR quedó desactualizado* (proponer enmienda o reemplazo con `g14-redactor-de-adrs`), *la referencia es ilustrativa* (anotarlo) o *falta el artefacto* (crearlo o corregir la cita).
3. **Estados.** Los `vigente-sin-ratificar` no tienen nada roto pero siguen «propuestos»: ratificarlos o dejar escrito que no se ratificarán es parte del cierre.

## Qué comprueba

Estado declarado (propuesto / aceptado / reemplazado, total o en parte), ratificación vencida, reemplazos sin recíproco, citas a ADRs reemplazados sin mencionar el reemplazo, enlaces relativos rotos, rutas entre backticks inexistentes en todos los repos, variables de entorno citadas sin rastro fuera de los `.md`, marcadores `[por-verificar]`/`[pendiente]`/`[ratifica…]`.

## Límites

- No lee la prosa: una afirmación como «las políticas viven en un archivo» sin ruta citada no se verifica. Por eso el informe es entrada para la capa de criterio, no un veredicto final.
- Una ruta o variable puede faltar porque es un ejemplo del ADR, o porque vive en un repo que no se pasó. `a-revisar` significa «alguien lo mira», no «está mal».

## Evidencia de uso

`salidas/vigencia-de-adrs.md` (08/11/2026): 15 ADRs de `vaiven-direccion`. Resultado: 1 reemplazado en parte, 4 a revisar, 8 vigentes sin ratificar (6 con la ratificación vencida entre 66 y 97 días), 2 vigentes. Hallazgos concretos: el ADR-0013 dice que lo reemplaza el 0018 y el 0018 no lo declara, y `VERTEX_SA_JSON`, citada en un ADR, no aparece en código ni config fuera de documentación.

## Ejemplo de uso

**Pedido:** ¿Qué ADRs siguen vigentes y cuáles quedaron desactualizados?

**Resultado:** Corre el script sobre la carpeta de ADRs, lista los que tienen referencias rotas o ratificaciones vencidas con la frase exacta, y para esos propone si enmendar, reemplazar o corregir la cita.
