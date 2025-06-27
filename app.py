import os
from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from datetime import datetime
import sqlite3
import json
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY', os.urandom(24))
app.config['DATABASE'] = 'database.db'
socketio = SocketIO(app)

# Database setup
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_db() as db:
        # Users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                clave TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Friendships table
        db.execute('''
            CREATE TABLE IF NOT EXISTS amistades (
                usuario_id INTEGER NOT NULL,
                amigo_id INTEGER NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                PRIMARY KEY (usuario_id, amigo_id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY(amigo_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Messages table
        db.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente_id INTEGER NOT NULL,
                destinatario_id INTEGER,
                mensaje TEXT NOT NULL,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(remitente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY(destinatario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')
        
        # Demo user
        if not db.execute('SELECT 1 FROM usuarios WHERE usuario = "demo"').fetchone():
            db.execute(
                'INSERT INTO usuarios (usuario, clave) VALUES (?, ?)',
                ("demo", generate_password_hash("demo123"))
            )
        db.commit()

init_db()

# Security middleware
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Word filter
try:
    with open('palabras_prohibidas.json', encoding='utf-8') as f:
        palabras_prohibidas = json.load(f)
except FileNotFoundError:
    palabras_prohibidas = ["odio", "violencia"]

def filtrar_mensaje(texto):
    for palabra in palabras_prohibidas:
        texto = texto.replace(palabra, "***")
    return texto

# Auth routes
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "").strip()
        email = request.form.get("email", "").strip()
        
        if len(usuario) < 4 or len(clave) < 6:
            flash("Usuario (mín. 4 caracteres) y contraseña (mín. 6) son obligatorios", "error")
            return redirect(url_for('registro'))
        
        try:
            with get_db() as db:
                db.execute(
                    "INSERT INTO usuarios (usuario, clave, email) VALUES (?, ?, ?)",
                    (usuario, generate_password_hash(clave), email)
                )
                db.commit()
            flash("¡Registro exitoso! Por favor inicia sesión.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("El usuario o email ya existe", "error")
    
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")
        
        with get_db() as db:
            user = db.execute(
                "SELECT * FROM usuarios WHERE usuario = ?", 
                (usuario,)
            ).fetchone()
            
            if user and check_password_hash(user["clave"], clave):
                session["usuario_id"] = user["id"]
                return redirect(url_for('home'))
        
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# Main routes
@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/home")
@login_required
def home():
    with get_db() as db:
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE id = ?", 
            (session["usuario_id"],)
        ).fetchone()
        
        posts = db.execute('''
            SELECT u.usuario as autor, m.mensaje, m.fecha 
            FROM mensajes m
            JOIN usuarios u ON m.remitente_id = u.id
            WHERE m.destinatario_id IS NULL
            ORDER BY m.fecha DESC
            LIMIT 20
        ''').fetchall()
        
        amigos = db.execute('''
            SELECT u.id, u.usuario 
            FROM amistades a 
            JOIN usuarios u ON a.amigo_id = u.id 
            WHERE a.usuario_id = ? AND a.estado = "aceptada"
        ''', (session["usuario_id"],)).fetchall()
    
    return render_template("home.html", usuario=usuario, posts=posts, amigos=amigos)

# Emergency button
@app.route("/panic", methods=["POST"])
@login_required
def panic_button():
    with get_db() as db:
        amigos = db.execute('''
            SELECT u.usuario, u.email 
            FROM amistades a
            JOIN usuarios u ON a.amigo_id = u.id
            WHERE a.usuario_id = ? AND a.estado = 'aceptada'
            LIMIT 3
        ''', (session["usuario_id"],)).fetchall()
        
        if not amigos:
            return jsonify({"status": "error", "message": "No tienes amigos agregados"}), 400
            
        # In production: Integrate with Twilio here
        print(f"🚨 Notificando a: {[a['usuario'] for a in amigos]}")
        return jsonify({
            "status": "success",
            "notified": [a['usuario'] for a in amigos]
        })

# WebSocket handlers
@socketio.on('connect')
def handle_connect():
    if 'usuario_id' not in session:
        return False

@socketio.on('mensaje')
def handle_message(data):
    if 'usuario_id' not in session:
        return
    
    mensaje_filtrado = filtrar_mensaje(data['mensaje'])
    emit('nuevo_mensaje', {
        'remitente': session.get("usuario_id"),
        'mensaje': mensaje_filtrado,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)