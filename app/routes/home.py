# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from ..models import db, PanicLog, User, Message

home_bp = Blueprint('home', __name__)

# 🚩 Landing pública
@home_bp.route('/')
def landing():
    return render_template("landing.html")

# ⚙️ Nueva ruta para cambiar idioma y guardar en cookie
@home_bp.route('/set_language/<lang_code>')
def set_language(lang_code):
    resp = make_response(redirect(request.referrer or url_for('home.landing')))
    resp.set_cookie('lang', lang_code, max_age=30*24*60*60)
    return resp

# Ruta /home → dashboard usuario
@home_bp.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Chat
@home_bp.route('/chat')
@login_required
def chat():
    return render_template("chat.html", user=current_user)

# 🚨 Botón de Pánico
@home_bp.route('/panico', methods=['GET', 'POST'])
@login_required
def panico():
    if request.method == 'POST':
        panic_message = f"{current_user.username} necesita conversar, está pasando un momento difícil."
        log = PanicLog(user_id=current_user.id, message=panic_message)
        db.session.add(log)
        db.session.commit()

        recent_receivers = (
            db.session.query(User)
            .join(Message, Message.receiver_id == User.id)
            .filter(Message.sender_id == current_user.id)
            .order_by(Message.timestamp.desc())
            .distinct(User.id)
            .limit(5)
            .all()
        )

        for friend in recent_receivers:
            print(f"Notificación push a {friend.username}: {panic_message}")

        flash('Botón de Pánico activado. Tus contactos recibirán una alerta.')
        return redirect(url_for('home.home'))

    return render_template('panico.html')

# Ruta de prueba
@home_bp.route('/prueba')
def prueba():
    return "<h1>✅ Ruta de prueba pública funcionando</h1>"




