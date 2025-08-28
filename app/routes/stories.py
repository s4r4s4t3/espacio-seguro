"""
Rutas relacionadas con las historias (estados) al estilo Instagram.

Este módulo define las vistas que permiten a los usuarios crear y
eliminar historias.  Las historias son imágenes efímeras que se
muestran en la parte superior del feed y en la galería del perfil.

Usamos Cloudinary para almacenar las imágenes cuando está configurado
en las variables de entorno.  En caso de fallo, se puede caer en un
almacenamiento local como fallback.
"""
import os
import uuid
import cloudinary
import cloudinary.uploader
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.models import db, Story

# Aseguramos que Cloudinary esté configurado.  Si las variables
# CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET no
# existen, cloudinary.config realizará una configuración vacía y se
# generará un error al subir.  Esta configuración se comparte con otras
# rutas que ya emplean Cloudinary.
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

stories_bp = Blueprint('stories', __name__)


@stories_bp.route('/crear_estado', methods=['POST'])
@login_required
def crear_estado():
    """
    Crea una nueva historia para el usuario autenticado.  Se espera
    recibir un archivo de imagen en el campo `story_image` y un texto
    opcional en `caption`.  La imagen se sube a Cloudinary y se
    guarda la URL segura en la base de datos.
    """
    file = request.files.get('story_image')
    caption = request.form.get('caption', '').strip() or None

    if not file or not file.filename:
        flash(_('Debes seleccionar una imagen para el estado.'), 'warning')
        return redirect(request.referrer or url_for('home.feed'))

    # Validar extensiones simples (permitimos imágenes)
    allowed_exts = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_exts):
        flash(_('Formato de imagen no soportado.'), 'danger')
        return redirect(request.referrer or url_for('home.feed'))

    # Subir a Cloudinary cuando haya credenciales
    image_url = None
    if os.getenv('CLOUDINARY_CLOUD_NAME') and os.getenv('CLOUDINARY_API_KEY') and os.getenv('CLOUDINARY_API_SECRET'):
        try:
            upload_result = cloudinary.uploader.upload(
                file,
                folder='espacio_seguro/historias',
                transformation=[{'quality': 'auto', 'fetch_format': 'auto'}]
            )
            image_url = upload_result['secure_url']
        except Exception as e:
            # Continuar con fallback local
            flash(_('Error al subir a Cloudinary: %(err)s. Guardando localmente.', err=str(e)), 'warning')

    if image_url is None:
        # Fallback: guardar localmente en static/stories dentro del paquete
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        # La carpeta absoluta se basa en current_app.root_path
        from flask import current_app
        local_folder_abs = os.path.join(current_app.root_path, 'static', 'stories')
        os.makedirs(local_folder_abs, exist_ok=True)
        filepath = os.path.join(local_folder_abs, filename)
        file.save(filepath)
        # La URL relativa se compone únicamente del nombre de archivo.  La ruta
        # completa se construye en las plantillas con url_for('static', filename='stories/<file>').
        image_url = filename

    nueva = Story(image_url=image_url, caption=caption, user_id=current_user.id)
    db.session.add(nueva)
    db.session.commit()
    flash(_('✅ Estado creado correctamente.'), 'success')
    return redirect(request.referrer or url_for('home.feed'))


@stories_bp.route('/eliminar_estado/<int:story_id>', methods=['POST'])
@login_required
def eliminar_estado(story_id):
    """
    Elimina una historia existente.  Sólo el autor puede eliminarla.
    Se intentará borrar la imagen de Cloudinary si es una URL remota.
    """
    story = Story.query.get_or_404(story_id)
    if story.user_id != current_user.id:
        flash(_('No tienes permiso para eliminar este estado.'), 'danger')
        return redirect(request.referrer or url_for('home.feed'))

    # Si la imagen está en Cloudinary, intentamos eliminarla
    if story.image_url:
        if story.image_url.startswith('http'):
            try:
                public_id = story.image_url.rsplit('/', 1)[-1].split('.')[0]
                cloudinary.uploader.destroy(public_id)
            except Exception:
                pass  # No impedir la eliminación de la base de datos
        else:
            # Fallback: eliminar archivo local
            from flask import current_app
            local_path = os.path.join(current_app.root_path, 'static', 'stories', story.image_url)
            if os.path.exists(local_path):
                try:
                    os.remove(local_path)
                except Exception:
                    pass

    db.session.delete(story)
    db.session.commit()
    flash(_('Estado eliminado.'), 'info')
    return redirect(request.referrer or url_for('home.feed'))