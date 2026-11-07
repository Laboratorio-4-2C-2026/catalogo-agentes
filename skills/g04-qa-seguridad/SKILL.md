---
name: g04-qa-seguridad
description: 'Revisión de seguridad del código de un PR o módulo de una app NestJS y React con Firebase Auth: autenticación, permisos por usuario, validación de entradas, secretos y exposición de datos. Usar para revisar un PR sensible o auditar un módulo sin atacar la app en ejecución.'
metadata:
  tipo: skill
  area:
  - qa
  - seguridad
  fase:
  - revision
  - testing
  tecnologias:
  - nestjs
  - firebase
  - react
  - prisma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados:
  - g08-security-reviewer
---

# QA de seguridad

Auditoría de lectura del código. Para probar la app corriendo, usar `g04-pentesting`.

## Checklist

**Autenticación**
- Todo endpoint pasa por el guard global, y cada `@Public()` está justificado.
- El ID token de Firebase se verifica en el servidor. No se confía en un `userId` que venga del cliente.

**Permisos**
- Cada lectura o escritura filtra por el dueño del recurso. Es el fallo más probable: cambiar el id de un vehículo no debe dar acceso a uno ajeno.
- Los endpoints internos usan un secreto propio, comparado de forma segura.

**Entradas**
- DTOs con `class-validator`, con `whitelist` para evitar asignación masiva.
- Sin SQL armado a mano con datos del usuario; `$queryRaw` solo con parámetros.
- Subidas de archivos: tipo, tamaño y ruta controlados.

**Salidas**
- Las respuestas no incluyen campos internos ni datos de otros usuarios.
- Los errores no filtran stack traces, y los logs no guardan tokens ni datos personales.

**Secretos y configuración**
- Sin secretos en el repo ni en el bundle: revisar las variables `VITE_`, que son públicas.
- CORS limitado a orígenes conocidos, y permisos mínimos en workflows.
- Reglas de Firebase Storage restringidas.

**Frontend**
- Sin `dangerouslySetInnerHTML` con datos del usuario.
- Ocultar un botón no es control de acceso: el backend lo tiene que validar.

## Flujo

1. Definir el alcance: PR o módulo.
2. Leer el código siguiendo cada dato desde la entrada hasta la base.
3. Confirmar cada hallazgo en el código. Lo que no se puede confirmar se marca como "a verificar".
4. Clasificar por impacto y facilidad de explotación: crítica, alta, media o baja.

## Reglas

- Solo lectura. Publicar comentarios únicamente con autorización.
- Si aparece un secreto real, no copiarlo en la salida: indicar dónde está y recomendar rotarlo.
- Decir qué no se revisó: esto no certifica que la app sea segura.

## Ejemplo de uso
**Pedido:** Hacé QA de seguridad del módulo de vehículos.

**Resultado:** Hallazgos con archivo y línea, severidad, escenario de explotación y arreglo concreto, más lo que se revisó sin problemas y lo que no se pudo verificar.
