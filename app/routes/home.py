# app/routes/home.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from ..models import db, PanicLog, User, Message, Post, Story
from flask_babel import _
from sqlalchemy import desc
import cloudinary.uploader

from flask import request  # Para obtener la URL de referencia en eliminaciones

home_bp = Blueprint('home', __name__)

# 🌍 Landing pública
@home_bp.route('/')
def landing():
    return render_template("landing.html")

# 🌐 Selección de idioma (cookie)
@home_bp.route('/set_language/<lang_code>')
def set_language(lang_code):
    """
    Define el idioma de la aplicación mediante una cookie. Algunos códigos
    utilizados en el selector de idioma son alias que deben mapearse a
    un código de idioma real reconocido por Flask‑Babel.  Por ejemplo,
    "br" y "pt" apuntan al portugués de Brasil (pt_BR) ya que los
    archivos de traducción de SafeSpace sólo incluyen esta variante.
    """
    supported = ['es', 'en', 'pt_BR', 'de', 'fr', 'it']
    # Normalizamos alias: "br" y "pt" se mapearán a "pt_BR".  Esto permite
    # que el selector de idioma muestre portugués (Brasil) mediante
    # distintas banderas pero utilice la misma traducción.
    if lang_code in ('br', 'pt', 'pt_BR'):
        lang = 'pt_BR'
    elif lang_code in supported:
        lang = lang_code
    else:
        lang = 'es'
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
    """
    La aplicación ya no tiene un chat global independiente. Para mantener
    compatibilidad con enlaces antiguos o favoritos de los usuarios,
    cualquier visita a esta ruta redirige al feed principal.  El feed
    ofrece el formulario para crear una publicación directamente en la
    parte superior de la lista de publicaciones.
    """
    return redirect(url_for('home.feed'))

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
    """
    Muestra el feed principal para el usuario autenticado.  Incluye
    publicaciones y estados de todos los usuarios ordenados por fecha de
    creación.  Los estados se muestran en una franja horizontal con las
    miniaturas de los usuarios.  Las publicaciones se listan debajo.
    """
    publicaciones = Post.query.order_by(desc(Post.timestamp)).all()
    # Obtenemos todas las historias ordenadas por fecha descendente para
    # mostrarlas en el feed.  Podríamos limitar a las últimas 24h pero
    # por simplicidad mostramos todas.
    historias = Story.query.order_by(desc(Story.timestamp)).all()
    return render_template(
        "feed.html",
        publicaciones=publicaciones,
        historias=historias,
        user=current_user
    )

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

# 🗑️ Eliminar publicación
@home_bp.route('/eliminar_post/<int:post_id>', methods=['POST'])
@login_required
def eliminar_post(post_id):
    """
    Elimina una publicación existente si pertenece al usuario actual.
    También intenta eliminar la imagen asociada de Cloudinary o del
    almacenamiento local cuando corresponde.  Si el usuario no es el
    autor de la publicación se mostrará un mensaje de error.
    """
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash(_('No tienes permiso para eliminar esta publicación.'), 'danger')
        return redirect(request.referrer or url_for('home.feed'))

    # Eliminar imagen remota o local si existe
    if post.image_url:
        if post.image_url.startswith('http'):
            try:
                public_id = post.image_url.rsplit('/', 1)[-1].split('.')[0]
                cloudinary.uploader.destroy(public_id)
            except Exception:
                pass
        else:
            # Fallback: eliminar archivo local en static/post_images
            from flask import current_app
            import os
            local_path = os.path.join(current_app.root_path, 'static', 'post_images', post.image_url)
            if os.path.exists(local_path):
                try:
                    os.remove(local_path)
                except Exception:
                    pass
    db.session.delete(post)
    db.session.commit()
    flash(_('Publicación eliminada.'), 'info')
    return redirect(request.referrer or url_for('home.feed'))
