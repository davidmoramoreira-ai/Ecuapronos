from pymongo import MongoClient
from datetime import datetime

# Conexión a tu MongoDB local
client = MongoClient('mongodb://localhost:27017/')
db = client['Ecuapronos']

# Lista de partidos de la LigaPro Ecuador
partidos_ligapro = [
    # JORNADA ANTERIOR - FINALIZADOS CON MARCADOR REAL
    {
        "partido_id": "LP-101",
        "torneo": "LigaPro",
        "jornada": 14,
        "equipo_local": "Liga de Quito",
        "equipo_visitante": "Emelec",
        "fecha_hora_partido": datetime(2026, 10, 10, 18, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 2, "goles_visitante": 1}
    },
    {
        "partido_id": "LP-102",
        "torneo": "LigaPro",
        "jornada": 14,
        "equipo_local": "Barcelona SC",
        "equipo_visitante": "El Nacional",
        "fecha_hora_partido": datetime(2026, 10, 11, 16, 30),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 3, "goles_visitante": 0}
    },
    {
        "partido_id": "LP-103",
        "torneo": "LigaPro",
        "jornada": 14,
        "equipo_local": "Independiente del Valle",
        "equipo_visitante": "Universidad Católica",
        "fecha_hora_partido": datetime(2026, 10, 11, 19, 0),
        "estado": "FINALIZADO",
        "resultado_real": {"goles_local": 1, "goles_visitante": 1}
    },

    # PRÓXIMA JORNADA - PROGRAMADOS PARA PRONOSTICAR
    {
        "partido_id": "LP-104",
        "torneo": "LigaPro",
        "jornada": 15,
        "equipo_local": "Barcelona SC",
        "equipo_visitante": "Liga de Quito",
        "fecha_hora_partido": datetime(2026, 10, 24, 18, 0),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "LP-105",
        "torneo": "LigaPro",
        "jornada": 15,
        "equipo_local": "Emelec",
        "equipo_visitante": "Independiente del Valle",
        "fecha_hora_partido": datetime(2026, 10, 25, 15, 30),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    },
    {
        "partido_id": "LP-106",
        "torneo": "LigaPro",
        "jornada": 15,
        "equipo_local": "El Nacional",
        "equipo_visitante": "Delfín SC",
        "fecha_hora_partido": datetime(2026, 10, 25, 18, 0),
        "estado": "PROGRAMADO",
        "resultado_real": {"goles_local": None, "goles_visitante": None}
    }
]

# Limpiar partidos antiguos de LigaPro e insertar los nuevos
db.partidos.delete_many({"torneo": {"$regex": "ligapro", "$options": "i"}})
resultado = db.partidos.insert_many(partidos_ligapro)

print(f"¡Éxito! Se insertaron {len(resultado.inserted_ids)} partidos de LigaPro Ecuador en MongoDB.")
