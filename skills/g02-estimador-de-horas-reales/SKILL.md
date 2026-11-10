---
name: g02-estimador-de-horas-reales
description: Usar cuando el equipo de Zest no cargó horas y hace falta el costo real (AC) del desarrollo para el valor ganado. Estima horas por persona y por semana a partir de los commits de git de todas las ramas, con un método reproducible (margen, piso y techo por día), las valoriza a la tarifa de la línea base y declara qué no puede ver.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - git
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: experimental
  relacionados:
  - g02-valor-ganado-evm
  - g02-ticket-time-estimator
  - g02-dev-grade-estimator
  - g15-evm-calculator
---
# Estimador de horas reales desde git

El valor ganado necesita el **costo real (AC)**, y en Zest el desarrollo no siempre carga
parte de horas. Esta skill da un número **reproducible y auditable** para esas horas, en vez de
uno redondo sin método. **Solo lee el historial de git: no modifica ningún repo.**

No es lo mismo que `g02-ticket-time-estimator` (cuánto *va a durar* un ticket) ni que
`g02-dev-grade-estimator` (nota de cada dev): acá se mide cuánto *se trabajó*, para el AC.

## Paso 1. Preparar los repos

1. Repos que cuentan: el de la app (`zest`) y, si el equipo trabaja ahí, el de soporte
   (`zest-support`).
2. Traé **todas las ramas** y el historial completo: un clon superficial o de una sola rama
   subestima el esfuerzo.
   ```bash
   git -C ../zest fetch --all --prune
   git -C ../zest rev-parse --is-shallow-repository   # tiene que decir false
   ```
   Si dice `true`: `git -C ../zest fetch --unshallow`.
3. Armá `alias.yml` para juntar los distintos emails o nombres de git de una misma persona, y
   para reconocer bots:
   ```yaml
   Thiago Serebrinsky:
     - ThiagoSere
     - thiago@ejemplo.com
   Santiago Blanco Pan:
     - santiagoblancop
   ```

## Paso 2. Correr el script

```bash
python3 horas_git.py --repo ../zest --repo ../zest-support \
  --desde 2026-08-06 --hasta 2026-11-12 --inicio-periodos 2026-08-06 \
  --alias alias.yml --excluir "Claude,github-actions[bot]" \
  --tarifa 10 --csv horas-detalle.csv
```

- **Períodos:** semanales desde `--inicio-periodos`. En Zest, el Período 1 empieza el jueves
  06/08/2026, igual que la línea base.
- **Método por persona y día con actividad:** `acotar((último commit − primer commit) + margen,
  piso, techo)`. Por defecto: margen 1 h (trabajo antes del primer commit), piso 1,5 h y techo
  9 h.
- **`--excluir`:** bots y las personas de gestión, que ya están presupuestadas como nivel de
  esfuerzo. Si no, se cuentan dos veces.
- **`--tarifa`:** la de la línea base vigente. En la v2 de Zest es USD 10/h.

## Paso 3. Revisar antes de usar el número

- **Días de un solo commit:** el script los lista. Caen al piso aunque la jornada haya sido
  larga. Si son muchos, el número está subestimado.
- **Comparar con lo que se sabe:** horas planificadas al corte, horas que el equipo declaró en
  steerings anteriores. Si la diferencia es grande, buscá la causa antes de presentarlo (ramas
  sin traer, alias mal armados, una persona que trabaja sin commitear).
- **Mismo corte que el EV y el PV:** la fecha `--hasta` tiene que ser la fecha de corte del valor
  ganado.

## Paso 4. Entregar

```
## Horas reales estimadas — corte <fecha>
<tabla por persona y período que imprime el script>

AC de desarrollo estimado: USD <total> (<horas> h × USD <tarifa>)

Método: commits de <repos>, todas las ramas, del <desde> al <hasta>;
margen <m> h, piso <p> h, techo <t> h; excluidos: <lista>.

Limitaciones: es un piso (no ve reuniones, diseño ni investigación sin commits);
<n> días con un solo commit contados al piso; <otras>.
```

Pasá el AC a `g02-valor-ganado-evm` para el cálculo. Presentalo como "estimación con este
método, reproducible contra el repositorio".

## Reglas

- No modificar ningún repo: solo `git log`, `git fetch` y `rev-parse`.
- No redondear ni "ajustar" el resultado a mano. Si hace falta corregir algo, se cambia un
  parámetro y se dice cuál.
- No publicar emails de las personas en el entregable: usar nombres.
- Si una persona no aparece en git (por ejemplo, QA que prueba a mano), decirlo y pedir sus
  horas: no inventarlas.

## Ejemplo de uso

**Pedido:** "No tenemos las horas de los devs del Sprint 3. Estimame el AC de desarrollo de Zest del 06/08 al 12/11 desde git, a USD 10 la hora."

**Resultado:** Verifica que el clon no sea superficial, corre `horas_git.py` sobre todas las ramas excluyendo bots y gestión, y devuelve la tabla de horas por dev y por semana (por ejemplo, unas 194 h en total, USD 1.944), con los días de un solo commit marcados y las limitaciones del método escritas, lista para pasar a `g02-valor-ganado-evm`.
