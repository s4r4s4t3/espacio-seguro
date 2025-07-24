import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_babel import Babel

load_dotenv()

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['BABEL_DEFAULT_LOCALE'] = 'es'
    app.config['LANGUAGES'] = ['es', 'en', 'pt', 'br', 'de', 'fr', 'it']

    db.init_app(app)
    # Usar "eventlet" solo si tu entorno lo soporta (Render sí)
    socketio.init_app(app, async_mode='eventlet')
    login_manager.init_app(app)
    babel.init_app(app)

    login_manager.login_view = 'auth.login'

    # Importa todos los modelos antes de db.create_all()
    from app.models import User, FriendRequest, Message, DiaryEntry, PanicLog, Post

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints principales
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp, url_prefix="/")

    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    from app.routes.diary import diary_bp
    app.register_blueprint(diary_bp)

    from app.routes.friends import amigos_bp
    app.register_blueprint(amigos_bp)

    from app.routes.config import config_bp
    app.register_blueprint(config_bp)

    from app.routes.legales import legales_bp
    app.register_blueprint(legales_bp)

    @babel.localeselector
    def get_locale():
        lang = request.cookies.get('lang')
        if lang in app.config['LANGUAGES']:
            return lang
        return app.config['BABEL_DEFAULT_LOCALE']

    return app

    # 🚫 Registrar Blueprint OAuth Google (comentado)
    """
    from config import Config
    google_bp = make_google_blueprint(
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        redirect_to="auth.login_google",
        scope=["profile", "email"]
    )
    app.register_blueprint(google_bp, url_prefix="/login")
    """
