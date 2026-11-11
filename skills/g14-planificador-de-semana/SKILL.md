---
name: g14-planificador-de-semana
description: Secuencia y publica en Jira una semana de sprint en dos carriles (aplicación y datos/motor) con sus tareas madre y dependencias, usando la capacidad por dev acordada antes (en VaiVen, ~6 h; menos si la semana se replanificó). Usala cuando dirección tiene que desglosar la próxima semana para dos devs de dedicación parcial, asumiendo cerrada la semana anterior. Publica con g14-auditor-de-jira.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: "14"
  autor:
    nombre: Anapaola Borda
    github: AnaB2
  colaboradores: []
  responsables:
  - AnaB2
  madurez: usado-en-proyecto
  relacionados: []
---

# Planificador de semana

Baja el plan del hito a **una semana ejecutable por carril**. En VaiVen: dos devs a 6 h/semana, carril A (aplicación, etiqueta `app`) y carril B (datos y motor), una **tarea madre por carril y semana** con sus subtareas. Ejemplos reales: `docs/planning/tickets/tareas-madre/h4-semana-8-carril-{a,b}.md`, los README de `docs/planning/tickets/hito-4/`, `hito-5/` y `hito-6/`.

## Reglas duras

1. **La semana N asume cerrada la N-1.** Se escribe sobre lo que la anterior **tenía que entregar**, no sobre el estado de `main` a mitad de semana. Sin filas de arrastre, sin horas de la semana anterior, sin condicionales del tipo «si X se atrasa, movemos Y». El atraso se gestiona aparte, en el tablero de seguimiento.
2. **No hay semanas vacías.** Cada carril llega a la capacidad acordada (~6,0 h en VaiVen; si `g14-planificador-de-capacidad` redujo la semana, ese es el techo). Si el contenido mínimo no llena la semana, se completa con **alcance real** (pulido contra Figma, validación de errores, QA, adelantar tickets del hito siguiente), nunca inflando estimaciones. Ver `g14-planificador-de-capacidad`.
3. **El techo de cada ticket lo fija su «qué NO hacer»**, no las horas.
4. **Se lee contra `main` antes de sumar.** Un ticket que da por existente una tabla o un componente se verifica en el código (en la semana 10 de VaiVen, `matches` y `contactos` no existían y la semana se rearmó).
5. **Un artefacto que no se edita en paralelo es de un solo carril** (en VaiVen, el workflow JSON de n8n): toda la cadena que lo toca va al mismo dev.

## Procedimiento

1. **Juntá la entrada:** qué promete el hito para esa semana (README del hito), qué cierra la semana anterior, qué pidió el PM, y si hay parciales u otras entregas en la semana.
2. **Elegí los tickets por carril** y ordenalos por dependencia. El PR que desbloquea al otro carril va **primero y solo** («este PR se abre el primer día»).
3. **Cruzá dependencias entre carriles** dentro de la semana: si A espera algo de B, B lo entrega en sus primeras horas, y A arranca por lo que no depende de nada. Marcá en cada ticket `Depende de` / `Bloquea`.
4. **Medí** cada carril (ver formato abajo). A 6,0 / B 6,0, con el colchón declarado si lo hay.
5. **Escribí la tarea madre** de cada carril (formato abajo) y los tickets nuevos con el estándar de redacción (ver `g14-redactor-de-tickets-ejecutables` y `g14-traductor-de-tickets-para-jira`).
6. **Actualizá el README del hito:** la semana con su estado (`BORRADOR` → `PUBLICADA`), las claves de Jira y lo que **salió** de la semana y a dónde fue (otra semana, reserva, de baja).
7. **Revisión en frío** antes de publicar (`g14-revisor-fresco-de-tickets`): se aplican los hallazgos y se hace una vuelta de cierre.
8. **Publicá con `g14-auditor-de-jira`:** las issues nuevas (tickets y madres) se crean primero en Jira, a mano o por MCP, para tener su clave; después se suman al mapeo de su `sync-all-jira.py` y se sincronizan las descripciones. Esta skill no trae un creador de issues propio (en VaiVen era un script atado a los hitos del proyecto). Releé desde Jira, corré T1 sobre lo publicado, confirmá que la estimación quedó cargada y que todo está en «Por hacer». Auditá con el `auditar-jira.py` de esa misma skill (exit 0).
9. **Registrá** en el estado del proyecto (`PLANNING-STATE.md`): qué se publicó, claves, horas por carril, qué pasa a la semana siguiente y los pendientes.

## Formato de la tarea madre

```markdown
# Semana N · carril A — <qué queda funcionando al final>

| | |
|---|---|
| **Tarea madre** | `Semana N · carril A` — `SCRUM-xx` |
| **Sprint** | n · fechas · **semana N (dd/mm – dd/mm)** · 🔴 parcial dd/mm |
| **Horas** | **6,0 h**, con 0,25 de colchón |
| **Depende de** | la semana N-1 cerrada, sin arrastres; <entregas de dirección> |
| **Desbloquea** | <qué habilita> |

**Qué construye.** <un párrafo: el orden de la semana y por qué>

## Los tickets
| ID | Ticket | Depende de |

## La medición
| Ticket | h |  ... | Colchón | **Suma 6,0** |
Salió hacia la semana N+1: <ticket (h, motivo)>.
```

En Jira la madre publica «Qué construye», la tabla de tickets y las dependencias; **la medición no** (las horas van al campo de estimación).

## Qué NO hacer

- No metas arrastres ni condicionales sobre lo atrasado.
- No inflés una estimación para llenar la semana: traé alcance.
- No publiques una semana sin la revisión en frío ni sin T1 sobre lo publicado.
- No pongas en Jira códigos internos ni la palabra «carril» en títulos o descripciones; issues nuevas pasan de «Idea» a «Por hacer».

## Ejemplo de uso

**Pedido:** Armá la semana 11 del Hito 5 (30/10 – 05/11): el carril A conecta la elección del candidato y el B la función `elegir_candidato`, con la promoción a producción.

**Resultado:** Dos tareas madre a 6,0 h cada una, con el PR que desbloquea al otro carril primero, dependencias cruzadas marcadas, lo que sale de la semana anotado en el README del hito, y la secuencia de revisión en frío y publicación lista para correr.
