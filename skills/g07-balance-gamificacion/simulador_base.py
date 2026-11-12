"""Simulador de balance de puntos (g07-balance-gamificacion).

Study Arena NO tiene XP, niveles, rachas ni logros. El sistema real es:

  - PointTransaction (entity/points/PointTransaction.java): una fila por recompensa,
    con (user_id, source_type, source_id, reason) UNIQUE (uk_point_tx_user_source_reason,
    PointTransaction.java:40-45). Es idempotente: la misma fuente nunca paga dos veces
    al mismo usuario por el mismo motivo, incluso si el puntaje calculado es 0
    (PointTransaction.java:30-31; PointsService.java:66).
  - PointReason (entity/points/PointReason.java:7-9): solo SESSION_PARTICIPATION y
    QUIZ_COMPLETION. No hay "duelos", "misiones" ni nada parecido.

Reglas de puntaje por sesión (service/points/SessionPointsCalculator.java):
  - plannedDurationMinutes = (focusTime + breakTime) * cycles
    (entity/session/Session.java:96). El break cuenta como tiempo planificado.
  - CreateSessionRequest solo valida @Positive en focusTime/breakTime/cycles,
    sin @Max (dto/session/CreateSessionRequest.java:26-36): no hay techo de duración.
  - totalSeconds se acumula por heartbeat con ventana de continuidad de 30s
    (entity/session/SessionParticipant.java:51, accumulateIfContinuous :160-165).
    No depende de que haya otros participantes: una sesión con un solo asistente
    computa exactamente igual (SessionPointsCalculator.java:30-51 no mira a nadie más).
  - participacion = totalSeconds / (plannedDurationMinutes * 60)  [SessionPointsCalculator.java:37]
  - tramos (bordes con >=, SessionPointsCalculator.java:22-28,40-48):
        >= 0.85 -> x1.5
        >= 0.50 -> x1.0
        >= 0.20 -> x0.5
        <  0.20 -> 0 puntos
  - puntos = round(plannedDurationMinutes * multiplicador)  [SessionPointsCalculator.java:50]
  - Los puntos se materializan recien al consultar el ranking del grupo
    (PointsService.awardPendingSessionPoints, PointsService.java:151-164), con
    earnedAt = session.plannedEndsAt (no el momento de la consulta).

Reglas de puntaje por quiz (service/QuizService.java):
  - Un quiz tiene entre 1 y 50 preguntas (dto/material/QuizRequest.java:19-21).
  - puntos = round(correctas / total_preguntas * 50)  [QuizService.java:83,323-324]
    Ojo: un quiz de 1 pregunta y uno de 50 preguntas pagan el mismo máximo (50 puntos)
    si se responde todo bien: la cantidad de preguntas no multiplica el premio.
  - Solo el primer intento COMPLETADO cuenta (QuizAttempt con completedAt, y la
    idempotencia de PointTransaction hace el resto): intentos repetidos no sirven,
    pero SÍ sirve crear un nuevo quiz (un nuevo source_id) por cada ronda de farming.
  - El autor de un quiz SÍ puede jugarlo: playable() (QuizService.java:376-386) solo
    exige que no sea DRAFT; a diferencia de own() (QuizService.java:388-398), que es el
    que sí exige ser el autor, playable() nunca excluye al autor. No hay bloqueo de
    "no podés jugar tu propio quiz".

Ranking semanal (service/points/LeaderboardService.java, WeekService.java):
  - Semanal y por grupo, lunes 00:00 (inclusive) a lunes 00:00 siguiente (exclusive),
    zona America/Argentina/Buenos_Aires (WeekService.java:31-42), agrupado por earnedAt.
  - Posicion por DENSE_RANK sobre los puntos (1, 2, 2, 3); empates ordenados
    alfabeticamente por nombre solo para mostrar, sin afectar la posicion
    (LeaderboardService.java:79-100).
  - El ranking se resetea cada semana: no es acumulativo entre semanas. Un usuario que
    se suma tarde compite en igualdad de condiciones desde la semana en que empieza.

Sin dependencias externas: python3 simulador.py --semanas 16 --usuarios 200 --seed 42
"""
import argparse
import random
import statistics
from collections import defaultdict

