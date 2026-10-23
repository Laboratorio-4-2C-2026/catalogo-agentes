---
name: g03-supertest-api-testing
description: Patrones para tests de integración HTTP de APIs Express con TypeScript usando Supertest, repositorios falsos en memoria y verificación de autorización (401 y 403). Usar al testear endpoints de un backend Express.
metadata:
  tipo: skill
  area:
  - backend
  - qa
  fase:
  - testing
  tecnologias:
  - express
  - typescript
  - supertest
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '03'
  autor:
    nombre: Ignacio Nicolás Correa Rodríguez
    github: NachoCor2007
  responsables:
  - NachoCor2007
  madurez: experimental
  relacionados: []
---
# Skill: Express API Integration Testing with Supertest

## 1. When to Use This Skill
Apply this skill whenever:
- Writing automated HTTP integration tests for Express routes and controllers.
- Testing API response contracts, headers, and status codes (`200`, `201`, `204`, `400`, `401`, `403`, `404`).
- Testing security and permission rules with mock JWT/Cognito user tokens.
- Setting up in-memory repository doubles (fakes) to test endpoints without a live database.

---

## 2. Test Architecture: Zero Real Database

### A. In-Memory Repository Fakes
Tests must be fast, deterministic, and isolated. Never connect to a real PostgreSQL database or Docker container during test runs. 

Create typed in-memory fakes implementing domain repository interfaces:

```typescript
// Example: in-memory repository double for testing
export class FakeExpenseRepository implements ExpenseRepository {
  private items: Map<string, Expense> = new Map();

  async findById(id: string): Promise<Expense | null> {
    return this.items.get(id) ?? null;
  }

  async save(expense: Expense): Promise<void> {
    this.items.set(expense.id, expense);
  }

  async delete(id: string): Promise<void> {
    this.items.delete(id);
  }

  // Test helper to prepopulate state
  seed(expenses: Expense[]): void {
    expenses.forEach((e) => this.items.set(e.id, e));
  }
}
```

---

## 3. Supertest HTTP Integration Patterns

### A. Testing Happy Path & Correct Status Codes
Use `request(app)` from Supertest to test route handlers from the HTTP boundary down to the business service:

```typescript
import request from 'supertest';
import { createApp } from '../app';
import { FakeExpenseRepository } from './fakes/fake-expense-repository';

describe('POST /api/expenses', () => {
  it('should return 201 Created and save the expense', async () => {
    const expenseRepo = new FakeExpenseRepository();
    const app = createApp({ expenseRepo });
    const userToken = generateTestToken({ sub: 'user-123' });

    const res = await request(app)
      .post('/api/expenses')
      .set('Authorization', `Bearer ${userToken}`)
      .send({ description: 'Almuerzo', amount: 3500 });

    expect(res.status).toBe(201);
    expect(res.body).toHaveProperty('id');
    expect(res.body.description).toBe('Almuerzo');
  });
});
```

### B. Testing Zod Validation Failures (`400 Bad Request`)
Verify that invalid request bodies produce structured `400` validation errors:

```typescript
it('should return 400 when required fields are missing or invalid', async () => {
  const app = createApp();
  const token = generateTestToken({ sub: 'user-123' });

  const res = await request(app)
    .post('/api/expenses')
    .set('Authorization', `Bearer ${token}`)
    .send({ amount: -500 }); // Missing description, invalid negative amount

  expect(res.status).toBe(400);
  expect(res.body.error).toBe('BAD_REQUEST');
  expect(res.body.details).toBeDefined();
});
```

---

## 4. Mandatory Security & Authorization Tests

Every protected endpoint MUST have tests verifying identity and resource ownership:

### A. 401 Unauthorized Test (Authentication)
Verify requests without a token or with a malformed token are rejected:

```typescript
it('should return 401 when Authorization header is missing', async () => {
  const app = createApp();
  const res = await request(app).delete('/api/expenses/exp-1');

  expect(res.status).toBe(401);
  expect(res.body.message).toMatch(/token/i);
});
```

### B. 403 Forbidden Test (Resource Ownership / IDOR)
Verify an authenticated user cannot mutate or access another user's resource:

```typescript
it('should return 403 when trying to delete an expense owned by another user', async () => {
  const expenseRepo = new FakeExpenseRepository();
  expenseRepo.seed([{ id: 'exp-1', ownerId: 'user-alice', amount: 1500 }]);

  const app = createApp({ expenseRepo });
  const bobToken = generateTestToken({ sub: 'user-bob' }); // Bob tries to delete Alice's expense

  const res = await request(app)
    .delete('/api/expenses/exp-1')
    .set('Authorization', `Bearer ${bobToken}`);

  expect(res.status).toBe(403);
});
```

---

## 5. Summary Checklist for API Tests

- [ ] Route mounts through test app instance (`createApp({ fakes })`).
- [ ] Database is replaced with in-memory double (zero PostgreSQL connections).
- [ ] Happy path returns explicit status code (`200`, `201`, `204`).
- [ ] Invalid payload returns `400 Bad Request` with validation details.
- [ ] Missing token returns `401 Unauthorized`.
- [ ] Non-owner access returns `403 Forbidden`.
- [ ] Non-existent ID returns `404 Not Found`.
- [ ] No internal database stack traces leaked in error responses.

---

## 6. Using This With Any Agent

Nothing in this file assumes Claude specifically — it's plain markdown with no tool syntax baked in. Point your agent at it directly: reference it from your agent's own project-instructions file (`AGENTS.md` for Codex CLI, `GEMINI.md` for Gemini CLI, or the equivalent for whatever you use), or just name the file path in your prompt. Works the same in Codex, Gemini, Claude, or no agent at all — reading it yourself.

## Ejemplo de uso

**Pedido:** "Escribí los tests de integración de GET /events/:id."

**Resultado:** Tests con Supertest que cubren el caso exitoso, el recurso inexistente y los accesos sin token o sin permiso, usando un repositorio falso en memoria.
