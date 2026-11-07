---
name: g04-chequeo-de-kpis
description: 'Verifica que el reporting diario de KPIs de PitStop esté sano: workflows corridos, muestras, valores publicados en prod y cantidad mínima de KPIs válidos. Usar cuando se pregunta si los KPIs se están reportando bien o antes de una entrega.'
metadata:
  tipo: skill
  area:
  - qa
  - devops
  - datos
  fase:
  - mantenimiento
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - supabase
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados: []
---

# Chequeo de KPIs

Comprueba si el reporting cumple lo que exige el ADR de KPIs de PitStop (`project-plan/adr/ADR-KPIs-PitStop.md`): entre 5 y 10 KPIs válidos por día, y solo `prod` cuenta para el cumplimiento.

## Flujo

1. **Leer el ADR y los tickets de KPI** para confirmar catálogo, ambiente y objetivos. El catálogo puede haber cambiado desde entonces.
2. **Workflows:** en `pitstop-app`, con `gh run list --workflow <archivo>`, revisar las corridas del período, tanto el monitor cada 30 minutos como el cierre diario. Listar fallos y huecos.
3. **Evidencia:** bajar los artifacts de las corridas (`gh run download`) y revisar muestras, lotes y recibos. Conservan 14 días, así que avisar si ya no están.
4. **Por día argentino**, comparar lo enviado contra lo que el receptor devuelve por GET:
   - Cuántos KPIs válidos en `prod`.
   - Falta alguno del catálogo activo.
   - El día de envío (`reported_at`) coincide con el exigido: un envío tardío no repara un día incumplido.
5. **Valores sanos:** porcentajes entre 0 y 100, sin ceros que representen falta de datos. Sin denominador se omite el valor; no se inventa.
6. **Salud actual:** `GET /health` y `GET /health/db` en el ambiente que se está revisando.

## Salida

Tabla por día: KPIs válidos, faltantes, estado (cumple / no cumple), causa y evidencia. Al final, qué corregir primero.

## Reglas

- Solo lectura: no reenviar ni corregir valores. El primer valor publicado es inmutable.
- No mostrar secretos ni copiarlos a la salida. Las credenciales se usan desde su entorno seguro.
- Si no hay acceso a una fuente, decirlo y marcar ese dato como no verificado.

## Ejemplo de uso
**Pedido:** ¿Se reportaron bien los KPIs esta semana?

**Resultado:** Una tabla por día con KPIs válidos en prod, workflows fallidos y envíos faltantes o tardíos, indicando la evidencia y qué hay que corregir.
