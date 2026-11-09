---
name: g02-demo-data-generator
description: Usar cuando piden datos para poblar la base de Zest. Lee la estructura actual de la base en el repo y genera un paquete listo para cargar con recetas reales, colecciones y usuarios ficticios, con fotos.
metadata:
  tipo: skill
  area:
  - datos
  fase:
  - desarrollo
  tecnologias:
  - typescript
  - postgresql
  - prisma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados: []
---
# Generador de datos de demo — Zest

## Objetivo
Cuando te lo piden, generar un **paquete listo para que un dev lo cargue** en su base local (o en staging):
- **Usuarios ficticios** que parezcan reales, con nombre, email y foto de perfil.
- **Recetas reales** (preparaciones que existen y funcionan), con ingredientes del catálogo, pasos y fotos.
- **Colecciones** de esos usuarios, con portada y color.

El dev solo copia una carpeta y corre un comando. **No cargar nada en ninguna base ni hacer commits**: entregar el paquete.

## Cantidades por defecto
Si el pedido no dice otra cosa: **8 usuarios, 30 recetas** (repartidas en todas las categorías y dificultades), **10 colecciones** con entre 3 y 8 recetas cada una. Cada receta tiene 1 o 2 fotos.

## Pasos

### 1. Actualizar el repo y leer la estructura
```bash
cd ~/zest-agentes/zest && git checkout main && git pull && git submodule update --init --recursive
```
Leer **siempre** antes de generar, porque la base cambia:
- `backend/prisma/schema.prisma`: modelos, campos y enums.
- `support/docs/db.md`: la fuente de verdad del modelo de datos.
- `backend/prisma/seed-data/ingredients.json`: el catálogo de ingredientes. **Las recetas solo pueden usar ingredientes de este catálogo**, con el nombre exacto (en inglés y en minúsculas).
- `backend/src/recipes/dto/create-recipe.dto.ts` y `backend/src/collections/dto/create-collection.dto.ts`: límites de cada campo.

Si el esquema tiene modelos o campos que `load-demo-data.ts` no cubre (por ejemplo `saved_recipes` o `planner_entries`), agregarlos al JSON y al cargador siguiendo el mismo estilo, y avisarlo en el README del paquete.

### 2. Armar la carpeta de entrega
```
~/zest-agentes/demo-data/<AAAA-MM-DD>/
├── LEEME.md
├── load-demo-data.ts        (copiado de esta skill)
└── demo-data/
    ├── seed-data.json
    ├── CREDITOS.md
    └── images/
```

### 3. Generar `seed-data.json`
```json
{
  "users": [
    { "handle": "martina.rios", "name": "Martina Ríos", "email": "martina.rios@example.com",
      "avatarUrl": "https://..." }
  ],
  "recipes": [
    { "slug": "milanesa-napolitana", "author": "martina.rios",
      "title": "Milanesa napolitana", "description": "...",
      "category": "ALMUERZO", "time": 45, "timeUnit": "MINUTOS", "difficulty": "MEDIA", "servings": 4,
      "ingredients": [ { "name": "ground beef", "amount": "800", "unit": "GRAMO" } ],
      "steps": [ "Paso 1...", "Paso 2..." ],
      "images": [ "images/milanesa-napolitana-1.jpg" ] }
  ],
  "collections": [
    { "slug": "clasicos-de-domingo", "owner": "martina.rios", "name": "Clásicos de domingo",
      "accentColor": "#E8A33D", "cover": "images/col-clasicos-de-domingo.jpg",
      "recipes": [ "milanesa-napolitana" ] }
  ]
}
```
Criterios de contenido:
- **Usuarios**: nombres variados y creíbles (Argentina y Latinoamérica), emails `nombre.apellido@example.com` (dominio reservado: nunca casillas reales). Nunca usar nombres de personas famosas.
- **Recetas**: en castellano, recetas reales con cantidades y pasos que funcionan. Mezclar clásicos argentinos (empanadas, chipá, locro, flan), cocina internacional y opciones vegetarianas. Cada autor con un estilo propio (alguien hace pastelería, otro cocina rápida, etc.).
- **Ingredientes**: si una receta necesita algo que no está en el catálogo, usar el equivalente más cercano que sí esté, o cambiar de receta. Nunca inventar nombres.
- **Colecciones**: nombres naturales ("Para el finde", "Viandas de la semana") y colores hexadecimales armónicos.

### 4. Conseguir las fotos
- **Recetas y portadas**: fotos reales del plato desde bancos con licencia libre (Unsplash, Pexels o Wikimedia Commons con licencia CC0 o CC BY). Descargarlas en `images/`, en jpg, de 1200 px de ancho como máximo y menos de 1 MB.
- **Avatares**: retratos de bancos libres (Unsplash o Pexels) o, como alternativa, avatares ilustrados de DiceBear (`https://api.dicebear.com/9.x/notionists/png?seed=<handle>`). Nunca fotos de personas famosas ni sacadas de redes sociales.
- Registrar en `CREDITOS.md` cada imagen con su fuente, autor y licencia.

### 5. Validar
```bash
python3 validate_seed.py --repo ~/zest-agentes/zest --data ~/zest-agentes/demo-data/<fecha>/demo-data
```
Corregir hasta que termine con **0 errores**.

### 6. Escribir el `LEEME.md` del paquete
Con estas instrucciones para el dev:
```markdown
# Datos de demo de Zest — <fecha>
<N> usuarios, <N> recetas y <N> colecciones, con fotos.

## Cómo cargarlos
1. Copiar `load-demo-data.ts` y la carpeta `demo-data/` dentro de `backend/prisma/`.
2. Con la base levantada y el `.env` del backend completo:
   cd backend
   npx prisma db seed                         # catálogo de ingredientes
   npx ts-node prisma/load-demo-data.ts       # datos + imágenes a S3
3. Sin acceso a S3: `npx ts-node prisma/load-demo-data.ts --skip-images`.
4. Para volver a cargar desde cero: agregar `--reset`.

Los usuarios de demo no pueden iniciar sesión: son autores de las recetas.
No commitear la carpeta `demo-data/` sin acordarlo con el equipo.
```

### 7. Entregar
Comprimir la carpeta (`zip -r demo-data-<fecha>.zip <fecha>`), adjuntar el zip al issue que pidió los datos y comentar el resumen: cantidades, categorías cubiertas y cualquier cambio que haya hecho falta en el cargador.

## Reglas
- No conectarse a ninguna base ni subir nada a S3: eso lo hace el dev con el paquete.
- No commitear ni abrir PRs.
- Solo imágenes con licencia libre, registradas en `CREDITOS.md`.

## Ejemplo de uso
**Pedido:** Necesito datos para poblar la base de Zest.
**Resultado:** Lee el esquema del repo, genera recetas, colecciones y usuarios ficticios con fotos libres y valida el paquete antes de adjuntarlo.
