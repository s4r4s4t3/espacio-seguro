from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from . import db

# --------------------
# Tabla de Usuarios
# --------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password = db.Column(db.String(256), nullable=False)

    bio = db.Column(db.String(300), default="")
    profile_picture = db.Column(db.String(300), nullable=False, default="default.png")
    accepted_terms = db.Column(db.Boolean, default=False)

    sent_messages = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='sender',
                                    lazy=True)
    received_messages = db.relationship('Message',
                                        foreign_keys='Message.receiver_id',
                                        backref='receiver',
                                        lazy=True)
    diary_entries = db.relationship('DiaryEntry',
                                    backref='author',
                                    lazy=True)
    panic_logs = db.relationship('PanicLog',
                                 backref='author',
                                 lazy=True)
    posts = db.relationship('Post',
                            backref='author',
                            lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# --------------------
# Solicitudes de Amistad
# --------------------
class FriendRequest(db.Model):
    __tablename__ = 'friend_request'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(10), default='pending')  # pending, accepted, rejected
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ Asegura que no se dupliquen solicitudes entre 2 usuarios
    __table_args__ = (
        db.UniqueConstraint('sender_id', 'receiver_id', name='uq_friend_request_unique_pair'),
    )

# --------------------
# Mensajes (Global y Privado)
# --------------------
class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Null = Chat Global
    content = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

# --------------------
# Entradas del Diario Personal
# --------------------
class DiaryEntry(db.Model):
    __tablename__ = 'diary_entry'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --------------------
# Botón de Pánico - Logs
# --------------------
class PanicLog(db.Model):
    __tablename__ = 'panic_log'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(256), nullable=True)

# --------------------
# 🧑‍🎨 Nuevo modelo: Publicaciones del Feed
# --------------------
class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
