# app/routes/config.py

import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..models import db, User

config_bp = Blueprint('config', __name__)

UPLOAD_FOLDER = 'app/static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@config_bp.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    user = User.query.get(current_user.id)

    if request.method == 'POST':
        # ✅ Guardar bio
        bio = request.form.get('bio')
        user.bio = bio

        # ✅ Guardar imagen
        file = request.files.get('profile_picture')
        if file and file.filename:
            if allowed_file(file.filename):
                # Crear nombre único con UUID
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                user.profile_picture = filename
            else:
                flash('Solo se permiten imágenes: png, jpg, jpeg, gif', 'danger')
                return redirect(url_for('config.config'))

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('config.config'))

    return render_template('config.html', user=user)

