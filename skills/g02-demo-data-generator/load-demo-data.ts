/**
 * Carga los datos de demo de Zest (usuarios, recetas, colecciones e imágenes).
 *
 * Instalación: copiar la carpeta `demo-data/` y este archivo dentro de `backend/prisma/`.
 *
 *   cd backend
 *   npx prisma db seed                                      # catálogo de ingredientes (si no está)
 *   npx ts-node prisma/load-demo-data.ts                    # carga todo y sube las imágenes a S3
 *   npx ts-node prisma/load-demo-data.ts --skip-images      # sin S3: carga los datos sin imágenes
 *   npx ts-node prisma/load-demo-data.ts --reset            # borra los datos de demo y los vuelve a cargar
 *
 * Es idempotente: los ids salen de un hash del slug, así que correrlo dos veces no duplica nada.
 * Los usuarios de demo tienen auth0Sub "demo|<handle>": aparecen en la app pero no pueden iniciar sesión.
 * Usa DATABASE_URL y las variables AWS_* del .env del backend.
 */
import { PrismaClient } from '@prisma/client';
import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { extname, join } from 'node:path';
import { stableIngredientId } from './seed';

interface DemoUser { handle: string; name: string; email: string; avatarUrl?: string }
interface DemoRecipe {
  slug: string; author: string; title: string; description: string;
  category: string; time: number; timeUnit: string; difficulty: string; servings: number;
  ingredients: { name: string; amount: string; unit: string }[];
  steps: string[]; images?: string[];
}
interface DemoCollection {
  slug: string; owner: string; name: string; accentColor: string; cover?: string; recipes: string[];
}
interface DemoData { users: DemoUser[]; recipes: DemoRecipe[]; collections: DemoCollection[] }

