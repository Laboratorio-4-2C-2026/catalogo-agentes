---
name: g09-zervi-project-hub
description: "Audita o prepara actualizaciones del hub o Linktree de Zervi: reúne enlaces y propone botones con fuentes, audiencia y permisos explícitos."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  tipo: skill
  area: [gestion, documentacion]
  fase: [revision, mantenimiento]
  tecnologias: [agnostico]
  metodologia: [agnostico]
  herramientas: [otra]
  requiere: []
  grupo: "09"
  autor:
    nombre: Bruno Iacovone
    github: BrunoIacovone
  responsables: [BrunoIacovone]
  madurez: usado-en-proyecto
  relacionados: []
---

## Activación

Activa para auditar o preparar actualizaciones del hub de Zervi, incluida la invocación `g09-zervi-project-hub` o el nombre original `zervi-project-hub`. Mantener significa proponer cambios, sin ejecución recurrente.

## Reglas obligatorias

- Lee [la guía](references/guide.md). Entrega borrador en chat; escrituras, publicación, documentos, compartición y tickets requieren autorización explícita y acotada.
- Separa inventario interno y botones. Exige aprobación de URL, texto y parámetros para la audiencia real. Enlaces restringidos requieren autorización del responsable y aviso; publicarlos no concede acceso. Excluye lo desconocido.
- Separa identidad, URL exacta, HTTP y permiso de audiencia: 200/login no prueba acceso. No pidas contraseñas ni accedas a secretos; no expongas tokens, URLs firmadas o parámetros sensibles.
- Comprueba solo con entorno, método y alcance autorizados. No cambies visibilidad, rastrees sin límite, actives endpoints operativos ni sondees backend/health/Render.
- Jira reciente no sustituye alcance aprobado del Charter. Separa línea base, cambios autorizados, trabajo y despliegue.
- No inventes hechos ni aprobaciones. Registra procedencia, versión, ambiente y corte; las verificaciones históricas no son actuales.

## Decisiones

| Condición | Acción |
|---|---|
| Sin conectores/acceso | Usa datos pegados; distingue inaccesible, no revisado y faltante de ausencia. |
| Conflicto/autoridad desconocida | Expón evidencia; solicita decisión. |
| Publicación sin aprobar | Pendiente interno, fuera del bloque copiable. |
| Redirección/enlace corto/secreto | Aplica controles; no publiques destinos inciertos o sensibles. |

## Pasos

1. Registra audiencia, fuentes y autorización; acepta datos pegados y pide solo las URLs o decisiones necesarias.
2. Recopila evidencia permitida; normaliza, clasifica y detecta redundancias según el procedimiento.
3. Valida identidad, vigencia y permisos por separado; aplica la lista de control.

## Salida

Entrega en orden:
1. Inventario interno.
2. Bloque independiente de botones aprobados (o ninguno).
3. Pendientes con fuente/responsable conocido.
4. Cambios propuestos frente al corte anterior, límites y decisiones abiertas.

## Referencias

- [Procedimiento, entradas y formato](references/guide.md).

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-project-hub sin consultar servicios. E1 identifica una demo pública en `https://example.org/demo`; A1 aprueba para visitantes anónimos esa URL, título «Demo académica» y descripción «Recorrido de publicación». E2 identifica un repositorio privado sin aprobación de divulgación.

**Resultado:** Botón aprobado según A1: «Demo académica» — `https://example.org/demo` — «Recorrido de publicación». Mantiene E2 solo en el inventario interno y solicita aprobación separada; declara revisión documental, sin publicación ni cambios de permisos.
