# app/routes/chat.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import User, Message, db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/<int:friend_id>', methods=['GET', 'POST'])
@login_required
def chat(friend_id):
    friend = User.query.get_or_404(friend_id)

    # Asegurarse que son amigos antes de permitir chatear
    if friend not in current_user.friends:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        content = request.form['message']
        if content:
            new_message = Message(sender_id=current_user.id, receiver_id=friend_id, content=content)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('chat.chat', friend_id=friend_id))

    # Mensajes entre ambos
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == friend_id)) |
        ((Message.sender_id == friend_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return render_template('chat_privado.html', friend=friend, messages=messages)

