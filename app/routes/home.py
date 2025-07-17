# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from ..models import db, PanicLog, User, Message
from flask_babel import _

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def landing():
    return render_template("landing.html")

# ✅ Ruta robusta para cambiar idioma
@home_bp.route('/set_language/<lang_code>')
def set_language(lang_code):
    supported = ['es', 'en', 'pt', 'br', 'de', 'fr', 'it']
    if lang_code not in supported:
        lang_code = 'es'
    resp = make_response(redirect(request.referrer or url_for('home.landing')))
    resp.set_cookie('lang', lang_code, max_age=30*24*60*60)
    return resp

@home_bp.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.accepted_terms:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        current_user.accepted_terms = True
        db.session.commit()
        flash(_('¡Gracias por aceptar nuestros términos!'), 'success')
        return redirect(url_for('home.home'))

    return render_template("welcome.html", user=current_user)

@home_bp.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@home_bp.route('/chat')
@login_required
def chat():
    return render_template("chat.html", user=current_user)

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

        flash(_('Botón de Pánico activado. Tus contactos recibirán una alerta.'), 'info')
        return redirect(url_for('home.home'))

    return render_template('panico.html')

@home_bp.route('/prueba')
def prueba():
    return "<h1>✅ Ruta de prueba pública funcionando</h1>"
