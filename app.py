from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['Ecuapronos']

# ==========================================
# FUNCIÓN DE CÁLCULO DE PUNTOS
# ==========================================
def calcular_puntuacion(goles_l_pron, goles_v_pron, goles_l_real, goles_v_real):
    """
    Reglas de puntaje:
    - 3 puntos: Marcador exacto.
    - 1 punto: Acertar ganador o empate (sin atinar el marcador exacto).
    - 0 puntos: Sin acierto o partido no jugado.
    """
    if goles_l_real is None or goles_v_real is None:
        return 0
    
    # 1. Marcador Exacto -> 3 Puntos
    if goles_l_pron == goles_l_real and goles_v_pron == goles_v_real:
        return 3
    
    # 2. Acertar Tendencia (Ganador/Empate) -> 1 Punto
    signo_pron = 1 if goles_l_pron > goles_v_pron else (-1 if goles_l_pron < goles_v_pron else 0)
    signo_real = 1 if goles_l_real > goles_v_real else (-1 if goles_l_real < goles_v_real else 0)
    
    if signo_pron == signo_real:
        return 1
        
    return 0


# ==========================================
# RUTAS DE VISTAS (PÁGINAS HTML)
# ==========================================

@app.route('/')
def index():
    torneo_seleccionado = request.args.get('torneo', 'LigaPro')
    
    if torneo_seleccionado == 'Libertadores':
        partidos = list(db.partidos.find({"torneo": {"$regex": "libertadores", "$options": "i"}}, {'_id': False}))
    elif torneo_seleccionado == 'Champions':
        partidos = list(db.partidos.find({"torneo": {"$regex": "champions", "$options": "i"}}, {'_id': False}))
    else:
        partidos = list(db.partidos.find({"$or": [{"torneo": {"$regex": "ligapro", "$options": "i"}}, {"torneo": {"$exists": False}}]}, {'_id': False}))

    grupos = list(db.grupos.find({}, {'_id': False}))
    return render_template('index.html', partidos=partidos, grupos=grupos, torneo_activo=torneo_seleccionado)


@app.route('/registros')
def vista_registros():
    return render_template('registros.html')


@app.route('/grupos')
def vista_grupos():
    lista_grupos = list(db.grupos.find({}, {'_id': False}))
    
    # Recalcular puntos y ordenar miembros por ranking en cada grupo
    for g in lista_grupos:
        miembros_procesados = []
        if 'miembros' in g and isinstance(g['miembros'], list):
            for m in g['miembros']:
                # Extraer cédula según el tipo de dato guardado en MongoDB
                if isinstance(m, dict):
                    cedula_m = str(m.get('cedula'))
                    nombre_m = m.get('nombre', f'Usuario {cedula_m}')
                    rol_m = m.get('rol', 'miembro')
                else:
                    cedula_m = str(m)
                    usuario_db = db.usuarios.find_one({"cedula": cedula_m})
                    nombre_m = usuario_db.get('nombre') if usuario_db and 'nombre' in usuario_db else f'Usuario {cedula_m}'
                    rol_m = 'admin' if cedula_m == str(g.get('creador_cedula')) else 'miembro'

                # Calcular puntos acumulados de los pronósticos de este miembro
                pronosticos = list(db.pronosticos.find({"$or": [{"cedula": cedula_m}, {"cedula_usuario": cedula_m}]}))
                total_pts = 0
                
                for p in pronosticos:
                    partido = db.partidos.find_one({"partido_id": p.get('partido_id')})
                    if partido and partido.get('estado') == 'FINALIZADO':
                        res_real = partido.get('resultado_real', {})
                        # Compatibilidad con estructura prediccion
                        pred = p.get('prediccion', {})
                        g_local_p = pred.get('goles_local') if 'goles_local' in pred else p.get('goles_local', 0)
                        g_vis_p = pred.get('goles_visitante') if 'goles_visitante' in pred else p.get('goles_visitante', 0)
                        
                        pts = calcular_puntuacion(
                            int(g_local_p), int(g_vis_p),
                            res_real.get('goles_local'), res_real.get('goles_visitante')
                        )
                        total_pts += pts

                miembros_procesados.append({
                    "cedula": cedula_m,
                    "nombre": nombre_m,
                    "rol": rol_m,
                    "puntos_totales": total_pts
                })

            # Ordenar miembros descendentemente por puntos (Ranking)
            g['miembros'] = sorted(miembros_procesados, key=lambda x: x['puntos_totales'], reverse=True)

    return render_template('grupos.html', grupos=lista_grupos)


