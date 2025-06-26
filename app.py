from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg2  # ¡Nuevo! Para PostgreSQL

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))  # Clave desde variables de entorno
app.config['DATABASE'] = os.environ.get('DATABASE_URL')  # ¡Importante!

# Conexión a la base de datos (PostgreSQL)
def get_db():
    return psycopg2.connect(app.config['DATABASE'])

# ... (el resto de tu código actual, SIN socketio.run) ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)