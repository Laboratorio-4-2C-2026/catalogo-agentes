---
name: g02-stacked-pr-guard
description: Antes de mergear una PR de Zest o borrar una rama, detecta PRs abiertas que apuntan a una rama ya mergeada o que dependen de esa rama, para que nada caiga en una rama muerta. Usar con PRs apiladas; no define la estrategia de ramas.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Luz Laura
    github: luzlaura
  responsables:
  - luzlaura
  madurez: usado-en-proyecto
  relacionados:
  - g02-stale-review-guard
---
# Stacked PR Guard

En Zest las PRs van contra `dev`, pero a veces se apilan: una PR apunta a la rama de otra. Si la PR de abajo se mergea y la de arriba sigue apuntando a esa rama, el trabajo cae en una rama muerta y nunca llega a `dev`. Ya pasó con la PR 44.

## Cuándo usarla

- Antes de mergear una PR que tenga otras apiladas encima.
- Antes de borrar una rama.
- Al empezar una tanda de revisiones, para saber el orden.

## Pasos

1. Corré el script, que solo lee GitHub:

   ```bash
   python3 stacked_prs.py proyecto-zest/zest
   ```

   Para preguntar por una rama puntual antes de borrarla o mergearla:

   ```bash
   python3 stacked_prs.py proyecto-zest/zest --branch ZEST-126
   ```

2. Interpretá cada alerta:
   - **RAMA MUERTA:** la base de la PR ya se mergeó. Hay que cambiar la base de la PR antes de mergearla.
   - **Base sin PR:** la PR apunta a una rama que no tiene PR propia. Hay que preguntarle al autor adónde tiene que llegar.
   - **Cadena:** el orden correcto es de abajo hacia arriba.
3. Antes de afirmar que una rama está muerta, mirá el destino de la PR que la mergeó: si no fue `dev`, el código puede no haber llegado a `dev` todavía.
4. Armá el mensaje para el autor de la PR.

## Reglas

- No cambies bases, no mergees y no borres ramas. Solo informá y proponé.
- No publiques comentarios en GitHub sin el OK explícito de quien pidió el chequeo.

## Ejemplo de uso
**Pedido:** ¿Puedo mergear la PR 78 de Zest?
**Resultado:** Avisa que su base `ZEST-126` ya se mergeó en la PR 77, que la PR 80 está apilada encima, y propone cambiar la base antes de mergear.