@app.route('/perfil')
def vista_perfil():
    cedula = request.args.get('cedula', '').strip()
    
    if not cedula:
        return render_template('perfil.html', usuario=None, pronosticos=[], puntos_totales=0, efectividad=0, cedula_buscada="")
    
    # Buscar si el usuario existe en la base de datos
    usuario = db.usuarios.find_one({"cedula": cedula}, {'_id': False})
    
    # Si la cédula no está registrada, redirigir automáticamente a /registros
    if not usuario:
        return redirect(url_for('vista_registros'))
    
    pronosticos_usuario = []
    pron_raw = list(db.pronosticos.find({"$or": [{"cedula": cedula}, {"cedula_usuario": cedula}]}))
    
    for p in pron_raw:
        partido = db.partidos.find_one({"partido_id": p.get('partido_id')})
        if partido:
            res_real = partido.get('resultado_real', {})
            pred = p.get('prediccion', {})
            g_local_p = pred.get('goles_local') if 'goles_local' in pred else p.get('goles_local', 0)
            g_vis_p = pred.get('goles_visitante') if 'goles_visitante' in pred else p.get('goles_visitante', 0)
            
            es_finalizado = partido.get('estado') == 'FINALIZADO'
            pts = calcular_puntuacion(
                int(g_local_p), int(g_vis_p),
                res_real.get('goles_local'), res_real.get('goles_visitante')
            ) if es_finalizado else 0
            
            pronosticos_usuario.append({
                "partido": f"{partido.get('equipo_local')} vs {partido.get('equipo_visitante')}",
                "torneo": partido.get('torneo', 'LigaPro'),
                "pronostico": f"{g_local_p} - {g_vis_p}",
                "resultado_real": f"{res_real.get('goles_local', '-')} - {res_real.get('goles_visitante', '-')}" if es_finalizado else "Pendiente",
                "estado": partido.get('estado'),
                "puntos": pts
            })

    puntos_totales = sum(item['puntos'] for item in pronosticos_usuario)
    total_finalizados = sum(1 for item in pronosticos_usuario if item['estado'] == 'FINALIZADO')
    efectividad = round((puntos_totales / (total_finalizados * 3)) * 100, 1) if total_finalizados > 0 else 0

    return render_template('perfil.html', 
                           usuario=usuario, 
                           pronosticos=pronosticos_usuario, 
                           puntos_totales=puntos_totales, 
                           efectividad=efectividad,
                           cedula_buscada=cedula)

# ==========================================
# ENDPOINTS API REST
# ==========================================

# 1. Registrar Usuario
@app.route('/api/usuarios', methods=['POST'])
def register_user():
    data = request.json
    password_encriptada = generate_password_hash(data.get('password'))
    
    nuevo_usuario = {
        "cedula": str(data.get('cedula')),
        "nombre": data.get('nombre'),
        "username": data.get('username'),
        "email": data.get('email'),
        "password": password_encriptada,
        "rol": "usuario",
        "estado": "activo",
        "fecha_registro": datetime.utcnow()
    }
    db.usuarios.insert_one(nuevo_usuario)
    return jsonify({"message": "¡Usuario registrado con éxito en Ecuapronos!", "status": "success"}), 201


# 2. Crear Grupo (Validando que la cédula del creador exista)
@app.route('/api/grupos', methods=['POST'])
def crear_grupo():
    data = request.json
    creador = str(data.get('creador_cedula', '')).strip()
    nombre_grupo = data.get('nombre_grupo', '').strip()
    codigo_invitacion = data.get('codigo_invitacion', '').strip()

    if not creador or not nombre_grupo or not codigo_invitacion:
        return jsonify({"message": "Todos los campos son obligatorios", "status": "error"}), 400

    # Verificar si la cédula del creador está registrada en la base de datos
    usuario_existe = db.usuarios.find_one({"cedula": creador})
    if not usuario_existe:
        return jsonify({
            "message": "Cédula no registrada. Debes registrarte primero para crear un grupo.",
            "status": "not_registered",
            "redirect_url": "/registros"
        }), 403

    # Verificar si el código de invitación ya está en uso
    codigo_existente = db.grupos.find_one({"codigo_invitacion": codigo_invitacion})
    if codigo_existente:
        return jsonify({"message": "El código de invitación ya existe. Usa otro diferente.", "status": "error"}), 400

    nuevo_grupo = {
        "nombre_grupo": nombre_grupo,
        "codigo_invitacion": codigo_invitacion,
        "creador_cedula": creador,
        "miembros": [creador],
        "fecha_creacion": datetime.utcnow()
    }
    
    db.grupos.insert_one(nuevo_grupo)
    return jsonify({"message": "¡Grupo creado con éxito!", "status": "success"}), 201


