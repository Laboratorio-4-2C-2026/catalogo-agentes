---
name: g01-seed-from-real-api
description: Genera un seed de base de datos con datos reales de una API pública (por ejemplo, películas de TMDB), guardados en un fixture JSON versionado para que el seed sea reproducible y no dependa de la red. Usar cuando los datos inventados no alcanzan para hacer demos o probar búsquedas y recomendaciones.
metadata:
  tipo: skill
  area:
  - datos
  - backend
  fase:
  - desarrollo
  tecnologias:
  - prisma
  - typescript
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '01'
  autor:
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: experimental
  relacionados:
  - g02-demo-data-generator-agent
---
# Seed from Real API

Armás un seed en dos pasos separados: **capturar** (llama a la API una vez y guarda un JSON) y **sembrar** (lee el JSON y escribe en la base). Así el seed corre sin red, sin API key y siempre da el mismo resultado.

## Pasos

1. **Definir el recorte.** Preguntá qué datos hacen falta y cuántos (por ejemplo, 300 películas populares con géneros, elenco y trailers). Fijá un criterio estable: endpoint, páginas, idioma y región.
2. **Script de captura** (`scripts/capture-fixture.ts`):
   - Reusá el cliente o el mapper que ya tenga el proyecto para esa API. Si no hay, usá `fetch` con timeout.
   - Respetá el rate limit con pocas requests en paralelo y una pausa entre lotes.
   - Guardá solo los campos que usa el schema, ya mapeados, en `prisma/fixtures/<nombre>.json`, ordenados por ID externo.
   - No guardes la API key ni datos personales.
   - Agregá al JSON la fecha de captura y la fuente, y respetá los términos de uso de la API (atribución, si la piden).
3. **Seed** (`prisma/seed.ts` o el seed del proyecto):
   - Leé el fixture y hacé `upsert` por ID externo para que se pueda correr dos veces sin duplicar.
   - Insertá en orden de dependencias: catálogos (géneros, personas, compañías), después las entidades principales y por último las tablas puente.
   - Usá `createMany({ skipDuplicates: true })` o transacciones por lote para que sea rápido.
   - Sumá encima los datos que la API no da (usuarios de prueba, grupos, swipes), con una semilla fija si son aleatorios.
4. **Verificar.** Corré el seed dos veces sobre una base vacía y comprobá que los conteos sean iguales. Revisá además que ninguna FK quede huérfana.
5. Documentá en el README cómo regenerar el fixture: `TMDB_API_KEY=... pnpm tsx scripts/capture-fixture.ts`.

## Reglas

- El seed nunca llama a la red.
- El fixture se versiona. Si pesa más de unos MB, achicá el recorte en lugar de comprimirlo.
- No uses el seed contra producción.

## Ejemplo

En Cinematch, el seed (`SeedAppModule`) carga `Movie`, `Genre`, `Person`, `MovieVideo` y sus tablas puente desde un fixture de TMDB. El feed y la búsqueda semántica muestran películas reales en las demos sin consumir cuota de la API.

## Ejemplo de uso

**Pedido:** Armame un seed con 300 películas reales de TMDB para las demos.

**Resultado:** Crea un script que captura una vez los datos de TMDB a un fixture JSON versionado y un seed idempotente que lo carga en la base sin usar la red, y verifica que correrlo dos veces dé los mismos conteos.
