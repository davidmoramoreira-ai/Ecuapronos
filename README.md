# Ecuapronos

Ecuapronos es una aplicación web full-stack diseñada para la gestión y participación en quinielas deportivas competitivas. La plataforma permite a los usuarios registrarse, pronosticar marcadores de partidos de fútbol de diversas competiciones (como LigaPro, Copa Libertadores y UEFA Champions League) y competir en tablas de clasificación en tiempo real basadas en la precisión de sus predicciones.

Arquitectura y Tecnologías Utilizadas
Backend
Python: Lenguaje principal para la lógica del servidor.

Flask: Framework web ligero para el enrutamiento, controladores y gestión de peticiones HTTP.

PyMongo / Flask-PyMongo: Controlador para la conexión y manipulación de datos en MongoDB.

Base de Datos
MongoDB: Base de datos NoSQL orientada a documentos, utilizada para almacenar de forma flexible usuarios, partidos, pronósticos, grupos y puntajes.

Frontend
HTML5 y CSS3: Estructura semántica y diseño visual dinámico con interfaz en modo oscuro (dark mode).

JavaScript (Vanilla / ES6+): Manipulación del DOM, validación de formularios dinámicos y envío/recepción de datos mediante peticiones asíncronas (fetch).

Características e Implementaciones Principales
1. Autenticación y Gestión de Usuarios
Sistema de registro de usuarios e inicio de sesión seguro.

Control de sesiones activas mediante el manejo de estado en servidor/cookies.

Perfiles individuales donde cada usuario visualiza sus estadísticas, historial de predicciones y puntos acumulados.

2. Módulo de Pronósticos Dinámicos
Formulario interactivo para el ingreso y modificación de marcadores predichos antes del inicio de cada encuentro.

Reglas de validación para evitar el ingreso o modificación de pronósticos una vez iniciado o finalizado un partido.

3. Automatización de Escudos y Equipos
Scripts automatizados para la integración, descarga e inserción de logotipos y escudos de equipos de fútbol para mantener la interfaz actualizada e intuitiva.

4. Tablas de Clasificación y Puntuación
Sistema dinámico de cálculo de puntos que evalúa el resultado exacto vs. el ganador/empate pronosticado.

Tabla de posiciones global y por grupos en tiempo real para fomentar la competencia entre los participantes.

5. Cobertura de Competiciones
Estructura adaptable para almacenar y clasificar fixtures correspondientes a distintas ligas e torneos (LigaPro Ecuador, Copa Libertadores, UEFA Champions League).
