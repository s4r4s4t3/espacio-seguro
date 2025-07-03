# app/routes/chat.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import User, Message, db
import cloudinary
import cloudinary.uploader

# ✅ Configura Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

chat_bp = Blueprint('chat', __name__)

# ✅ Ruta: Chat Global (render)
@chat_bp.route('/chat')
@login_required
def chat_global():
    return render_template('chat.html')

# ✅ Ruta: Chat Privado (render)
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

# ✅ Ruta: Envía mensaje GLOBAL con texto y/o imagen
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
        image_url=image_url
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        'content': new_message.content,
        'image_url': new_message.image_url,
        'sender_username': current_user.username
    })

# ✅ Ruta: Envía mensaje PRIVADO con texto y/o imagen
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
        image_url=image_url
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

