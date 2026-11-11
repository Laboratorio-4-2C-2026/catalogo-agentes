---
name: g09-revisar-infraestructura
description: Revisa Terraform y la configuración de los ambientes de Zervi, su coherencia con la aplicación y los recursos administrados fuera del state. Usar para detectar drift y riesgos de configuración; la verificación de una publicación concreta pertenece al verificador de despliegue.
metadata:
  tipo: skill
  area:
  - devops
  - seguridad
  fase:
  - revision
  tecnologias:
  - terraform
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados: []
---
# Revisión de Terraform y ambientes

Evaluá si la infraestructura declarada y la configuración del ambiente son consistentes, reproducibles y compatibles con la aplicación. La revisión no aplica cambios.

## Entrada y preparación

Recibí ambiente, alcance (estático o con contraste remoto), revisión de aplicación y, si existe, un plan o diff a revisar. Si no se especifica ambiente, hacé primero revisión estática y dejá pendiente el contraste remoto; no elijas una cuenta por coincidencia de nombres.

Leé completo el runbook de despliegue (`docs/RUNBOOK_DEPLOY_MAIN.md` del repositorio de aplicación), las instrucciones aplicables y el README de infraestructura (`infrastructure-updated/README.md` del workspace de infraestructura). Revisá luego HCL, `.terraform.lock.hcl`, ejemplos públicos y configuración consumida por el código objetivo. El runbook conserva reglas operativas, pero sus SHA, IDs, migraciones y estados fechados deben contrastarse con la evidencia actual. Si la documentación se contradice, exponé el conflicto y su impacto.

El directorio de referencia es `zervi/infrastructure-updated`; no asumas que un ejemplo con `cd infrastructure` identifica el directorio real. No ejecutes scripts de deploy preservados ni cargues archivos de shell de credenciales como parte de una lectura estática.

## Revisión

1. Identificá root, módulos, providers y versiones fijadas, lockfile, variables, flags de habilitación, outputs y backend de estado. Relevá cómo se separan ambientes, cuentas y proyectos; no supongas que existe un workspace por ambiente.
2. Mapeá recurso → ambiente → propietario → administración (Terraform, proveedor/CLI u otro mecanismo). La ausencia de un recurso fuera de Terraform no es automáticamente un defecto ni su inclusión implica que esté importado.
3. En Zervi, comprobá el caso de Render Free fuera del state y el soporte del provider efectivamente fijado antes de proponer una importación. Conservá el antecedente Render Free (`infrastructure-updated/RENDER_FREE.md` del workspace de infraestructura) como contexto histórico. No conviertas el plan a uno pago para silenciar diferencias.
4. Revisá Neon (proyecto/branch, región, SSL, versión y recuperación), Pages (proyecto, producción y Direct Upload), R2 (bucket y acceso), Render (servicio, rama, runtime, puerto y health), Auth0 y CORS en las partes que existan. No supongas que Terraform administra todas esas integraciones.
5. Compará nombres de variables y contratos con el código de la revisión elegida. Las variables VITE son públicas y se incorporan al build; configurar Pages no reescribe un bundle existente. Verificá que los recursos con sufijo fijo `dev` no se compartan accidentalmente al cambiar `environment`.
6. Revisá secretos en definición/outputs y protección del state sin imprimir valores. No vuelques `.env`, tfvars privados, state ni JSON de planes completos en el informe. Un output marcado sensible puede seguir guardándose en state.
7. Si hay herramientas disponibles, usá `terraform fmt -check -recursive` y `terraform validate` con dependencias ya preparadas. Si faltan, informá qué no pudo verificarse o prepará una copia aislada sin migrar state, actualizar providers ni tocar el checkout del usuario. No uses `init -upgrade` como parte de una revisión.
8. Para contraste remoto, verificá identidad/ambiente y usá consultas de lectura. Un `plan` normal puede consultar recursos y generar información sensible: ejecutalo solo para el ambiente identificado, con credenciales por el mecanismo establecido y salida privada redactada. Si no se puede, revisá el plan aportado y marcá el drift como no comprobado.
9. Interpretá `plan -detailed-exitcode`: 0 sin diferencias propuestas, 2 con diferencias que requieren evaluación, 1 error. Diferenciá drift remoto, cambios deseados de configuración y falta de recursos/importación. `No changes` no acredita servicios fuera del state ni funcionamiento de la aplicación.

## Hallazgos y salida

Abrí con la conclusión: coherente, con hallazgos o revisión parcial. Registrá fecha, ambiente, revisión, versiones y alcance de consultas. Entregá inventario de recursos/administradores y hallazgos priorizados:

| Prioridad | Recurso / archivo | Evidencia | Impacto | Corrección propuesta | Validación pendiente |
| --- | --- | --- | --- | --- | --- |

Separá errores reproducibles, diferencias deliberadas documentadas y mejoras opcionales. Para cada hallazgo mostrale al usuario la referencia concreta y el mecanismo del impacto. Incluí checks ejecutados, resultados y bloqueos de acceso; no presentes ausencia de acceso como un error del ambiente.

## Límites y aceptación

No ejecuta apply, destroy, import, refresh que persista cambios, migración de state, rotación de secretos ni modificaciones de planes/recursos. Una recomendación de corrección no la autoriza. Tampoco dispara despliegues ni rollback.

La revisión está completa cuando identifica qué administra cada mecanismo, comprueba contratos relevantes y deja claro qué evidencia es estática, remota o pendiente. Para declarar ausencia de drift, exigí contraste actual del alcance administrado; no alcanza con HCL válido.

## Ejemplo de uso

**Pedido:** Revisá estáticamente el Terraform y la configuración del ambiente indicado; identificá qué recursos administra y qué queda fuera del state.

**Resultado:** Un inventario de recursos y administradores, checks disponibles y hallazgos con evidencia; el drift remoto queda pendiente sin contraste actual.
