from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Ecuapronos']

# Diccionario con URLs directas y funcionales en PNG
logos_equipos = {
    # LIGAPRO (ECUADOR)
    "Liga de Quito": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg50P43l5ThCvnsdymdq0yUL1cUYXkSy7yP1I7ecM4Fg&s=10",
    "Barcelona SC": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEG8170G3s5xFrizMcD3UHUuPZc81J9tijPxXSfD85iA&s=10",
    "Independiente del Valle": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbbxO9LjC-LEFZ_N9emOo-tta3vePqbFcg8db0KSe2Wg&s=10",
    "Universidad Católica": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2YkzfQuZ0QqEappgD_5IkxJNW-89Ggcs-qDujvIUVWg&s=10",
    "El Nacional": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJ9JXY8cz4U8PEr1yLlGSJTon3GukXAzDg4hhFCSpoIw&s=10",
    "Delfín SC": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq0VSxmhN51WGazuFwiIGpRuNH4VH1hx-PhGhZIDXXNQ&s=10",
    "Emelec": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwsMa-AvRfUPl9h4OyXxdfGhNzmM7oly3DKsqU6vJwNA&s=10",

    # LIBERTADORES
    "River Plate": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTO8JDzKZb0RFmcU1lMYhJ6SbuT0Po5L4ZlX6sZhIweQ&s=10",
    "Flamengo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjncqP_vYUhiaIaEZNUFydX9ZjLKLBE7Q6TZEFEOaKhw&s=10",
    "Palmeiras": "https://upload.wikimedia.org/wikipedia/commons/1/10/Palmeiras_logo.svg",
    "Boca Juniors": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5ulp4UNbA0C9x4V1ZwGklosxOeho6jdlbsPJBaKosww&s",

    # CHAMPIONS LEAGUE
    "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    "AS Roma": "https://upload.wikimedia.org/wikipedia/en/f/f7/AS_Roma_logo_%282017%29.svg",
    "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "PSG": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
    "FC Barcelona": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg"
}

print("🔄 Actualizando los escudos en MongoDB...")

actualizados = 0
for partido in db.partidos.find({}):
    eq_local = partido.get("equipo_local", "").strip()
    eq_visitante = partido.get("equipo_visitante", "").strip()
    
    update_data = {}
    if eq_local in logos_equipos:
        update_data["logo_local"] = logos_equipos[eq_local]
    if eq_visitante in logos_equipos:
        update_data["logo_visitante"] = logos_equipos[eq_visitante]
        
    if update_data:
        db.partidos.update_one(
            {"partido_id": partido.get("partido_id")},
            {"$set": update_data}
        )
        actualizados += 1

print(f"✅ ¡Escudos actualizados correctamente en {actualizados} partidos!")