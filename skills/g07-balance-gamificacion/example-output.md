# Ejemplo de output — balance de puntos de Study Arena

Corrida real sobre las reglas del backend de Study Arena (commit `874dc77`, 11/11/2026), con `python3 -I simulador.py --semanas 16 --usuarios 200 --seed 42`.

## Salida del simulador

```
perfil        n pts total med  pts/min invertido
abandona     19          1106               1.63
casual       79          1731               1.42
constante    45          9294               1.61
farmer        7        122958               5.05
intenso      21         16989               1.77
tardio       29          5621               1.63

Señales
- Puntos totales: farmer / intenso = 7.24  (puntos acumulados en 16 semanas)
- Eficiencia (puntos por minuto REAL invertido): farmer / intenso = 2.85  <- esta es la señal que importa, no el total acumulado

- Puntos por fuente (SESSION vs QUIZ), por perfil:
  abandona   QUIZ=8%, SESSION=92%
  casual     QUIZ=9%, SESSION=91%
  constante  QUIZ=12%, SESSION=88%
  farmer     QUIZ=52%, SESSION=48%
  intenso    QUIZ=16%, SESSION=84%
  tardio     QUIZ=11%, SESSION=89%

- Ranking semanal: máximo de semanas seguidas con el mismo top 5 = 1 de 16  (el ranking resetea cada lunes, WeekService.java:31-42: no es acumulativo)
- El 'tardío' empata la mediana semanal del 'constante' en la semana: 9  (como el ranking es semanal, no cumulativo, compite en igualdad apenas empieza)
- Concentración: el top 10% de usuarios tiene el 56% de los puntos acumulados en 16 semanas
```

## Diagnóstico

| Señal | Estado | Evidencia |
|---|---|---|
| Farmeo con quizzes propios de 1 pregunta | 🔴 | 50 puntos en unos 40 s (≈ 75 pts/min) contra 1,5–1,8 pts/min de una sesión. El farmer saca 7,2 veces los puntos del intenso. |
| Incentivo de presencia en sesiones | 🔴 | Por minuto presente, el tramo del 20% paga 2,5 puntos, el del 50% paga 2,0 y el del 85% paga 1,76: quedarse rinde menos que irse temprano. |
| Sesiones larguísimas | 🟢 | Los puntos crecen lineal con la duración, así que alargarla no mejora el rendimiento por minuto. No se puede estar en dos sesiones a la vez (`AlreadyInAnotherSessionException`). |
| Fuente dominante | 🟡 | Los usuarios honestos sacan entre el 84% y el 92% de sus puntos de sesiones; el farmer saca el 52% de quizzes. |
| Ranking semanal | 🟢 | El top 5 nunca se repite dos semanas seguidas: el reinicio de cada lunes le da chance a todos. |

## Alternativas a simular

- **Quizzes**: mínimo de 5 preguntas para que el quiz dé puntos, que el autor no reciba puntos por jugar su propio quiz, o tope diario de puntos por quizzes.
- **Sesiones**: puntos proporcionales al tiempo presente (`totalSeconds`) en vez de a la duración planificada, o tramos cuyo rendimiento por minuto no decrezca.

## Limitaciones de esta corrida

- Todos los usuarios están en un solo grupo de 200; en la app el ranking es por grupo de 4 a 8 personas.
- El tiempo para crear y jugar un quiz (40 s) es una estimación.
- El perfil "tardío" tiene menos participación que el "constante", así que la semana en que lo alcanza depende del perfil, no de las reglas.
