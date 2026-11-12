---
name: g07-balance-gamificacion
description: "Simula el sistema de puntos real de Study Arena (puntos por participación en sesiones de estudio según tramos de presencia, puntos por quiz completado y ranking semanal por grupo con dense rank) con poblaciones de usuarios ficticios durante semanas, para detectar exploits como quizzes de una pregunta o irse temprano de una sesión, medir qué fuente de puntos domina y probar cambios de reglas antes y después. Usar antes de cambiar una regla de puntos o cuando alguien pregunta si el ranking es justo; no modifica código."
metadata:
  tipo: skill
  area:
  - backend
  - datos
  - diseno
  fase:
  - analisis
  - diseno
  - revision
  tecnologias:
  - spring-boot
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-seed-mundo-gamificado
  - g07-documentar-producto
---

# Balance de gamificación

Cada regla de puntos de Study Arena se escribió en su propio ticket ("los puntos de una sesión dependen de cuánto estuviste presente", "un quiz da hasta 50 puntos"), pero nadie mira cómo se comportan **juntas** con muchos usuarios durante semanas. Ahí aparecen los problemas: una acción que se puede repetir sin límite, un tramo que premia irse temprano o una fuente de puntos que hace que la otra no importe.

Esta skill convierte las reglas reales del código en un simulador, lo corre con distintos tipos de usuario y responde, con números, si el sistema es justo y si se puede hacer trampa.

## El sistema real (verificar contra el código antes de cada uso)

Study Arena **no** tiene XP, niveles, rachas ni logros. El simulador `simulador_base.py` de esta carpeta ya trae estas reglas, cada una con su `archivo:línea`:

- **Puntos**: una fila de `PointTransaction` por recompensa, única por `(usuario, tipo de fuente, fuente, motivo)`, de modo que la misma fuente nunca paga dos veces. Los motivos son solo `SESSION_PARTICIPATION` y `QUIZ_COMPLETION`.
- **Sesión** (`SessionPointsCalculator`): `participación = segundos presentes / (duración planificada × 60)`. Con `≥ 0,85` se multiplica por 1,5, con `≥ 0,50` por 1,0, con `≥ 0,20` por 0,5 y por debajo da 0. `puntos = round(duración planificada × multiplicador)`. La duración es `(focus + break) × ciclos`, sin máximo. La presencia se cuenta por heartbeats con una ventana de 30 s, y no se puede estar presente en dos sesiones a la vez (`AlreadyInAnotherSessionException`).
- **Quiz** (`QuizService`): `puntos = round(correctas / total × 50)`, solo por el primer intento completado. Un quiz tiene de 1 a 50 preguntas, y el autor puede jugar su propio quiz.
- **Ranking** (`LeaderboardService`, `WeekService`): semanal y **por grupo**, de lunes a lunes en hora de Buenos Aires según `earnedAt`, con dense rank (1, 2, 2, 3).

## Cuándo usar esta skill

- "¿Es justo el ranking?", "¿se pueden farmear puntos?", "¿qué pesa más, sesiones o quizzes?"
- Antes de aprobar un ticket que cambia una regla de puntos, sesiones, quizzes o ranking, para comparar el antes y el después.
- Para justificar con datos una decisión de diseño ante la cátedra o el PO.

## Paso 1: confirmar que las reglas siguen iguales

Antes de simular, releé los archivos citados en el docstring de `simulador_base.py` sobre la rama actual (`rg -n "THRESHOLD|MULTIPLIER|MAX_QUIZ_POINTS" backend/src/main/java`, `CreateSessionRequest`, `QuizRequest`, `playable(`). Si algo cambió, actualizá `REGLAS` y las funciones del simulador antes de correrlo, y avisale al usuario qué cambió.

## Paso 2: correr el escenario base

Copiá el simulador a un directorio temporal (no al repo) y corré `python3 -I simulador.py --semanas 16 --usuarios 200 --seed 42`. Usá siempre la misma `--seed` entre escenarios para comparar.

Perfiles: casual, constante, intenso, tardío (se suma en la semana 6), el que abandona y el **farmer**, que explota las reglas reales: una sesión por día en la que se queda apenas pasado el 20% (el tramo que más paga por minuto presente) y varios quizzes propios de 1 pregunta por día.

## Paso 3: diagnosticar

Marcá cada señal 🟢/🟡/🔴 con el número que lo justifica:

- **Farmeo**: puntos del farmer contra los del intenso. Mostralo **separado por fuente**, porque el promedio mezclado esconde el exploit (un quiz de 1 pregunta rinde decenas de veces más puntos por minuto que una sesión).
- **Incentivo de presencia**: puntos por minuto presente en cada tramo de sesión. Si el tramo bajo paga más por minuto que el alto, el sistema premia irse temprano: es 🔴.
- **Fuente dominante**: qué % de los puntos viene de sesiones y qué % de quizzes para cada perfil.
- **Ranking semanal por grupo**: con grupos realistas (4 a 8 personas), cuántas semanas gana el mismo usuario en su grupo y si un solo farmer gana todas.
- **Tardío**: si con los mismos hábitos que el constante compite en igualdad desde su primera semana (debería, porque el ranking se reinicia cada lunes).

Cuidado con los artefactos del modelo: si un perfil tiene parámetros distintos a otro, la diferencia en sus resultados no se puede atribuir a las reglas. Compará perfiles que solo difieran en lo que querés medir.

## Paso 4: probar alternativas

Para cada 🟡/🔴, proponé una o dos reglas alternativas concretas y simulá el antes y el después con la misma semilla. Ejemplos para este sistema:

- quizzes: un mínimo de preguntas para que el quiz dé puntos, que el autor no reciba puntos por jugar su propio quiz, o un tope diario de puntos por quizzes;
- sesiones: puntos proporcionales al tiempo presente en lugar de a la duración planificada, o tramos cuyo rendimiento por minuto no decrezca.

Aclarale al usuario que son propuestas de diseño: el PO decide.

## Output

1. Reglas verificadas y la rama o commit contra el que se verificaron.
2. Tabla por perfil: puntos medianos, puntos por minuto invertido y % por fuente.
3. Señales 🟢/🟡/🔴 con su número.
4. Alternativas probadas, con el antes y el después.
5. Supuestos y limitaciones del modelo (comportamiento de cada perfil, tiempos estimados para crear un quiz, etc.).

Ver `example-output.md` para una corrida real sobre Study Arena.

## Qué no hacer

- No modifiques el código del backend ni crees tickets: entregá el análisis.
- No presentes el resultado como verdad sobre usuarios reales: es una simulación con perfiles supuestos.
- No dejes el simulador dentro del repo de Study Arena salvo que el usuario lo pida.

## Ejemplo de uso

**Pedido:** ¿Se pueden farmear puntos en Study Arena? ¿Qué cambia si ponemos un mínimo de 5 preguntas por quiz para que dé puntos?

**Resultado:** Verifica las reglas de sesiones, quizzes y ranking en el backend y corre 16 semanas con 200 usuarios. Muestra que crear y jugar quizzes propios de 1 pregunta da unos 75 puntos por minuto contra menos de 2 de una sesión, y que el tramo del 20% paga más por minuto que quedarse toda la sesión. Después repite la corrida con el mínimo de 5 preguntas y compara el antes y el después.
