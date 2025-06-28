# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, PanicLog, User, Message

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

# 🚨 Botón de Pánico — real y funcional
@home_bp.route('/panico', methods=['GET', 'POST'])
@login_required
def panico():
    if request.method == 'POST':
        # Mensaje automático
        panic_message = f"{current_user.username} necesita conversar, está pasando un momento difícil."

        # Guardar en la base de datos
        log = PanicLog(user_id=current_user.id, message=panic_message)
        db.session.add(log)
        db.session.commit()

        # Buscar últimos contactos (simulado)
        recent_receivers = (
            db.session.query(User)
            .join(Message, Message.receiver_id == User.id)
            .filter(Message.sender_id == current_user.id)
            .order_by(Message.timestamp.desc())
            .distinct(User.id)
            .limit(5)
            .all()
        )

        # Simular notificación push
        for friend in recent_receivers:
            print(f"Notificación push a {friend.username}: {panic_message}")

        flash('Botón de Pánico activado. Tus contactos recibirán una alerta.')
        return redirect(url_for('home.home'))

    return render_template('panico.html')

# Música
@home_bp.route('/musica')
@login_required
def musica():
    return "<h3>🎵 Playlist Musical en desarrollo</h3>"

# IA de Apoyo
@home_bp.route('/ia')
@login_required
def ia():
    return "<h3>🤖 Asistente IA en desarrollo</h3>"

# ⚙️ Configuración
@home_bp.route('/config')
@login_required
def config():
    return "<h3>⚙️ Configuración en desarrollo</h3>"

# Ruta de prueba pública
@home_bp.route('/prueba')
def prueba():
    return "<h1>✅ Ruta de prueba pública funcionando</h1>"


