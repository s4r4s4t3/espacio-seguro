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


