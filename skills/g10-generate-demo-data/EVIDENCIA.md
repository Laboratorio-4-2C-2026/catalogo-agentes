# Caso de uso — datos para demostrar Conexia

Se preparó y cargó un lote coherente para disponer de cuentas, horarios, viajes e intenciones con los que recorrer el producto. La carga del 5/11/2026 incorporó 600 usuarios del lote y 5.000 registros en varias entidades; los efectos de matching dejaron 9.649 coincidencias del lote.

| Evidencia | Qué respalda |
|---|---|
| [Generación local](evidencias/run-summary.json) | Cantidades, reglas y comprobaciones del dataset inicial |
| [Carga realizada](evidencias/load-report.json) | Cuentas, avatares y registros cargados; login y consultas verificadas |
| [Integridad posterior](evidencias/post-load-integrity.json) | Doce controles sin incidencias en relaciones y reglas de negocio |

Las cifras del lote se distinguen del total de la base y de la generación inicial. Son datos de demo creados para probar una aplicación real. Las cuentas se verificaron administrativamente; ese método no acredita recepción de correo institucional. Los extractos conservan resultados históricos y no incluyen credenciales ni el dataset masivo.
