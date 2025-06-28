# config.py
import os

class Config:
    # Clave secreta para sesiones seguras
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta")

    # URI de la base de datos: usa PostgreSQL si está definida, sino SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
