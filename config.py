import os

class Config:
    SECRET_KEY = "clave_super_secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