# ---------------------------------------------------------------------------
# REGLAS REALES (citas archivo:línea en el docstring de arriba y en cada función)
# ---------------------------------------------------------------------------
REGLAS = {
    "session_umbral_alto": 0.85,      # SessionPointsCalculator.java:22
    "session_umbral_medio": 0.50,     # SessionPointsCalculator.java:23
    "session_umbral_bajo": 0.20,      # SessionPointsCalculator.java:24
    "session_mult_alto": 1.5,         # SessionPointsCalculator.java:26
    "session_mult_medio": 1.0,        # SessionPointsCalculator.java:27
    "session_mult_bajo": 0.5,         # SessionPointsCalculator.java:28
    "quiz_max_puntos": 50,            # QuizService.java:83
    "quiz_min_preguntas": 1,          # dto/material/QuizRequest.java:20
    "quiz_max_preguntas": 50,         # dto/material/QuizRequest.java:20
    "heartbeat_ventana_seg": 30,      # entity/session/SessionParticipant.java:51
}


def session_points(planned_minutes, participation_ratio):
    """puntos de una participación en sesión. SessionPointsCalculator.java:30-51."""
    if planned_minutes <= 0:
        return 0
    if participation_ratio >= REGLAS["session_umbral_alto"]:
        mult = REGLAS["session_mult_alto"]
    elif participation_ratio >= REGLAS["session_umbral_medio"]:
        mult = REGLAS["session_mult_medio"]
    elif participation_ratio >= REGLAS["session_umbral_bajo"]:
        mult = REGLAS["session_mult_bajo"]
    else:
        return 0
    return round(planned_minutes * mult)


def quiz_points(correct, total):
    """puntos de un intento de quiz completado. QuizService.java:323-324."""
    if total <= 0:
        return 0
    return round(correct / total * REGLAS["quiz_max_puntos"])


class PointLedger:
    """Emula la idempotencia real de PointTransaction: una fila por
    (user_id, source_type, source_id, reason). PointTransaction.java:40-45;
    PointsService.awardPoints, PointsService.java:68-93."""

    def __init__(self):
        self._seen = set()
        self.rows = []  # (user_id, week, source_type, source_id, reason, points, minutos_reales)

    def award(self, user_id, week, source_type, source_id, reason, points, minutos_reales):
        key = (user_id, source_type, source_id, reason)
        if key in self._seen:
            return 0  # ya materializado: no paga de nuevo (idempotente)
        self._seen.add(key)
        self.rows.append((user_id, week, source_type, source_id, reason, points, minutos_reales))
        return points


# Perfiles: probabilidad de actuar cada día, y cómo juegan. Nada de "racha" ni "nivel":
# cada perfil es simplemente cuánto y cómo usa sesiones y quizzes.
PERFILES = {
    "casual":    dict(peso=0.35, p_dia=0.35, alta=0, baja=None),
    "constante": dict(peso=0.25, p_dia=0.80, alta=0, baja=None),
    "intenso":   dict(peso=0.10, p_dia=0.97, alta=0, baja=None),
    "farmer":    dict(peso=0.05, p_dia=1.00, alta=0, baja=None),
    "tardio":    dict(peso=0.15, p_dia=0.80, alta=6, baja=None),
    "abandona":  dict(peso=0.10, p_dia=0.80, alta=0, baja=3),
}


def dia_de_accion(perfil_cfg, semana, rnd):
    activo = semana >= perfil_cfg["alta"] and (perfil_cfg["baja"] is None or semana < perfil_cfg["baja"])
    return activo and rnd.random() < perfil_cfg["p_dia"]


