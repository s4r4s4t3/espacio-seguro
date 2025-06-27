from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.home import home_bp
    app.register_blueprint(home_bp)
    
    from app.routes.friends import friends_bp
    app.register_blueprint(friends_bp)
    
    from .routes.chat import chat_bp
    app.register_blueprint(chat_bp)


    return app
