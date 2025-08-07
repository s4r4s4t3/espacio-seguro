"""
Adaptador de servidor para SocketIO.

Intentamos usar eventlet para un servidor asíncrono en producción.  Si
eventlet no está instalado (por ejemplo, en entornos de desarrollo
cerrados), usamos el servidor integrado de Flask como fallback.  Esta
aproximación nos permite ejecutar la aplicación sin depender de
eventlet en todos los contextos.
"""
try:
    import eventlet  # type: ignore
    eventlet.monkey_patch()
    _use_eventlet = True
except ImportError:
    _use_eventlet = False

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
    # Ejecutar con SocketIO si eventlet está disponible; de lo contrario,
    # usar el servidor de Flask.  El parámetro debug controla el modo
    # depuración en ambos casos.
    if _use_eventlet:
        socketio.run(app, debug=True)
    else:
        # Fallback: ejecutar la app de Flask sin SocketIO.  Las
        # funcionalidades de chat en tiempo real no funcionarán, pero
        # permite probar el resto de la aplicación.
        app.run(debug=True)