def jugar_dia_honesto(perfil, rnd, ledger, user_id, semana, dia_global, next_session_id):
    """Un día de un perfil honesto (no farmer): participa de sesiones reales con
    distinto grado de compromiso, y a veces completa un quiz normal (varias
    preguntas, acierto imperfecto). Devuelve (puntos_dia, minutos_reales_dia)."""
    puntos = 0
    minutos = 0.0

    # --- sesión de estudio ---
    # Sesiones de duración "normal" del uso real: focusTime+breakTime por ciclo entre
    # ~20 y 45 min, 2 a 4 ciclos. plannedDurationMinutes = (focus+break)*cycles,
    # Session.java:96.
    focus_break = rnd.uniform(20, 45)
    ciclos = rnd.randint(2, 4)
    planned_minutes = focus_break * ciclos

    if perfil == "intenso":
        participacion = rnd.uniform(0.80, 1.0)
    elif perfil == "constante":
        participacion = rnd.uniform(0.45, 0.85)
    elif perfil == "tardio":
        participacion = rnd.uniform(0.45, 0.80)
    elif perfil == "abandona":
        participacion = rnd.uniform(0.25, 0.60)
    else:  # casual
        participacion = rnd.uniform(0.15, 0.50)

    session_id = next_session_id()
    pts = session_points(planned_minutes, participacion)
    ganado = ledger.award(user_id, semana, "SESSION", session_id, "SESSION_PARTICIPATION", pts, None)
    puntos += ganado
    # minutos reales realmente presentes (lo que de verdad "cuesta" en heartbeats)
    minutos += planned_minutes * min(participacion, 1.0)

    # --- quiz normal (a veces) ---
    prob_quiz = {"intenso": 0.55, "constante": 0.30, "tardio": 0.30, "abandona": 0.20, "casual": 0.15}[perfil]
    if rnd.random() < prob_quiz:
        total_preguntas = rnd.randint(5, 20)
        acierto = {"intenso": rnd.uniform(0.80, 0.98),
                   "constante": rnd.uniform(0.65, 0.90),
                   "tardio": rnd.uniform(0.60, 0.85),
                   "abandona": rnd.uniform(0.50, 0.75),
                   "casual": rnd.uniform(0.45, 0.70)}[perfil]
        correctas = round(total_preguntas * acierto)
        quiz_id = ("quiz", user_id, dia_global, "honesto")  # un quiz nuevo por intento real
        pts_q = quiz_points(correctas, total_preguntas)
        ganado_q = ledger.award(user_id, semana, "QUIZ", quiz_id, "QUIZ_COMPLETION", pts_q, None)
        puntos += ganado_q
        # tiempo real: responder N preguntas, ~20s cada una
        minutos += total_preguntas * (20 / 60)

    return puntos, minutos


