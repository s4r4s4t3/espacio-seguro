# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from ..models import db, PanicLog, User, Message, Post
from flask_babel import _
from sqlalchemy import desc
import cloudinary.uploader

home_bp = Blueprint('home', __name__)

# 🌍 Landing pública
@home_bp.route('/')
def landing():
    return render_template("landing.html")

# 🌐 Selección de idioma (cookie)
@home_bp.route('/set_language/<lang_code>')
def set_language(lang_code):
    supported = ['es', 'en', 'pt', 'br', 'de', 'fr', 'it']
    lang = lang_code if lang_code in supported else 'es'
    resp = make_response(redirect(request.referrer or url_for('home.landing')))
    resp.set_cookie('lang', lang, max_age=30*24*60*60)
    return resp

# 👋 Bienvenida (primera vez, aceptación de términos)
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

# 🏠 Dashboard
@home_bp.route('/home')
@login_required
def home():
    """
    Página de inicio para usuarios autenticados. En lugar de mostrar un dashboard
    separado con navegación duplicada, redirigimos directamente al feed.
    """
    return redirect(url_for('home.feed'))

# 💬 Chat global (compatibilidad con ruta antigua)
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

        # Opcional: notificar a los últimos contactos (real o con push simulado)
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

    return render_template('panico.html', user=current_user)

# 📰 Feed del usuario (privado)
@home_bp.route('/feed')
@login_required
def feed():
    publicaciones = Post.query.order_by(desc(Post.timestamp)).all()
    return render_template("feed.html", publicaciones=publicaciones, user=current_user)

# 📝 Nueva publicación
@home_bp.route('/nueva_publicacion', methods=['GET', 'POST'])
@login_required
def nueva_publicacion():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if not content:
            flash(_('El contenido no puede estar vacío.'), 'warning')
            return redirect(url_for('home.nueva_publicacion'))

        image = request.files.get('image')
        image_url = None
        if image and image.filename:
            try:
                upload_result = cloudinary.uploader.upload(image)
                image_url = upload_result['secure_url']
            except Exception as e:
                print("Error al subir imagen:", e)
                flash(_('Error al subir la imagen.'), 'danger')
                return redirect(url_for('home.nueva_publicacion'))

        nuevo_post = Post(content=content, image_url=image_url, user_id=current_user.id)
        db.session.add(nuevo_post)
        db.session.commit()
        flash(_('✅ Publicación creada con éxito.'), 'success')
        return redirect(url_for('home.feed'))

    return render_template("nueva_publicacion.html", user=current_user)
