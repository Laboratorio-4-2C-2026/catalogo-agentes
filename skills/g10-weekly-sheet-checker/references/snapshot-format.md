# Snapshot de lectura

El helper verifica fecha, origen y campos semanales. Las recomendaciones sobre avances y su contenido se elaboran con las fuentes del proyecto.

Comando:

```text
python scripts/check_week.py --context <contexto.json> --snapshot <lectura.json>
```

El contexto usa `timezone`, `report_year`, `max_snapshot_age_hours`, identidad de `sheet` (`spreadsheet_id`, `gid`, `sheet_name`) y este bloque. El snapshot debe cubrir los encabezados y filas configurados, con sus etiquetas:

```json
{
  "weekly": {
    "header_row": 7,
    "first_column": "B",
    "last_column": "U",
    "week_start_iso": 1,
    "allowed_values": ["Verde", "Amarillo", "Rojo"],
    "required_inputs": [{"name": "Alcance", "row": 10}],
    "reasons": {"column": "V", "required_for": ["Amarillo", "Rojo"]},
    "computed_summary": {"row": 8, "rule": "one_red_or_three_yellows"}
  }
}
```

Configurar todas las filas requeridas reales. Omitir `computed_summary` si la hoja tiene otra regla; en ese caso revisar la fórmula directamente. El helper implementa únicamente la regla expresamente indicada: un rojo o tres amarillos dan Rojo; uno o dos amarillos dan Amarillo; todo verde da Verde. No impone esa regla a otras plantillas.

El snapshot debe contener valores de la pestaña exacta, con origen A1, representados como listas de filas y columnas. Conservar posiciones vacías:

```json
{
  "source": {
    "spreadsheet_id": "id-de-la-planilla",
    "gid": "id-de-la-pestana",
    "sheet_name": "nombre-verificado",
    "read_at": "2026-11-04T21:00:00-03:00"
  },
  "values": []
}
```

Obtener esos valores del conector o copiando un rango verificado en Google Sheets. Para texto TSV, usar un lector CSV con delimitador tabulador y soporte de celdas entrecomilladas con saltos de línea; no partirlo simplemente por cada salto. En el navegador, usar solo las acciones y el portapapeles documentados de computer-use. No crear el snapshot a partir de valores supuestos.

`--at` permite comprobar un corte histórico con zona horaria explícita; no usarlo para presentar una lectura vieja como actual. `COMPLETE` comprueba presencia y valores permitidos, no autoría ni fecha de edición. Las razones compartidas y los campos externos requieren interpretación. `UNVERIFIED` y `PERIOD_NOT_FOUND` requieren resolver lectura o calendario; no son olvidos del usuario.

Para una prueba de otra semana expresamente solicitada, agregar `--week-start 2026-11-09`. Conservar el `read_at` real y el corte actual: este argumento solo selecciona la columna y marca `preview: true` cuando corresponde. No usar un `--at` futuro para simular que la lectura o los hechos ocurrieron en el futuro. Este helper solo lee archivos locales y produce su resultado; bajo ningún concepto escribe en el Sheet.

Usar Python 3.9 o posterior con datos de zonas horarias del sistema o el paquete `tzdata`. Si faltan esos datos, el contexto puede proporcionar `timezone_fallback` con `offset`, `valid_from` y `valid_until`: solo se admite un desplazamiento fijo expresamente verificado para ese intervalo. No configurar un offset fijo para una zona con cambios estacionales dentro del período. Al vencer el intervalo, el helper pide resolver la zona en lugar de adivinarla.
