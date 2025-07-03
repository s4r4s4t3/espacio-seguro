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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@config_bp.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    user = User.query.get(current_user.id)

    if request.method == 'POST':
        # ✅ Guardar bio
        bio = request.form.get('bio')
        if bio is not None:
            user.bio = bio.strip()

        # ✅ Guardar imagen
        file = request.files.get('profile_picture')
        if file and file.filename:
            if allowed_file(file.filename):
                try:
                    # Subir a Cloudinary
                    upload_result = cloudinary.uploader.upload(file)
                    user.profile_picture = upload_result['secure_url']
                    flash('Imagen subida a Cloudinary correctamente.', 'success')
                except Exception as e:
                    flash(f'Error al subir a Cloudinary: {str(e)}. Guardando localmente.', 'warning')
                    # Fallback local
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{uuid.uuid4().hex}.{ext}"
                    upload_folder_abs = os.path.join(current_app.root_path, 'static/profile_pics')
                    if not os.path.exists(upload_folder_abs):
                        os.makedirs(upload_folder_abs)
                    filepath = os.path.join(upload_folder_abs, filename)
                    file.save(filepath)
                    user.profile_picture = filename
            else:
                flash('Solo se permiten imágenes: png, jpg, jpeg, gif', 'danger')
                return redirect(url_for('config.config'))

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('config.config'))

    return render_template('config.html', user=user)

