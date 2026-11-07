---
name: g04-dependency-version-control
description: 'Controla las dependencias de un monorepo: decide si agregar una, revisa versiones y vulnerabilidades, y actualiza de a una con lockfile y checks. Usar al agregar o actualizar paquetes, al resolver conflictos de versiones o ante una alerta de seguridad.'
metadata:
  tipo: skill
  area:
  - devops
  - seguridad
  fase:
  - desarrollo
  - mantenimiento
  tecnologias:
  - nodejs
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - martinbarreiroo
  madurez: experimental
  relacionados:
  - g11-plan-actualizacion
---

# Dependency version control

Mantiene las dependencias al día y bajo control, con el menor riesgo posible.

## Antes de agregar una dependencia

1. ¿Ya lo resuelve algo instalado o la plataforma? Si son pocas líneas, no se agrega.
2. Revisar la lista de dependencias prohibidas del proyecto (`forbidden_dependencies` en `team.yaml`).
3. Evaluar mantenimiento, licencia, tamaño y si se usa en el navegador. Confirmar el nombre exacto del paquete para evitar typosquatting.

## Revisar

Usar el gestor de paquetes que define el repo (`packageManager`, lockfile):

- `outdated` para ver qué versiones hay.
- `audit` para vulnerabilidades, indicando si afectan a producción o solo al desarrollo.
- Misma dependencia con versiones distintas entre workspaces.

## Actualizar

1. **De a una**, o por grupos que van juntos (por ejemplo, los paquetes de `@nestjs/*`). Sin mezclar con otras tareas.
2. **Leer las notas de la versión** en la documentación actual. Si es major, listar qué cambia para el proyecto antes de tocar nada.
3. Instalar con el gestor del repo y commitear el lockfile. Nunca editarlo a mano ni borrarlo para resolver un conflicto.
4. Si cambian herramientas generadas (como Prisma), regenerar.
5. Correr formato, lint, tipos, tests y build en la raíz, y probar el flujo afectado.
6. Si falla, arreglar o revertir esa actualización, y documentar el motivo.

## Salida

Tabla: paquete | de | a | tipo | cambios relevantes | checks. Y lo que quedó sin actualizar, con el motivo.

## Reglas

- No correr `audit fix --force`: puede subir majors sin aviso.
- Una vulnerabilidad se evalúa según si el código vulnerable se alcanza; no se oculta ni se ignora sin justificarlo.
- No ejecutar scripts de instalación de paquetes dudosos: avisar y frenar.

## Ejemplo de uso
**Pedido:** ¿Podemos subir Prisma a la última versión?

**Resultado:** Lee las notas de la versión, detalla los cambios que afectan al proyecto, sube el paquete con su lockfile, corre todos los checks y devuelve un resumen, o frena si encuentra una migración riesgosa.
