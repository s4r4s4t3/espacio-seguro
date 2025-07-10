import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import User, Message, db
import cloudinary
import cloudinary.uploader
from datetime import datetime

# ✅ Configura Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

chat_bp = Blueprint('chat', __name__)

# ✅ Ruta: Chat Global (render con mensajes persistentes)
@chat_bp.route('/chat')
@login_required
def chat_global():
    messages = Message.query.filter_by(receiver_id=None).order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', messages=messages)

# ✅ Ruta: Chat Privado (sin cambios)
@chat_bp.route('/chat/<int:friend_id>', methods=['GET'])
@login_required
def chat_privado(friend_id):
    friend = User.query.get_or_404(friend_id)

    if friend not in current_user.friends:
        return redirect(url_for('home.home'))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == friend_id)) |
        ((Message.sender_id == friend_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return render_template('chat_privado.html', friend=friend, messages=messages)

# ✅ Ruta: Envía mensaje GLOBAL (guarda en base y responde)
@chat_bp.route('/send_message_global', methods=['POST'])
@login_required
def send_message_global():
    content = request.form.get('content', '').strip()
    image_file = request.files.get('image')
    image_url = None

    if image_file:
        try:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder='espacio_seguro/chat',
                quality="auto",
                fetch_format="auto"
            )
            image_url = upload_result['secure_url']
        except Exception as e:
            print(f"❌ Error subiendo imagen a Cloudinary: {e}")

    if not content and not image_url:
        return jsonify({'error': 'Mensaje vacío'}), 400

    new_message = Message(
        sender_id=current_user.id,
        receiver_id=None,
        content=content if content else None,
        image_url=image_url,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        'content': new_message.content,
        'image_url': new_message.image_url,
        'sender_username': current_user.username
    })

# ✅ Ruta: Envía mensaje PRIVADO (sin cambios)
@chat_bp.route('/send_message_privado', methods=['POST'])
@login_required
def send_message_privado():
    content = request.form.get('content', '').strip()
    receiver_id = request.form.get('receiver_id')
    image_file = request.files.get('image')
    image_url = None

    if image_file:
        try:
            upload_result = cloudinary.uploader.upload(
                image_file,
                folder='espacio_seguro/chat_privado',
                quality="auto",
                fetch_format="auto"
            )
            image_url = upload_result['secure_url']
        except Exception as e:
            print(f"❌ Error subiendo imagen a Cloudinary: {e}")

    if not content and not image_url:
        return jsonify({'error': 'Mensaje vacío'}), 400

    new_message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content if content else None,
        image_url=image_url,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        'content': new_message.content,
        'image_url': new_message.image_url,
        'sender_id': current_user.id,
        'receiver_id': receiver_id,
        'sender_username': current_user.username
    })
# ✅ Ruta: Elimina mensaje (sin cambios)
@chat_bp.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.sender_id != current_user.id:
        return jsonify({'error': 'No tienes permiso para eliminar este mensaje'}), 403

    db.session.delete(message)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Mensaje eliminado correctamente'})
# ✅ Ruta: Edita mensaje (sin cambios)
@chat_bp.route('/edit_message/<int:message_id>', methods=['POST'])
@login_required
def edit_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.sender_id != current_user.id:
        return jsonify({'error': 'No tienes permiso para editar este mensaje'}), 403

    new_content = request.form.get('content', '').strip()
    if not new_content:
        return jsonify({'error': 'El contenido del mensaje no puede estar vacío'}), 400

    message.content = new_content
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Mensaje editado correctamente',
        'new_content': message.content
    })
# ✅ Ruta: Marca mensajes como leídos (sin cambios)
@chat_bp.route('/mark_as_read/<int:friend_id>', methods=['POST'])
@login_required
def mark_as_read(friend_id):
    friend = User.query.get_or_404(friend_id)

    if friend not in current_user.friends:
        return jsonify({'error': 'No tienes permiso para marcar mensajes como leídos'}), 403

    unread_messages = Message.query.filter(
        Message.sender_id == friend_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).all()

    for message in unread_messages:
        message.is_read = True

    db.session.commit()

    return jsonify({'success': True, 'message': 'Mensajes marcados como leídos'})
# ✅ Ruta: Obtiene mensajes no leídos (sin cambios)
@chat_bp.route('/unread_messages/<int:friend_id>', methods=['GET'])
@login_required
def unread_messages(friend_id):
    friend = User.query.get_or_404(friend_id)

    if friend not in current_user.friends:
        return jsonify({'error': 'No tienes permiso para ver mensajes no leídos'}), 403

    unread_messages = Message.query.filter(
        Message.sender_id == friend_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).all()

    return jsonify({
        'unread_count': len(unread_messages),
        'messages': [{'id': msg.id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in unread_messages]
    })
# ✅ Ruta: Obtiene mensajes de un usuario específico (sin cambios)
@chat_bp.route('/messages/<int:user_id>', methods=['GET'])
@login_required
def get_messages(user_id):
    user = User.query.get_or_404(user_id)

    if user not in current_user.friends:
        return jsonify({'error': 'No tienes permiso para ver los mensajes de este usuario'}), 403

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return jsonify({
        'messages': [{'id': msg.id, 'content': msg.content, 'image_url': msg.image_url, 'timestamp': msg.timestamp} for msg in messages]
    })
    