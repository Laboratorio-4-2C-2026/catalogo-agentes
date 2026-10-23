---
name: g03-javascript-typescript-vitest
description: 'Buenas prácticas para tests de JavaScript y TypeScript con Vitest: estructura, mocks con vi e imports explícitos, adaptadas a un backend que no usa globals. Usar al escribir o corregir tests con Vitest.'
metadata:
  tipo: skill
  area:
  - backend
  - qa
  fase:
  - testing
  tecnologias:
  - vitest
  - typescript
  - javascript
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
  - nombre: Julieta Iglesias
    github: JuliIglesias
  responsables:
  - mPiccinini
  madurez: experimental
  relacionados: []
---
### Test Structure
- Name test files with `.test.ts` or `.test.js` suffix
- Place test files next to the code they test or in a dedicated `__tests__` directory
- Use descriptive test names that explain the expected behavior
- Use nested describe blocks to organize related tests
- Follow the pattern: `describe('Component/Function/Class', () => { it('should do something', () => {}) })`
- Import what you use explicitly: `import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'` — unlike some Jest setups, these are not global here.

### Effective Mocking
- Mock external dependencies (APIs, databases, etc.) to isolate your tests
- Use `vi.mock()` for module-level mocks
- Use `vi.spyOn()` for specific function mocks
- Use `mockImplementation()` or `mockReturnValue()` on the resulting mock to define its behavior
- Reset mocks between tests with `vi.resetAllMocks()` in `afterEach`

### Testing Async Code
- Always return promises or use async/await syntax in tests
- Use `resolves`/`rejects` matchers for promises
- Set a per-test timeout with the third argument to `it()`/`test()` (`it('...', async () => {}, 10000)`), or globally with `vi.setConfig({ testTimeout: ms })`

### Snapshot Testing
- Use snapshot tests for UI components or complex objects that change infrequently
- Keep snapshots small and focused
- Review snapshot changes carefully before committing

### Testing React Components
- Use React Testing Library over Enzyme for testing components
- Test user behavior and component accessibility
- Query elements by accessibility roles, labels, or text content
- Use `userEvent` over `fireEvent` for more realistic user interactions

## Common Vitest Matchers
- Basic: `expect(value).toBe(expected)`, `expect(value).toEqual(expected)`
- Truthiness: `expect(value).toBeTruthy()`, `expect(value).toBeFalsy()`
- Numbers: `expect(value).toBeGreaterThan(3)`, `expect(value).toBeLessThanOrEqual(3)`
- Strings: `expect(value).toMatch(/pattern/)`, `expect(value).toContain('substring')`
- Arrays: `expect(array).toContain(item)`, `expect(array).toHaveLength(3)`
- Objects: `expect(object).toHaveProperty('key', value)`
- Exceptions: `expect(fn).toThrow()`, `expect(fn).toThrow(Error)`
- Mock functions: `expect(mockFn).toHaveBeenCalled()`, `expect(mockFn).toHaveBeenCalledWith(arg1, arg2)`

## Using This With Any Agent

Nothing in this file assumes Claude specifically — it's plain markdown with no tool syntax baked in. Point your agent at it directly: reference it from your agent's own project-instructions file (`AGENTS.md` for Codex CLI, `GEMINI.md` for Gemini CLI, or the equivalent for whatever you use), or just name the file path in your prompt. Works the same in Codex, Gemini, Claude, or no agent at all — reading it yourself.

## Ejemplo de uso

**Pedido:** "Este test usa jest.fn() y falla, ¿cómo lo paso a Vitest?"

**Resultado:** El test reescrito con vi.fn(), los imports explícitos desde vitest y la explicación de cada cambio.
