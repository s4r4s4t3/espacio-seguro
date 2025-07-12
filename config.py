# config.py

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///db.sqlite3"
    ).replace(
        "postgres://",
        "postgresql+psycopg2://"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Seguridad sesión cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True

    # ✅ Seguridad CSRF
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY", "clave_csrf_secreta")

    # ✅ Seguridad CORS
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_CREDENTIALS = True

    # ✅ Seguridad de la aplicación
    APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT", "/")
    DEBUG = os.environ.get("DEBUG", "False").lower() in ['true', '1', 't']
    TESTING = os.environ.get("TESTING", "False").lower() in ['true', '1', 't']

    # ✅ OAuth Google
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")



