---
name: g14-generador-de-datos-de-prueba
description: Genera datos semilla SQL realistas y referencialmente consistentes para Supabase/PostgreSQL (usuarios, perfiles, publicaciones, imágenes, zonas desde una API pública) a partir del esquema documentado, con IDs fijos legibles y verificación al pie. Usala cuando QA o dirección necesita cargar un golden set o una demo del motor sin escribir la migración del producto.
metadata:
  tipo: skill
  area:
  - qa
  - datos
  fase:
  - testing
  tecnologias:
  - postgresql
  - supabase
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "14"
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: usado-en-proyecto
  relacionados: []
---

# Generador de datos de prueba

Un motor de matching no se demuestra con una base vacía, ni con mil filas clonadas. **El realismo importa más que el volumen**: diez publicaciones bien distribuidas demuestran el motor.

## Frontera (Regla de cátedra)

Dirección produce **el dataset** (archivo `.sql` de datos de prueba o un CSV curado). **La migración o semilla versionada del repo de producto la escribe un dev.** Si al generar aparece la tentación de escribir la migración, pará y preguntá.

## Antes de generar

1. Leé el esquema documentado (en VaiVen, `ai-config/docs/datos/esquema.md`) y las migraciones de `origin/main` del repo de producto: tablas, enums, únicos, estados y transiciones. Anotá el commit contra el que es compatible.
2. Leé los triggers que dispara un `INSERT`. En VaiVen, cada `INSERT` en `publicaciones` avisa al motor y lo juzga contra **todo** el lado complementario: por eso la carga va en **dos archivos y en orden** (primero necesidades, esperar que terminen las ejecuciones; después donaciones). Juntos, cada par se juzga y se paga dos veces.
3. Las listas cerradas **no se inventan**: categorías y zonas salen del contrato o de la fuente oficial (zonas de Georef con `generar-semilla-zonas.py`).

## Forma de cada archivo

1. **Encabezado**: precondiciones (`supabase db reset`, secretos que el reset borra), qué esperar después y la convención de IDs.
2. Todo entre `begin;` y `commit;`.
3. **Limpieza**: `delete` de las tablas que toca y de los usuarios del dominio de prueba (`%@golden.<dominio>`).
4. **Usuarios**: uno por publicación cuando el motor usa datos del autor o excluye al propio usuario. Mismo patrón de `auth.users` + `auth.identities` que la semilla del repo; el perfil lo crea el trigger.
5. **Perfiles**: `update` solo de los campos que el caso define (avatar, zona).
6. **Datos de negocio**: **UUID fijos que codifican el ID del caso** (`…0001NNN` necesidades, `…0002NNN` donaciones) para leer exportaciones sin tabla de cruce. Claves foráneas **por subconsulta** sobre un campo estable (`categorias.slug`, zona por región/partido/localidad), nunca por número. Vencimientos lejanos para que sobreviva a todas las corridas. Coherencia de tipo (urgencia solo en necesidades, estado del objeto solo en donaciones).
7. **Verificación al pie**: un `select count(*)` por tipo con el número esperado, y cero nulos en FKs resueltas por subconsulta.

## Distribución y texto

- Zonas en más de una región (no todo AMBA), urgencias variadas, casos con y sin avatar, imagen y zona en perfil: si todo es igual, el motor no discrimina.
- Texto en castellano rioplatense plausible: cortado, con faltas, con el dato importante al final. Nunca *lorem ipsum*.
- La IA puede redactar; un humano edita antes de congelar.

## Zonas desde Georef

`generar-semilla-zonas.py` consulta la API pública de Georef y deja un CSV curado: una fila por localidad más una por partido con localidad vacía, `region = 'AMBA'` para las 15 comunas y los 24 partidos del conurbano, deduplicación por jerarquía de Georef y `activa` solo en AMBA. Uso: `python3 generar-semilla-zonas.py [--stdout]`.

## Cómo se verifica

- Correr contra Postgres local con las migraciones de `main`, dentro de una transacción con rollback, y reportar los conteos.
- Dos corridas con la misma entrada dan el mismo dataset.
- Cargado, el motor tiene que **discriminar**: puntajes distintos. Uno referencialmente perfecto que da a todos lo mismo está mal generado.
- Declarar lo no verificado (por ejemplo, el disparo real al motor si faltaban secretos).

## Qué no hacer

- No copiar contraseñas ni claves reales en el SQL; los usuarios de prueba usan un dominio ficticio.
- No editar el archivo en el repo del dev: se corre tal cual.

Ejemplo concreto en VaiVen: `docs/qa/golden-set-v1-carga/1-necesidades.sql` y `2-donaciones.sql`, y la especificación `docs/agentes/especificaciones/11.1-generador-de-datos-de-prueba.md`.

## Ejemplo de uso

**Pedido:** Generame el SQL para cargar las 15 necesidades y 6 donaciones del golden set en la base local, con sus usuarios y fotos.

**Resultado:** Devuelve dos archivos `.sql` transaccionales (limpieza, usuarios, perfiles, publicaciones con UUID que codifican el caso, imágenes y conteos al pie), con las instrucciones de orden y de espera entre uno y otro, y el commit del esquema contra el que se verificó.
