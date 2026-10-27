from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Ecuapronos']

# Limpiamos toda la colección de partidos para empezar frescos
db.partidos.delete_many({})

# Lista completa y unificada de todos los torneos
todos_los_partidos = [
    # --- LIGAPRO ECUADOR ---
    {
        "partido_id": "LP-001",
        "torneo": "LigaPro",
        "jornada": 1,
        "equipo_local": "Liga de Quito",
        "equipo_visitante": "Independiente del Valle",
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "LP-002",
        "torneo": "LigaPro",
        "jornada": 1,
        "equipo_local": "Barcelona SC",
        "equipo_visitante": "Emelec",
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },

    # --- CHAMPIONS LEAGUE ---
    {
        "partido_id": "CHAMP-001",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Real Madrid",
        "equipo_visitante": "AS Roma",
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 4, "goles_visitante": 3}
    },
    {
        "partido_id": "CHAMP-002",
        "torneo": "Champions",
        "jornada": 2,
        "equipo_local": "Manchester City",
        "equipo_visitante": "PSG",
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 2, "goles_visitante": 4}
    },
    {
        "partido_id": "CHAMP-003",
        "torneo": "Champions",
        "jornada": 3,
        "equipo_local": "PSG",
        "equipo_visitante": "FC Barcelona",
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },

    # --- COPA LIBERTADORES ---
    {
        "partido_id": "LIB-001",
        "torneo": "Libertadores",
        "jornada": "Semifinal - Ida",
        "equipo_local": "River Plate",
        "equipo_visitante": "Flamengo",
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 2, "goles_visitante": 1}
    },
    {
        "partido_id": "LIB-002",
        "torneo": "Libertadores",
        "jornada": "Semifinal - Ida",
        "equipo_local": "Palmeiras",
        "equipo_visitante": "Boca Juniors",
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 1, "goles_visitante": 1}
    },
    {
        "partido_id": "LIB-003",
        "torneo": "Libertadores",
        "jornada": "Semifinal - Vuelta",
        "equipo_local": "Flamengo",
        "equipo_visitante": "River Plate",
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "LIB-004",
        "torneo": "Libertadores",
        "jornada": "Semifinal - Vuelta",
        "equipo_local": "Boca Juniors",
        "equipo_visitante": "Palmeiras",
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    }
]

# Insertar todos en la base de datos
resultado = db.partidos.insert_many(todos_los_partidos)
print(f"¡Éxito total! Se insertaron {len(resultado.inserted_ids)} partidos de todos los torneos.")