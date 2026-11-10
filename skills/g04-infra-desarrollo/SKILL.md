---
name: g04-infra-desarrollo
description: 'Configura y repara la infraestructura de desarrollo de un monorepo con Turborepo: Docker Compose, variables de entorno, scripts, hooks y CI de GitHub Actions, reutilizando lo que trae el template. Usar para problemas de entorno, onboarding o cambios en el pipeline de desarrollo.'
metadata:
  tipo: skill
  area:
  - devops
  fase:
  - desarrollo
  - mantenimiento
  tecnologias:
  - turborepo
  - docker
  - github-actions
  - prisma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - martinbarreiroo
  madurez: experimental
  relacionados: []
---

# Infra de desarrollo

Mantiene un entorno que cualquier integrante puede levantar y un CI confiable. No cubre el deploy a producción.

## Antes de tocar

1. Leer `AGENTS.md`, README, `docs/`, `turbo.json`, `docker-compose`, `.github/workflows` y los `package.json`.
2. Usar el gestor de paquetes y las herramientas que el repo ya define. Si el template ya lo resuelve, no se pide trabajo nuevo ni otra herramienta.

## Flujo

1. **Reproducir** el problema o definir el cambio. Para el CI, leer el log real con `gh run view --log-failed`.
2. **Ubicar la capa:** dependencias, variables, base de datos, cliente de Prisma generado, caché de Turborepo o workflow.
3. **Hacer el cambio mínimo**, reutilizando scripts existentes. El CI debe correr los mismos comandos que se corren localmente.
4. **Mantener alineado:** si cambia una variable, actualizar `.env.example`, la documentación y el workflow.
5. **Probar desde cero:** clon limpio o sin `node_modules`, base levantada, migraciones, `dev`, y los checks de formato, lint, tipos, tests y build.

## Reglas

- **Secretos:** nunca en el repo ni en los logs. En `.env.example` van nombres y valores de ejemplo; en CI, GitHub Secrets con permisos mínimos.
- No usar credenciales de producción en desarrollo ni en CI.
- No hacer resets de base, borrar volúmenes ni matar procesos ajenos sin autorización.
- Fijar versiones de actions y de herramientas en lugar de usar `latest`.
- Si no se pudo probar el workflow en GitHub, decirlo.

## Ejemplo de uso
**Pedido:** El CI falla al generar Prisma y a los devs nuevos no les levanta la base.

**Resultado:** Reproduce los dos problemas, corrige la configuración, actualiza la documentación de setup y comprueba que el entorno arranca desde cero y que el CI pasa.
