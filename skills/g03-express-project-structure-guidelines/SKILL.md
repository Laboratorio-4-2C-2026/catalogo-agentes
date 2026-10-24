---
name: g03-express-project-structure-guidelines
description: Define la estructura de carpetas por recurso, la separación en capas (routes, controllers, services, repositories) y las convenciones de nombres para backends Express con TypeScript. Usar al crear un módulo nuevo o decidir dónde va un archivo.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - diseno
  - desarrollo
  tecnologias:
  - express
  - typescript
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '03'
  autor:
    nombre: Mateo Piccinini
    github: mPiccinini
  colaboradores:
  - nombre: Ignacio Nicolás Correa Rodríguez
    github: NachoCor2007
  responsables:
  - mPiccinini
  madurez: usado-en-proyecto
  relacionados: []
---
# Skill: Express.js & TypeScript Project Structure Guidelines

## 1. When to Use This Skill
Apply this skill whenever:
- Structuring a new Express.js and TypeScript project or adding a new API resource/module.
- Organizing files, defining routes, controllers, services, or validation schemas.
- Enforcing Clean Architecture, layer separation, and single-responsibility boundaries.
- Auditing file layout, import paths, or identifier naming conventions.

---

## 2. Directory Layout (Resource-Based / Modular)

Code inside `src/` must be organized strictly by **domain resources** (Modular Monolith architecture):

```text
src/
├── index.ts                 # Server entry point: port binding & graceful shutdown
├── app.ts                   # Express application setup, security middleware (CORS, Helmet) & root router
├── config/                  # Global environment & external client configurations
│   ├── env.ts               # Runtime environment validation (Zod/dotenv)
│   └── prisma.ts            # PrismaClient singleton instance & connection pool
├── middleware/              # Cross-cutting global Express middlewares
│   ├── auth.ts              # Authentication & JWT verification middleware (e.g. AWS Cognito)
│   ├── validate-request.ts  # Generic Zod validation middleware (body, params, query)
│   └── error-handler.ts     # Global centralized error handling & HTTP status mapping
└── modules/                 # Modular domain resources (high cohesion, low coupling)
    └── [resource-name]/     # e.g., events, expenses, participants, users
        ├── routes.ts        # Resource HTTP route declarations with chained middlewares
        ├── controller.ts    # Lean request handlers: extract input, call service, send response
        ├── service.ts       # Core business logic, validation rules, and data access orchestration
        ├── validators.ts    # Zod schemas for request payload and query validation
        └── types.ts         # Module-specific interfaces, DTOs, and inferred types
```

---

## 3. Layer Responsibilities & Data Flow

### A. Routes (`routes.ts`)
- **Responsibility:** Define HTTP methods and URL paths.
- **Rules:** 
  - Attach necessary middlewares (`auth`, `validateRequest(schema)`).
  - Wrap all async controller calls in `asyncHandler`.
  - ❌ **NEVER** write business logic, authorization `if` checks, or database calls inside route files.

### B. Controllers (`controller.ts`)
- **Responsibility:** Act as the HTTP adapter.
- **Rules:**
  - Extract parameters (`req.params`, `req.body`, `req.user`).
  - Delegate execution to domain services.
  - Return clean HTTP responses (`res.status(200).json(result)` or `res.status(204).send()`).
  - ❌ **NEVER** instantiate Prisma or execute raw SQL directly in controllers.

### C. Services (`service.ts`)
- **Responsibility:** Encapsulate business logic, domain invariants, and data operations.
- **Rules:**
  - Verify resource ownership and access authorization (`resource.userId === authUserId`).
  - Throw typed domain errors (`NotFoundError`, `ForbiddenError`, `BadRequestError`).
  - Execute multi-table updates within database transactions (`prisma.$transaction`).

### D. Validators (`validators.ts`) & Types (`types.ts`)
- **Responsibility:** Enforce runtime payload integrity and compile-time type safety.
- **Rules:**
  - Define Zod schemas matching incoming request shapes.
  - Export inferred types using `z.infer<typeof schema>`.
  - ❌ **NEVER** trust client data with type assertions (`as MyType`) without runtime validation.

---

## 4. Naming Conventions

- **Files & Folders:** Strictly `kebab-case` (e.g., `event-service.ts`, `validate-request.ts`).
- **Interfaces, Types & Classes:** `PascalCase` (e.g., `CreateEventInput`, `AuthUserPayload`).
- **Functions, Methods & Variables:** `camelCase` (e.g., `getEventById`, `expenseAmount`).
- **Constants & Env Variables:** `UPPERCASE` (e.g., `DATABASE_URL`, `COGNITO_USER_POOL_ID`).

---

## 5. Anti-Patterns to Avoid

- ❌ **Layer Bleed:** Importing `PrismaClient` directly in controllers or routes.
- ❌ **Flat Architecture:** Putting all routes in one massive file or all services in a flat global directory.
- ❌ **Missing Async Error Catching:** Writing async route handlers without `asyncHandler` or `try/catch(next)`.
- ❌ **Hardcoded Configuration:** Reading `process.env.VAR` randomly throughout files instead of centralized `src/config/env.ts`.

---

## 6. Using This With Any Agent

Nothing in this file assumes Claude specifically — it's plain markdown with no tool syntax baked in. Point your agent at it directly: reference it from your agent's own project-instructions file (`AGENTS.md` for Codex CLI, `GEMINI.md` for Gemini CLI, or the equivalent for whatever you use), or just name the file path in your prompt. Works the same in Codex, Gemini, Claude, or no agent at all — reading it yourself.

## Ejemplo de uso

**Pedido:** "¿Dónde pongo la lógica para invitar participantes a un evento?"

**Resultado:** La ubicación de cada parte (ruta, controlador, servicio, repositorio) dentro del módulo correspondiente, con el motivo de cada decisión.
