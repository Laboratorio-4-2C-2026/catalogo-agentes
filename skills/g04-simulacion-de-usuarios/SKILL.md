---
name: g04-simulacion-de-usuarios
description: Simula usuarios sin conocimientos técnicos recorriendo PitStop en el navegador para encontrar fricción antes de probar con personas reales, a partir de perfiles y tareas concretas. Usar para validar un flujo nuevo o preparar pruebas con usuarios.
metadata:
  tipo: skill
  area:
  - qa
  - diseno
  fase:
  - testing
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados:
  - g11-usabilidad-sintetica
  - g11-sportmatch-sim
---

# Simulación de usuarios

Encuentra los problemas obvios de un flujo, con poco costo. **No reemplaza probar con personas reales**: las conclusiones son hipótesis y así se presentan.

## Flujo

1. **Perfiles:** de 2 a 4, según el público del producto. Ejemplos: dueña de un auto que no sabe de mecánica; alguien con dos vehículos y poco tiempo; persona mayor que usa solo el celular.
2. **Tareas:** objetivos, no instrucciones. "Querés acordarte de cuándo cambiar el aceite", no "tocá el botón Agregar".
3. **Recorrer en el navegador** en el dispositivo del perfil, con datos propios de prueba. En cada paso, registrar:
   - Qué ve y qué espera que pase.
   - Qué haría a continuación, usando solo lo que está en pantalla.
   - Lo que pasó de verdad.
4. **No usar lo que se sabe del código** ni la documentación para destrabarse. Si el perfil se traba o abandonaría, se registra y recién ahí se sigue.
5. **Clasificar:** bloquea la tarea / genera duda / detalle menor.

## Salida

Por perfil y tarea: completada o no, pasos y dudas con captura. Después, fricciones repetidas por impacto y qué conviene validar con personas reales, con preguntas para esa prueba.

## Reglas

- Ambiente de prueba y datos ficticios.
- No inventar citas ni presentar la simulación como un resultado con usuarios.
- Reportar; los arreglos los decide el equipo.

## Ejemplo de uso
**Pedido:** Simulá a tres usuarios cargando su primer vehículo y un service.

**Resultado:** Por perfil: tarea completada o no, en qué paso dudó y por qué, con capturas, más una lista de fricciones repetidas ordenadas por impacto.
