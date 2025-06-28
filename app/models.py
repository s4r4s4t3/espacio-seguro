# app/models.py

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
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256), nullable=False)

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

# --------------------
# Botón de Pánico - Logs
# --------------------
class PanicLog(db.Model):
    __tablename__ = 'panic_log'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(256), nullable=False)
