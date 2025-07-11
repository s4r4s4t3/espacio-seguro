# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

# ✅ Cargar variables de entorno desde .env
load_dotenv()

# ✅ Inicializar extensiones globales
db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # ✅ Configuración principal
    app.config.from_object("config.Config")

    # ✅ Seguridad para sesiones en producción
    app.config['SESSION_COOKIE_SECURE'] = True   # HTTPS obligatorio
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # ✅ Inicializar extensiones con la app
    db.init_app(app)
    socketio.init_app(app, async_mode='eventlet')
    login_manager.init_app(app)

    # ✅ Configuración de Flask-Login
    login_manager.login_view = 'auth.login'

    # ✅ Importar modelos para que SQLAlchemy los detecte
    from app.models import User, FriendRequest, Message, DiaryEntry

    # ✅ Crear tablas si no existen (solo si usás SQLite local)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ✅ Registrar Blueprints (mantené este orden)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp, url_prefix="/")  # 🗝️ Landing page raíz

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.routes.diary import diary_bp
    app.register_blueprint(diary_bp)

    from app.routes.amigos import amigos_bp
    app.register_blueprint(amigos_bp)

    from app.routes.config import config_bp
    app.register_blueprint(config_bp)

    from app.routes.legales import legales_bp
    app.register_blueprint(legales_bp)

    return app