def jugar_dia_farmer(rnd, ledger, user_id, semana, dia_global, next_session_id, next_quiz_id):
    """El farmer explota las reglas reales, no reglas inventadas:

    a) Sesión "larguísima" en vez de corta: el puntaje escala linealmente con
       plannedDurationMinutes (session_points), así que alargar la sesión NO mejora
       los puntos por minuto realmente invertido (ver nota más abajo). Se simula
       igual para demostrarlo con números.
    b) La sesión la hace solo: SessionPointsCalculator.java:30-51 no mira a otros
       participantes, así que da exactamente los mismos puntos.
    c) Quiz de 1 sola pregunta: QuizRequest permite min=1 (QuizRequest.java:20), y
       quiz_points no premia más preguntas, así que 1 pregunta = hasta 50 puntos
       igual que un quiz de 50.
    d) Juega su propio quiz: QuizService.playable() (QuizService.java:376-386) no
       excluye al autor, a diferencia de own() (QuizService.java:388-398). Como
       escribió la pregunta, acierta siempre.
       Como la idempotencia es por quiz_id (PointTransaction.java:40-45), cada quiz
       NUEVO vuelve a pagar: no hay límite de cuántos quizzes de 1 pregunta puede
       crear y jugar en un día.
    """
    puntos = 0
    minutos = 0.0

    # a) + b): una sesión "larguísima", solo, apuntando apenas al umbral MÁS BAJO
    # (0.20 -> x0.5) en vez de quedarse toda la sesión (0.85 -> x1.5), porque el
    # umbral bajo da MÁS puntos por minuto invertido: tasa = multiplicador/umbral.
    #   bajo:  0.5 / 0.20 = 2.50 puntos por minuto "planificado" cruzado
    #   medio: 1.0 / 0.50 = 2.00
    #   alto:  1.5 / 0.85 ≈ 1.76  (quedarse toda la sesión rinde MENOS por minuto)
    planned_minutes = rnd.uniform(600, 1500)  # sesión "larguísima": varias horas planificadas
    participacion = REGLAS["session_umbral_bajo"] + 0.001  # cruza apenas el tramo bajo, solo
    session_id = next_session_id()
    pts_s = session_points(planned_minutes, participacion)
    ganado_s = ledger.award(user_id, semana, "SESSION", session_id, "SESSION_PARTICIPATION", pts_s, None)
    puntos += ganado_s
    minutos += planned_minutes * participacion  # minutos reales que de verdad hay que esperar presente

    # c) + d): varios quizzes de 1 pregunta por día, autor = jugador, 100% acierto.
    quizzes_por_dia = rnd.randint(8, 15)
    for _ in range(quizzes_por_dia):
        quiz_id = next_quiz_id()
        pts_q = quiz_points(1, 1)  # 1/1 correctas = 50 puntos (quiz_points)
        ganado_q = ledger.award(user_id, semana, "QUIZ", quiz_id, "QUIZ_COMPLETION", pts_q, None)
        puntos += ganado_q
        # tiempo real: crear el quiz (formulario) + jugarlo (1 click): ~40s en total
        minutos += 40 / 60

    return puntos, minutos


def simular(semanas, usuarios, seed):
    rnd = random.Random(seed)
    nombres = list(PERFILES)
    pesos = [PERFILES[p]["peso"] for p in nombres]
    jugadores = [dict(id=i, perfil=rnd.choices(nombres, pesos)[0]) for i in range(usuarios)]

    puntos_totales = defaultdict(int)          # user_id -> puntos acumulados (todas las semanas)
    minutos_totales = defaultdict(float)       # user_id -> minutos reales invertidos
    puntos_por_semana = defaultdict(lambda: defaultdict(int))  # semana -> user_id -> puntos de ESA semana
    puntos_por_fuente = defaultdict(lambda: defaultdict(int))  # perfil -> source_type -> puntos

    ledger = PointLedger()
    _counter = {"session": 0, "quiz": 0}

    def next_session_id():
        _counter["session"] += 1
        return ("session", _counter["session"])

    def next_quiz_id():
        _counter["quiz"] += 1
        return ("quiz", _counter["quiz"])

    top5_por_semana = []
    for dia in range(semanas * 7):
        semana = dia // 7  # día 0 = lunes de la semana 0; WeekService.java:31-42
        for j in jugadores:
            cfg = PERFILES[j["perfil"]]
            if not dia_de_accion(cfg, semana, rnd):
                continue
            if j["perfil"] == "farmer":
                pts, mins = jugar_dia_farmer(rnd, ledger, j["id"], semana, dia, next_session_id, next_quiz_id)
            else:
                pts, mins = jugar_dia_honesto(j["perfil"], rnd, ledger, j["id"], semana, dia, next_session_id)
            puntos_totales[j["id"]] += pts
            minutos_totales[j["id"]] += mins
            puntos_por_semana[semana][j["id"]] += pts

        if dia % 7 == 6:
            ranking_semana = sorted(puntos_por_semana[semana].items(), key=lambda kv: -kv[1])
            top5_por_semana.append(tuple(uid for uid, _ in ranking_semana[:5]))

    for user_id, week, source_type, source_id, reason, points, _ in ledger.rows:
        perfil = jugadores[user_id]["perfil"]
        puntos_por_fuente[perfil][source_type] += points

    return jugadores, puntos_totales, minutos_totales, puntos_por_semana, top5_por_semana, puntos_por_fuente


