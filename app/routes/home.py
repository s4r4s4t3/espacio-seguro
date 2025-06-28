from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_bp = Blueprint('home', __name__)

# Ruta raíz → ahora sirve la plantilla home.html y requiere login
@home_bp.route('/')
@login_required
def index():
    return render_template("home.html", user=current_user)

# Alternativa: ruta /home (opcional)
@home_bp.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Chat
@home_bp.route('/chat')
@login_required
def chat():
    return render_template("chat.html", user=current_user)

# Funciones extra (botón de pánico, música, IA, etc.)
@home_bp.route('/panico')
def panico():
    return "<h3>🚨 Botón de Pánico en desarrollo</h3>"

@home_bp.route('/musica')
def musica():
    return "<h3>🎵 Playlist Musical en desarrollo</h3>"

@home_bp.route('/ia')
def ia():
    return "<h3>🤖 Asistente IA en desarrollo</h3>"

#@home_bp.route('/diario')
#def diario():
#    return "<h3>📝 Diario en desarrollo</h3>"

@home_bp.route('/config')
def config():
    return "<h3>⚙️ Configuración en desarrollo</h3>"

# Ruta de prueba pública
@home_bp.route('/prueba')
def prueba():
    return "<h1>✅ Ruta de prueba pública funcionando</h1>"



