---
name: g04-stress-testing
description: Prueba de estrés de la API NestJS para encontrar a qué carga se degrada, cómo falla y si se recupera, en un entorno local o de prueba aislado. Usar cuando se pide conocer el límite del sistema; para validar la carga esperada, usar load testing.
metadata:
  tipo: skill
  area:
  - qa
  - backend
  fase:
  - testing
  tecnologias:
  - nestjs
  - k6
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
  relacionados: []
---

# Stress testing

Responde: **¿dónde está el límite, cómo falla y se recupera sola?** A diferencia del load testing, acá se busca pasarse de la carga prevista.

## Seguridad

Correr solo contra el entorno local o un ambiente de prueba propio, con autorización del equipo. Nunca contra producción ni contra servicios de terceros (Vercel, Neon, Firebase): sus condiciones de uso limitan estas pruebas y consumen cuota real.

Usar una base aislada que se pueda descartar. Definir antes un criterio para cortar la prueba.

## Flujo

1. **Partir de una línea base** de `g04-load-testing`. Sin ella no se puede decir qué es degradarse.
2. **Definir señales de degradación:** por ejemplo, p95 que duplica la línea base o errores por encima del 1%. Definir también cuándo se considera caída.
3. **Escribir el script** con k6: rampa por escalones (por ejemplo +25% cada 2 minutos) hasta superar el límite.
4. **Observar en cada escalón:** latencia, errores 5xx y timeouts, CPU, memoria, event loop y conexiones de la base.
5. **Probar picos:** subida brusca y vuelta a lo normal.
6. **Probar la recuperación:** bajar la carga y medir cuánto tarda en volver a la línea base, si quedan conexiones colgadas o datos a medias.
7. **Revisar integridad:** las escrituras terminadas siguen correctas, y sin duplicados por reintentos.

## Salida

Punto de degradación, punto de falla, primer recurso agotado, tipo de falla (lenta o abrupta, con mensaje claro o no), tiempo de recuperación, margen contra la carga esperada y mejoras por orden de impacto.

## Reglas

- Parar si el proceso afecta a otras personas o servicios.
- No trasladar el número local a producción como si fuera el mismo: el entorno serverless escala y limita distinto.

## Ejemplo de uso
**Pedido:** Buscá hasta dónde aguanta el login y el listado de vehículos.

**Resultado:** La carga donde empieza a degradarse y donde falla, el primer recurso agotado, el comportamiento durante el fallo y si se recupera solo, con script reproducible.