def dense_rank(items):
    """DENSE_RANK (1, 2, 2, 3) sobre puntos desc. LeaderboardService.java:82-100."""
    ordenado = sorted(items, key=lambda kv: -kv[1])
    posiciones = {}
    pos = 0
    prev = None
    for uid, pts in ordenado:
        if pts != prev:
            pos += 1
            prev = pts
        posiciones[uid] = pos
    return posiciones


def _rachas_iguales(seq):
    grupo = []
    for x in seq:
        if grupo and x != grupo[-1]:
            yield grupo
            grupo = []
        grupo.append(x)
    if grupo:
        yield grupo


def reporte(jugadores, puntos_totales, minutos_totales, puntos_por_semana, top5, puntos_por_fuente, semanas):
    por_perfil = defaultdict(list)
    for j in jugadores:
        por_perfil[j["perfil"]].append(j["id"])

    print(f"{'perfil':<10} {'n':>4} {'pts total med':>13} {'pts/min invertido':>18}")
    med_pts = {}
    med_rate = {}
    for perfil, ids in sorted(por_perfil.items()):
        pts = [puntos_totales[uid] for uid in ids]
        rates = [puntos_totales[uid] / minutos_totales[uid] for uid in ids if minutos_totales[uid] > 0]
        med_pts[perfil] = statistics.median(pts) if pts else 0
        med_rate[perfil] = statistics.median(rates) if rates else 0
        print(f"{perfil:<10} {len(ids):>4} {med_pts[perfil]:>13.0f} {med_rate[perfil]:>18.2f}")

    print("\nSeñales")

    if "farmer" in med_pts and med_pts.get("intenso"):
        print(f"- Puntos totales: farmer / intenso = {med_pts['farmer'] / med_pts['intenso']:.2f}"
              f"  (puntos acumulados en {semanas} semanas)")
    if "farmer" in med_rate and med_rate.get("intenso"):
        print(f"- Eficiencia (puntos por minuto REAL invertido): farmer / intenso = "
              f"{med_rate['farmer'] / med_rate['intenso']:.2f}"
              f"  <- esta es la señal que importa, no el total acumulado")

    print("\n- Puntos por fuente (SESSION vs QUIZ), por perfil:")
    for perfil in sorted(puntos_por_fuente):
        fuentes = puntos_por_fuente[perfil]
        total = sum(fuentes.values()) or 1
        partes = ", ".join(f"{k}={100*v/total:.0f}%" for k, v in sorted(fuentes.items()))
        print(f"  {perfil:<10} {partes}")

    sin_cambio = max((len(list(g)) for g in _rachas_iguales(top5)), default=0)
    print(f"\n- Ranking semanal: máximo de semanas seguidas con el mismo top 5 = {sin_cambio} de {semanas}"
          f"  (el ranking resetea cada lunes, WeekService.java:31-42: no es acumulativo)")

    if "tardio" in por_perfil and "constante" in por_perfil:
        alcanza = None
        for s in range(semanas):
            if s < PERFILES["tardio"]["alta"]:
                continue
            t = statistics.median(puntos_por_semana[s].get(uid, 0) for uid in por_perfil["tardio"])
            c = statistics.median(puntos_por_semana[s].get(uid, 0) for uid in por_perfil["constante"])
            if t >= c:
                alcanza = s + 1
                break
        print(f"- El 'tardío' empata la mediana semanal del 'constante' en la semana: {alcanza or 'nunca'}"
              f"  (como el ranking es semanal, no cumulativo, compite en igualdad apenas empieza)")

    total_general = sum(puntos_totales.values()) or 1
    top10 = sorted(puntos_totales.values(), reverse=True)[: max(1, len(jugadores) // 10)]
    print(f"- Concentración: el top 10% de usuarios tiene el {100 * sum(top10) / total_general:.0f}% "
          f"de los puntos acumulados en {semanas} semanas")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--semanas", type=int, default=16)
    ap.add_argument("--usuarios", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    resultado = simular(a.semanas, a.usuarios, a.seed)
    reporte(*resultado, a.semanas)
