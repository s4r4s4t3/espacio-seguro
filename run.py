import eventlet
eventlet.monkey_patch()

from app import create_app, socketio, db
from app.models import User, Message

app = create_app()

# Evento: mensaje privado
@socketio.on('mensaje_privado')
def handle_mensaje_privado(data):
    sender = User.query.get(data['sender_id'])
    receiver = User.query.get(data['receiver_id'])
    content = data['content']

    nuevo_mensaje = Message(
        sender_id=sender.id,
        receiver_id=receiver.id,
        content=content
    )
    db.session.add(nuevo_mensaje)
    db.session.commit()

    socketio.emit('mensaje_privado', {
        'sender_id': sender.id,
        'receiver_id': receiver.id,
        'sender_username': sender.username,
        'content': content
    })

# Evento: mensaje global
@socketio.on('mensaje')
def manejar_mensaje(msg):
    print("Mensaje recibido:", msg)
    socketio.emit('mensaje', msg)

if __name__ == "__main__":
    socketio.run(app, debug=True)