# 3. Unirse a un Grupo existente por Código de Invitación (Validando si el usuario existe)
@app.route('/api/grupos/unirse', methods=['POST'])
def unirse_grupo():
    data = request.json
    codigo = data.get('codigo_invitacion')
    cedula = str(data.get('cedula')).strip()
    
    if not cedula:
        return jsonify({"message": "La cédula es obligatoria", "status": "error"}), 400

    # Verificar si el usuario está registrado en la base de datos
    usuario_existe = db.usuarios.find_one({"cedula": cedula})
    if not usuario_existe:
        return jsonify({
            "message": "Usuario no registrado. Debes registrarte primero.",
            "status": "not_registered",
            "redirect_url": "/registros"
        }), 403

    # Si existe, lo unimos al grupo
    resultado = db.grupos.update_one(
        {"codigo_invitacion": codigo},
        {"$addToSet": {"miembros": cedula}}
    )
    
    if resultado.modified_count > 0 or resultado.matched_count > 0:
        return jsonify({"message": "¡Te has unido al grupo correctamente!", "status": "success"}), 200
    
    return jsonify({"message": "Código de grupo no encontrado", "status": "error"}), 404

# 4. Registrar Pronóstico (Validando si el usuario existe)
@app.route('/api/pronosticos', methods=['POST'])
def guardar_pronostico():
    data = request.json
    cedula = str(data.get('cedula_usuario') or data.get('cedula')).strip()
    
    if not cedula:
        return jsonify({"message": "La cédula es obligatoria", "status": "error"}), 400

    # Verificar si el usuario está registrado en la base de datos
    usuario_existe = db.usuarios.find_one({"cedula": cedula})
    if not usuario_existe:
        return jsonify({
            "message": "Usuario no registrado. Redirigiendo al registro...",
            "status": "not_registered",
            "redirect_url": "/registros"
        }), 403

    # Si está registrado, guardamos el pronóstico
    nuevo_pronostico = {
        "cedula": cedula,
        "cedula_usuario": cedula,
        "partido_id": data.get('partido_id'),
        "goles_local": int(data.get('goles_local', 0)),
        "goles_visitante": int(data.get('goles_visitante', 0)),
        "prediccion": {
            "goles_local": int(data.get('goles_local', 0)),
            "goles_visitante": int(data.get('goles_visitante', 0))
        },
        "puntos_ganados": 0,
        "fecha_pronostico": datetime.utcnow()
    }
    
    db.pronosticos.insert_one(nuevo_pronostico)
    return jsonify({"message": "¡Pronóstico guardado con éxito!", "status": "success"}), 201


# ==========================================
# INTERACCIÓN DENTRO DE GRUPOS (CHAT / MURO)
# ==========================================

# Endpoint para enviar un mensaje al grupo
@app.route('/api/grupos/mensaje', methods=['POST'])
def enviar_mensaje_grupo():
    data = request.json
    codigo_invitacion = data.get('codigo_invitacion')
    cedula = str(data.get('cedula')).strip()
    mensaje_texto = data.get('mensaje', '').strip()

    if not cedula or not mensaje_texto:
        return jsonify({"message": "La cédula y el mensaje son obligatorios", "status": "error"}), 400

    usuario = db.usuarios.find_one({"cedula": cedula})
    if not usuario:
        return jsonify({"message": "Debes estar registrado para comentar", "status": "not_registered", "redirect_url": "/registros"}), 403

    nuevo_mensaje = {
        "codigo_invitacion": codigo_invitacion,
        "cedula_usuario": cedula,
        "nombre_usuario": usuario.get('nombre', 'Usuario'),
        "username": usuario.get('username', 'usuario'),
        "mensaje": mensaje_texto,
        "fecha": datetime.utcnow()
    }

    db.mensajes_grupo.insert_one(nuevo_mensaje)
    return jsonify({"message": "Mensaje publicado con éxito", "status": "success"}), 201


# 5.Endpoint para obtener los mensajes de un grupo
@app.route('/api/grupos/mensajes/<codigo_invitacion>', methods=['GET'])
def obtener_mensajes_grupo(codigo_invitacion):
    mensajes_raw = list(db.mensajes_grupo.find({"codigo_invitacion": codigo_invitacion}, {'_id': False}).sort("fecha", 1))
    return jsonify({"mensajes": mensajes_raw, "status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)