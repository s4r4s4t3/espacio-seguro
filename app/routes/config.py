# app/routes/config.py

import os
import uuid
import cloudinary
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import db, User

# ✅ Configurar Cloudinary
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
        # ✅ Validar y guardar bio
        bio = request.form.get('bio')
        if bio is not None:
            bio = bio.strip()
            if len(bio) > 300:
                flash('La bio no puede tener más de 300 caracteres.', 'danger')
                return redirect(url_for('config.config'))
            user.bio = bio

        # ✅ Botón para borrar foto
        if 'delete_photo' in request.form:
            if user.profile_picture and 'cloudinary' in user.profile_picture:
                # Intentar borrar de Cloudinary
                public_id = user.profile_picture.rsplit('/', 1)[-1].split('.')[0]
                try:
                    cloudinary.uploader.destroy(public_id)
                except Exception:
                    pass  # No detener flujo si falla
            user.profile_picture = None
            flash('Foto de perfil eliminada.', 'success')
            db.session.commit()
            return redirect(url_for('config.config'))

        # ✅ Validar y guardar imagen nueva
        file = request.files.get('profile_picture')
        if file and file.filename:
            if allowed_file(file.filename):
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0)

                if file_length > MAX_FILE_SIZE:
                    flash('La imagen excede el tamaño máximo de 10 MB.', 'danger')
                    return redirect(url_for('config.config'))

                try:
                    upload_result = cloudinary.uploader.upload(
                        file,
                        transformation=[
                            {'quality': 'auto', 'fetch_format': 'auto'}
                        ]
                    )
                    user.profile_picture = upload_result['secure_url']
                    flash('Imagen subida a Cloudinary correctamente.', 'success')
                except Exception as e:
                    flash(f'Error al subir a Cloudinary: {str(e)}. Guardando localmente.', 'warning')
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    upload_folder_abs = os.path.join(current_app.root_path, 'static/profile_pics')
                    if not os.path.exists(upload_folder_abs):
                        os.makedirs(upload_folder_abs)
                    filepath = os.path.join(upload_folder_abs, filename)
                    file.save(filepath)
                    user.profile_picture = filename
                    flash('Imagen guardada localmente.', 'success')
            else:
                flash('Solo se permiten imágenes: png, jpg, jpeg, gif.', 'danger')
                return redirect(url_for('config.config'))

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('config.config'))

    return render_template('config.html', user=user)