/** Carga backend/.env sin depender de dotenv (las variables ya definidas tienen prioridad). */
function loadEnv(): void {
  const path = join(__dirname, '..', '.env');
  if (!existsSync(path)) return;
  for (const line of readFileSync(path, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}
loadEnv();

const DIR = join(__dirname, 'demo-data');
const args = process.argv.slice(2);
const SKIP_IMAGES = args.includes('--skip-images');
const RESET = args.includes('--reset');
const CONTENT_TYPES: Record<string, string> = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };

/** Mismo esquema que stableIngredientId del seed: UUID v5-like a partir de un texto. */
function stableId(kind: string, slug: string): string {
  const bytes = createHash('sha1').update(`zest:demo:${kind}:${slug}`).digest().subarray(0, 16);
  bytes[6] = (bytes[6] & 0x0f) | 0x50;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const h = bytes.toString('hex');
  return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
}

function s3Client(): { client: S3Client; bucket: string } | null {
  if (SKIP_IMAGES) return null;
  const { AWS_S3_BUCKET, AWS_S3_REGION } = process.env;
  if (!AWS_S3_BUCKET || !AWS_S3_REGION) {
    throw new Error('Faltan AWS_S3_BUCKET / AWS_S3_REGION en el .env. Usá --skip-images para cargar sin imágenes.');
  }
  return { client: new S3Client({ region: AWS_S3_REGION }), bucket: AWS_S3_BUCKET };
}

async function upload(s3: ReturnType<typeof s3Client>, file: string, key: string): Promise<void> {
  if (!s3) return;
  const path = join(DIR, file);
  if (!existsSync(path)) throw new Error(`No existe la imagen ${file}`);
  await s3.client.send(new PutObjectCommand({
    Bucket: s3.bucket, Key: key, Body: readFileSync(path),
    ContentType: CONTENT_TYPES[extname(file).toLowerCase()] ?? 'image/jpeg',
  }));
}

function keyFor(prefix: 'recipes' | 'collections', kind: string, slug: string, file: string): string {
  const ext = extname(file).toLowerCase().replace('.jpeg', '.jpg');
  return `${prefix}/${stableId(kind, slug)}${ext}`;
}

async function main(): Promise<void> {
  const data = JSON.parse(readFileSync(join(DIR, 'seed-data.json'), 'utf8')) as DemoData;
  const prisma = new PrismaClient();
  const s3 = s3Client();

  const userIds = new Map(data.users.map((u) => [u.handle, stableId('user', u.handle)]));
  const recipeIds = new Map(data.recipes.map((r) => [r.slug, stableId('recipe', r.slug)]));

  try {
    const known = new Set((await prisma.ingredient.findMany({ select: { id: true } })).map((i) => i.id));
    if (known.size === 0) throw new Error('El catálogo de ingredientes está vacío: corré primero `npx prisma db seed`.');

    if (RESET) {
      const rIds = [...recipeIds.values()];
      const uIds = [...userIds.values()];
      await prisma.$transaction([
        prisma.collection.deleteMany({ where: { ownerId: { in: uIds } } }),
        prisma.collectionRecipe.deleteMany({ where: { recipeId: { in: rIds } } }),
        prisma.recipeImage.deleteMany({ where: { recipeId: { in: rIds } } }),
        prisma.recipeStep.deleteMany({ where: { recipeId: { in: rIds } } }),
        prisma.recipeIngredient.deleteMany({ where: { recipeId: { in: rIds } } }),
        prisma.recipe.deleteMany({ where: { id: { in: rIds } } }),
        prisma.user.deleteMany({ where: { id: { in: uIds } } }),
      ]);
      console.log('Datos de demo anteriores borrados.');
    }

    for (const u of data.users) {
      const id = userIds.get(u.handle)!;
      await prisma.user.upsert({
        where: { id },
        update: { name: u.name, email: u.email, avatarUrl: u.avatarUrl ?? null },
        create: { id, auth0Sub: `demo|${u.handle}`, name: u.name, email: u.email, emailVerified: true, avatarUrl: u.avatarUrl ?? null },
      });
    }
    console.log(`✔ ${data.users.length} usuarios`);

    for (const r of data.recipes) {
      const id = recipeIds.get(r.slug)!;
      const authorId = userIds.get(r.author);
      if (!authorId) throw new Error(`La receta ${r.slug} tiene un autor desconocido: ${r.author}`);
      const ingredients = r.ingredients.map((i) => {
        const ingredientId = stableIngredientId(i.name);
        if (!known.has(ingredientId)) throw new Error(`Ingrediente fuera del catálogo en ${r.slug}: "${i.name}"`);
        return { ingredientId, amount: i.amount, unit: i.unit as never };
      });
      const images = r.images ?? [];
      const keys = images.map((file, n) => keyFor('recipes', 'recipe-image', `${r.slug}-${n}`, file));
      for (const [n, file] of images.entries()) await upload(s3, file, keys[n]);

      const fields = {
        authorId, title: r.title, description: r.description,
        category: r.category as never, time: r.time, timeUnit: r.timeUnit as never,
        difficulty: r.difficulty as never, servings: r.servings,
      };
      await prisma.$transaction([
        prisma.recipe.upsert({ where: { id }, update: fields, create: { id, ...fields } }),
        prisma.recipeIngredient.deleteMany({ where: { recipeId: id } }),
        prisma.recipeStep.deleteMany({ where: { recipeId: id } }),
        prisma.recipeImage.deleteMany({ where: { recipeId: id } }),
        prisma.recipeIngredient.createMany({ data: ingredients.map((i) => ({ recipeId: id, ...i })) }),
        prisma.recipeStep.createMany({ data: r.steps.map((text, n) => ({ recipeId: id, stepNumber: n + 1, text })) }),
        ...(s3 ? [prisma.recipeImage.createMany({ data: keys.map((s3Key) => ({ recipeId: id, s3Key })) })] : []),
      ]);
    }
    console.log(`✔ ${data.recipes.length} recetas${s3 ? ' con imágenes' : ' (sin imágenes)'}`);

    for (const c of data.collections) {
      const id = stableId('collection', c.slug);
      const ownerId = userIds.get(c.owner);
      if (!ownerId) throw new Error(`La colección ${c.slug} tiene un dueño desconocido: ${c.owner}`);
      let coverImageKey: string | null = null;
      if (c.cover && s3) {
        coverImageKey = keyFor('collections', 'collection-cover', c.slug, c.cover);
        await upload(s3, c.cover, coverImageKey);
      }
      const recipeLinks = c.recipes.map((slug) => {
        const recipeId = recipeIds.get(slug);
        if (!recipeId) throw new Error(`La colección ${c.slug} referencia una receta desconocida: ${slug}`);
        return { collectionId: id, recipeId };
      });
      await prisma.$transaction([
        prisma.collection.upsert({
          where: { id },
          update: { ownerId, name: c.name, accentColor: c.accentColor, coverImageKey },
          create: { id, ownerId, name: c.name, accentColor: c.accentColor, coverImageKey },
        }),
        prisma.collectionRecipe.deleteMany({ where: { collectionId: id } }),
        prisma.collectionRecipe.createMany({ data: recipeLinks }),
      ]);
    }
    console.log(`✔ ${data.collections.length} colecciones`);
  } finally {
    await prisma.$disconnect();
  }
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? `✘ ${error.message}` : error);
  process.exitCode = 1;
});
