---
name: g10-dto-validation-checker
description: Verificar que los DTOs de NestJS tengan validación (class-validator) consistente con las restricciones reales del modelo de Prisma. Usar al crear o modificar un DTO, o al revisar un PR que toca `dto/`.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - desarrollo
  - revision
  tecnologias:
  - nestjs
  - prisma
  - typescript
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-guard-auth-auditor
  - g10-migration-safety-reviewer
  - g02-input-limits-hunter
---
# DTO Validation Checker

Comparar cada DTO del backend (`backend/src/**/dto/*.dto.ts`) contra el modelo de Prisma que persiste, para detectar campos sin validar o reglas de negocio que el DTO no refleja.

## Qué revisar

1. Para cada DTO, listar sus campos y decoradores de `class-validator` (`@IsString`, `@IsOptional`, `@IsDateString`, `@IsUUID`, etc.).
2. Cruzar contra el modelo de Prisma correspondiente: todo campo obligatorio en el modelo (sin `?` ni default) debería estar validado como requerido en el DTO; todo campo opcional debería tener `@IsOptional()`.
3. Revisar reglas de negocio que no son solo de tipo, como el validador custom `arrival-after-departure.validator.ts` en `trips/dto/create-trip.dto.ts`: señalar si existe una regla equivalente para otros pares de fechas/horarios del dominio (por ejemplo horarios de `Schedule`) y no está aplicada.
4. Señalar strings sin límite de longitud (`@MaxLength`) que vayan a una columna `varchar` acotada, y números sin `@Min`/`@Max` cuando el dominio tiene un rango lógico (ej. capacidad de un `Trip`).
5. Verificar que los DTO de "update" (`update-trip.dto.ts`) no vuelvan obligatorios campos que en el de creación eran opcionales, y viceversa.

## Salida esperada

Tabla: `DTO` | `campo` | `problema` | `severidad` | `sugerencia` (qué decorador agregar). No editar los DTOs: solo reportar, salvo que el usuario pida aplicar los cambios.

## Ejemplo de uso

**Pedido:** Revisá si los DTOs de trips y travel-intents tienen toda la validación que necesitan según el schema de Prisma.
**Resultado:** Tabla con los campos sin validar o sin límites razonables, listos para corregir antes de mergear.
