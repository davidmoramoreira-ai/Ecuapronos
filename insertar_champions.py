from pymongo import MongoClient
from datetime import datetime

# 1. Conexión a tu MongoDB local
client = MongoClient('mongodb://localhost:27017/')
db = client['Ecuapronos']

# 2. Lista completa de partidos de Champions
partidos_champions = [
    # JORNADA 2 - FINALIZADOS CON MARCADOR REAL
    {
        "partido_id": "CHAMP-001",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Real Madrid",
        "equipo_visitante": "AS Roma",
        "fecha_hora_partido": datetime(2026, 10, 14, 14, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 4, "goles_visitante": 3}
    },
    {
        "partido_id": "CHAMP-002",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Manchester City",
        "equipo_visitante": "PSG",
        "fecha_hora_partido": datetime(2026, 10, 14, 14, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 2, "goles_visitante": 4}
    },
    {
        "partido_id": "CHAMP-003",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Arsenal",
        "equipo_visitante": "Lille",
        "fecha_hora_partido": datetime(2026, 10, 13, 14, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 3, "goles_visitante": 0}
    },
    {
        "partido_id": "CHAMP-004",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Galatasaray",
        "equipo_visitante": "FC Barcelona",
        "fecha_hora_partido": datetime(2026, 10, 13, 14, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 1, "goles_visitante": 4}
    },

    # JORNADA 3 - PROGRAMADOS PARA PRONOSTICAR
    {
        "partido_id": "CHAMP-005",
        "torneo": "Champions",
        "jornada": 3,
        "equipo_local": "PSG",
        "equipo_visitante": "FC Barcelona",
        "fecha_hora_partido": datetime(2026, 10, 20, 14, 0),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "CHAMP-006",
        "torneo": "Champions",
        "jornada": 3,
        "equipo_local": "Real Madrid",
        "equipo_visitante": "RB Leipzig",
        "fecha_hora_partido": datetime(2026, 10, 21, 14, 0),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "CHAMP-007",
        "torneo": "Champions",
        "jornada": 3,
        "equipo_local": "Bayern de Múnich",
        "equipo_visitante": "Arsenal",
        "fecha_hora_partido": datetime(2026, 10, 21, 14, 0),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    }
]

# 3. Limpiar los antiguos de Champions e insertar los nuevos
db.partidos.delete_many({"torneo": "Champions"})
resultado = db.partidos.insert_many(partidos_champions)

print(f"¡Éxito! Se insertaron {len(resultado.inserted_ids)} partidos de Champions League en MongoDB.")