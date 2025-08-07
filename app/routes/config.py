# app/routes/config.py

import os
import uuid
import cloudinary
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, User
from flask_babel import _

# === Configurar Cloudinary ===
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

config_bp = Blueprint('config', __name__)

UPLOAD_FOLDER = os.path.join('app', 'static', 'profile_pics')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@config_bp.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    user = User.query.get(current_user.id)

    if request.method == 'POST':
        # === Actualizar Bio ===
        bio = request.form.get('bio')
        if bio is not None:
            bio = bio.strip()
            if len(bio) > 300:
                flash(_('La bio no puede tener más de 300 caracteres.'), 'danger')
                return redirect(url_for('config.config'))
            user.bio = bio

        # === Botón "Borrar foto" ===
        if 'delete_photo' in request.form:
            if user.profile_picture and 'cloudinary' in user.profile_picture:
                public_id = user.profile_picture.rsplit('/', 1)[-1].split('.')[0]
                try:
                    cloudinary.uploader.destroy(public_id)
                except Exception:
                    pass  # No romper el flujo si falla
            user.profile_picture = 'default.png'
            db.session.commit()
            flash(_('Foto de perfil eliminada.'), 'success')
            return redirect(url_for('config.config'))

        # === Nueva imagen de perfil ===
        file = request.files.get('profile_picture')
        if file and file.filename:
            if not allowed_file(file.filename):
                flash(_('Solo se permiten imágenes: png, jpg, jpeg, gif.'), 'danger')
                return redirect(url_for('config.config'))

            # Validación de tamaño
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0)
            if file_length > MAX_FILE_SIZE:
                flash(_('La imagen excede el tamaño máximo de 10 MB.'), 'danger')
                return redirect(url_for('config.config'))

            try:
                # ✅ Subir a Cloudinary
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder='espacio_seguro/perfiles',
                    transformation=[{'quality': 'auto', 'fetch_format': 'auto'}]
                )
                user.profile_picture = upload_result['secure_url']
                flash(_('Imagen subida a Cloudinary correctamente.'), 'success')
            except Exception as e:
                # 🧱 Fallback local
                flash(_('Error al subir a Cloudinary: %(err)s. Guardando localmente.', err=str(e)), 'warning')
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"
                upload_folder_abs = os.path.join(current_app.root_path, 'static/profile_pics')
                if not os.path.exists(upload_folder_abs):
                    os.makedirs(upload_folder_abs)
                filepath = os.path.join(upload_folder_abs, filename)
                file.save(filepath)
                user.profile_picture = filename
                flash(_('Imagen guardada localmente.'), 'success')

        db.session.commit()
        flash(_('Perfil actualizado correctamente.'), 'success')
        return redirect(url_for('config.config'))

    # Al mostrar la página, incluimos las publicaciones y las historias del usuario
    from app.models import Post, Story
    from sqlalchemy import desc
    publicaciones = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.timestamp)).all()
    historias = Story.query.filter_by(user_id=current_user.id).order_by(desc(Story.timestamp)).all()
    return render_template('config.html', user=user, publicaciones=publicaciones, historias=historias)


@config_bp.route('/perfil/<string:username>')
@login_required
def perfil(username):
    """
    Muestra el perfil público de otro usuario o del propio.  Incluye
    su foto de perfil, biografía, historias y publicaciones.  La
    información es de sólo lectura; la edición se realiza en
    /config.
    """
    user_profile = User.query.filter_by(username=username).first_or_404()
    from app.models import Post, Story
    from sqlalchemy import desc
    publicaciones = Post.query.filter_by(user_id=user_profile.id).order_by(desc(Post.timestamp)).all()
    historias = Story.query.filter_by(user_id=user_profile.id).order_by(desc(Story.timestamp)).all()

    # Determinar la relación de amistad entre el usuario actual y el perfil mostrado
    from app.models import FriendRequest
    status = 'none'
    pending_request_id = None
    if user_profile.id != current_user.id:
        fr = FriendRequest.query.filter(
            ((FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == user_profile.id)) |
            ((FriendRequest.sender_id == user_profile.id) & (FriendRequest.receiver_id == current_user.id))
        ).first()
        if fr:
            if fr.status == 'accepted':
                status = 'friend'
            elif fr.status == 'pending':
                # Si yo envié la solicitud
                if fr.sender_id == current_user.id:
                    status = 'sent'
                else:
                    status = 'received'
                    pending_request_id = fr.id
    return render_template(
        'perfil.html',
        perfil=user_profile,
        publicaciones=publicaciones,
        historias=historias,
        friend_status=status,
        pending_request_id=pending_request_id
    )
