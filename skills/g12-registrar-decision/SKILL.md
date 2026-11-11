---
name: g12-registrar-decision
description: Documenta una decisión o sesión de trabajo con contexto, alternativas y consecuencias, adaptándose al decision log o formato ADR del proyecto. Usar después de una sesión o reunión en la que se decidió, definió o encontró algo que tiene que quedar registrado.
owner: '@husseymarcos'
role: pm
created: '2026-11-05'
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g12-preparar-relevo-rol
  - g15-adr-writer
  - g15-product-adr-drafter
  - g04-arquitectura
---

# Registrar decisión

Transformar el relato y su evidencia en una entrada breve lista para registrar.
Ejemplo: `/registrar-decision PM: acordamos entregar tickets los lunes por el feedback de los devs`.

## Ubicar la sesión

Localizar el registro de decisiones, su plantilla y sus convenciones en la documentación
del proyecto. Puede ser un ADR por decisión, una bitácora de sesiones o una página
compartida. Identificar fecha, responsable real, rol si corresponde y contexto.
El owner de esta skill es su autor; no asumir que también tomó la decisión documentada.
Si faltan fecha, autor o la elección, entregar el borrador con `Por confirmar` donde
corresponda. No inventar un acuerdo ni convertir una propuesta en una decisión tomada.

Buscar entradas previas sobre el mismo tema, tanto para evitar duplicados como para
entender qué sigue vigente. Respetar la taxonomía existente. Si no hay una definida,
una sesión puede producir estos tipos de resultado:

| Tipo | Cuándo corresponde | Campos |
|---|---|---|
| Decisión | Se eligió entre opciones reales | Qué, Alternativas, Consecuencias |
| Definición | Se fijó una regla o valor | Qué, Por qué |
| Hallazgo | Se detectó algo aún no resuelto | Qué encontramos, Qué implica |
| Pendiente | Quedó una pregunta abierta | Pregunta, Dueño |

Usar sólo alternativas y motivos respaldados por el relato o las fuentes. Omitir campos
que no aporten; no rellenar con `ninguna`. Consecuencias inciertas se expresan como
expectativas o riesgos. El desglose de tareas permanece en su tracker o documento.

## Redactar

Usar el formato existente, incluidos estados y numeración si los tiene. Si no existe
plantilla, proponer este formato para una sesión; para un ADR individual, usar contexto,
decisión, alternativas, consecuencias y estado respaldado por la evidencia:

```markdown
### YYYY-MM-DD — Título de la sesión

- **Owner:** @autor-de-la-sesion
- **Contexto:** Hecho o restricción que motivó el trabajo.

#### Decisión — Título

- **Qué:** Elección y compromiso asumido.
- **Alternativas:** Opciones realmente consideradas.
- **Consecuencias:** Efectos y compromisos resultantes.
```

Si hay un solo resultado, aplanarlo: poner su tipo en el título y sus campos directamente
bajo el contexto. Enlazar tickets, ADR o evidencia cuando aclaren la causa o el alcance.
Conservar trazabilidad entre versiones. Si una decisión reemplaza otra, enlazar ambas
y seguir la convención de reemplazo o estado del proyecto. En ausencia de convención,
conservar el contenido anterior y agregar una referencia a la decisión nueva. Si la
elección todavía está pendiente, registrarla como propuesta o pregunta abierta.

## Entrega o registro

Devolver el contenido listo para copiar, el destino propuesto y los datos por
confirmar. Antes de registrar, comprobar que cada afirmación provenga del relato o de
una fuente, que la autoría sea correcta y que la entrada no duplique otra existente.

Si el usuario pidió escribir y los permisos lo permiten, usar la ubicación y unidad
de registro del proyecto: entrada, archivo ADR o página. Preservar el historial conforme
a su convención. Ante cambios concurrentes, releer antes de insertar. En repositorios de sólo lectura entregar el texto
o un archivo fuera de ellos. Publicar en GitHub o hacer push sólo si se pidió.

## Ejemplo de uso

**Pedido:** /registrar-decision PM: acordamos entregar tickets los lunes por el feedback de los devs

**Resultado:** Devuelve la entrada lista para pegar en el decision log del proyecto, con contexto, alternativas y consecuencias, y marca "Por confirmar" lo que el relato no respalda.
