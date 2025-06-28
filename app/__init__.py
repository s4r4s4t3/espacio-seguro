# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (opcional)
load_dotenv()

# Inicializa extensiones
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")  # Permitir CORS en prod si hace falta
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Inicializa extensiones con la app
    db.init_app(app)
    socketio.init_app(app, async_mode='eventlet')
    login_manager.init_app(app)

    # Redirigir al login si no está autenticado
    login_manager.login_view = 'auth.login'

    from app.models import User, FriendRequest, Message

    # 🔑 CREA LAS TABLAS SI NO EXISTEN — Render free sin Shell
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registra Blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    from app.routes.friends import friends_bp
    app.register_blueprint(friends_bp)

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    return app


