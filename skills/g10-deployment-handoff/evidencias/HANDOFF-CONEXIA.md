# Handoff de Conexia: Neon, Render, Vercel y DNS

Reconstrucción preparada el 10/11/2026. Estado: documento con comprobaciones de destino pendientes; ejecución y cuentas a cargo del equipo.

## Contexto y responsabilidad

| Componente | Destino relatado | Responsable |
|---|---|---|
| PostgreSQL | Neon | Devs: base, acceso y operación |
| Backend | Render | Devs: configuración, build y arranque |
| Frontend | Vercel | Devs: proyecto y despliegue |
| DNS de conexia.net.ar | Apuntado a Vercel según el relato | Equipo con control del dominio |

La contribución de QA fue preparar instrucciones y acompañar el handoff. No implicó transferirle el ownership de los despliegues.

## Correspondencia con el código actual

| Punto a documentar | Comprobación realizada |
|---|---|
| Build backend | package.json define build = nest build |
| Arranque backend | start:prod = node dist/src/main; no reutilizar una ruta supuesta dist/main.js |
| Puerto | main.ts escucha process.env.PORT con fallback local 3000 |
| CORS | main.ts usa FRONTEND_URL para el origen principal |
| Base de datos | prisma.config.ts toma DATABASE_URL; migraciones en prisma/migrations |
| Build frontend | build = tsc -b && vite build |
| Conexión a API | El cliente usa VITE_API_BASE_URL; queda incorporada en el build |

[Extractos con líneas y hashes](FUENTES-CODIGO.md).

## Secuencia que debe contener el handoff

1. Identificar entorno, versión y responsables; confirmar proyectos y permisos en las tres plataformas.
2. Configurar acceso a la base por canal seguro y revisar las migraciones aplicables antes de autorizarlas.
3. Preparar backend con su build, arranque, puerto, configuración de Firebase y origen permitido.
4. Preparar frontend con la URL pública de API y configuración cliente; verificar sus rutas internas.
5. Usar los destinos de DNS informados por el proyecto real de Vercel, sin adivinar registros o IPs.
6. Verificar la comunicación frontend/API/base y un recorrido autorizado, además de carga desde la raíz y rutas internas.
7. Acordar versión de aplicación recuperable, configuración anterior y respaldo de datos antes de una actualización.

Se comprobó la correspondencia con scripts y código. No se consultaron ni modificaron los paneles actuales de los proveedores, y no se ejecutaron estos pasos. Los valores de conexión, destinos DNS y procedimiento de migración deben confirmarse en el entorno concreto. Esta reconstrucción no reemplaza una guía operativa actualizada para producción.
