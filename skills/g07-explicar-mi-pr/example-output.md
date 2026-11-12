# Ejemplo de output — explicar mi PR (Study Arena, PR #69)

Corrida real del 11/11/2026 sobre el PR #69 de Study Arena, **STUDY-85 · Envío diario de KPIs a la plataforma Lab4**: +1.098 −37 en 24 archivos, mergeado el 15/10. Se usó para preparar la pregunta de KPIs del tercer steering.

---

## 🎤 Versión standup (≈60 segundos)

"Cerré STUDY-85, el envío diario de KPIs a la plataforma de la materia. Todos los días a las 18 el backend saca una foto de los 10 KPIs y los manda en un solo lote; a las 20 los vuelve a mandar por si el primer envío falló, y la plataforma ignora los duplicados. Siempre van los 10, así que nunca perdemos días por un KPI que no se pudo calcular. Si algo falla, queda en el log y hay un endpoint manual para reenviar. Está mergeado y con tests."

## 🧑‍🏫 Versión steering (≈3 minutos)

1. **Problema.** El Challenge N1 pide reportar entre 5 y 10 KPIs válidos por día, por código y sin IA en el medio. La nota es cuántos KPIs válidos llegan por día, así que un día sin envío es nota perdida.
2. **Solución, de afuera hacia adentro.**
   - Un job programado (`MetricsScheduler`) corre a las 18:00 y a las 20:00, hora de Buenos Aires.
   - `KpiReportService` arma el lote con el último corte de los 10 KPIs y lo manda a la plataforma con su clave.
   - Cada KPI del corte guarda cuándo se informó y qué valor se mandó (`reported_at`, `reported_value`).
   - Hay un endpoint manual, `POST /api/v1/internal/metrics/reports`, protegido con un header secreto, para reenviar a mano.
3. **La decisión.** Mandar **siempre los 10 KPIs**: si un KPI no tiene dato va como 0, y si falló su cálculo va con el último valor informado. La alternativa era mandar solo los que se pudieron calcular, pero un día con un error parcial habría bajado la nota. El costo es que un 0 o un valor repetido pueden no reflejar la realidad de ese día, y por eso queda registrado en el snapshot.
4. **Cómo sé que anda.** Cuatro archivos de tests nuevos (unos 650 renglones): el envío contra una plataforma simulada (`MockRestServiceServer`), con fallas, timeouts y configuración incompleta; el scheduler; y el endpoint manual, con y sin secreto. Además hubo una prueba real contra la plataforma central.
5. **Qué sigue.** Mostrar en el portal de KPIs cuántos días llegaron los 10.

## 🖥️ Demo en vivo

1. Abrir el portal de KPIs del Escenario 2 y mostrar el resumen diario del equipo.
2. Si hace falta mostrar el envío, reenviar el último corte (con el backend de producción y el secreto del job, que no se muestra en pantalla):
   ```bash
   curl -X POST "$BACKEND_URL/api/v1/internal/metrics/reports" -H "X-Metrics-Job-Secret: $METRICS_JOB_SECRET"
   ```
   Responde 200 si la plataforma aceptó el lote y 502 si falló.
3. **Plan B:** mostrar los tests del envío pasando (`KpiReportServiceTest`) y una fila de `kpi_snapshots` con `reported_at` cargado.

## ❓ Preguntas probables

1. **"Si un KPI no tiene dato y mandan 0, ¿no están inflando la nota?"** — El 0 es un valor real ("no hubo actividad"), no un dato inventado, y la plataforma lo cuenta igual que cualquier otro. Pero es una decisión discutible: si la cátedra considera que un KPI sin dato no es válido, se cambia en un solo lugar del servicio.
2. **"¿Y si falla el envío de las 18?"** — Se reenvía a las 20 y además hay un endpoint manual. La plataforma ignora los duplicados, así que reenviar no ensucia los datos.
3. **"¿Cómo saben que llegaron?"** — Cada KPI guarda `reported_at` cuando la plataforma acepta el lote, y los fallos quedan en el log como `KPI_REPORT_FAILED`. Lo más fuerte es mostrar el portal.
4. **"¿Por qué a las 18 y no a la medianoche?"** — Respuesta a confirmar con el autor: ¿se eligió para que el reenvío de las 20 caiga el mismo día de recepción, que es el que cuenta para la nota?
5. **"¿Qué pasa si alguien levanta el backend en su compu con la configuración de producción?"** — Es un riesgo real: cualquier backend con las 4 variables de la plataforma manda KPIs. Para evitarlo, en los entornos locales se dejan vacías o con un ambiente que no sea `prod`.
6. **"¿Cómo lo testearon sin pegarle a la plataforma real?"** — Con `MockRestServiceServer`, que simula las respuestas de la plataforma, incluidos errores y timeouts.

---

Links: PR #69 (`jmsapag/study-arena`) · ticket STUDY-85.
