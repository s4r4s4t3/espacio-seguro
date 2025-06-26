from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit
from datetime import datetime
import sqlite3
import os
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DATABASE'] = 'database.db'
socketio = SocketIO(app)

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Conexión a la base de datos
def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Inicialización de la base de datos
def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                clave TEXT NOT NULL,
                email TEXT UNIQUE,
                pais TEXT DEFAULT 'Desconocido',
                intereses TEXT DEFAULT '',
                playlist TEXT DEFAULT '',
                suscripcion BOOLEAN DEFAULT FALSE
            )
        ''')
        
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
        
        # Usuario demo
        if not db.execute('SELECT 1 FROM usuarios WHERE usuario = "demo"').fetchone():
            db.execute(
                'INSERT INTO usuarios (usuario, clave) VALUES (?, ?)',
                ("demo", generate_password_hash("demo123"))
            )
        db.commit()

init_db()

# Filtro de palabras sensibles
try:
    with open('palabras_prohibidas.json', encoding='utf-8') as f:
        palabras_prohibidas = json.load(f)
except FileNotFoundError:
    palabras_prohibidas = ["odio", "violencia"]

def filtrar_mensaje(texto):
    for palabra in palabras_prohibidas:
        texto = texto.replace(palabra, "***")
    return texto

# Rutas de autenticación
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

# Rutas principales
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

# Sistema de amigos
@app.route("/amigos")
@login_required
def lista_amigos():
    with get_db() as db:
        amigos = db.execute('''
            SELECT u.id, u.usuario 
            FROM amistades a 
            JOIN usuarios u ON a.amigo_id = u.id 
            WHERE a.usuario_id = ? AND a.estado = "aceptada"
        ''', (session["usuario_id"],)).fetchall()
        
        solicitudes = db.execute('''
            SELECT u.id, u.usuario 
            FROM amistades a 
            JOIN usuarios u ON a.usuario_id = u.id 
            WHERE a.amigo_id = ? AND a.estado = "pendiente"
        ''', (session["usuario_id"],)).fetchall()
    
    return render_template("amigos.html", amigos=amigos, solicitudes=solicitudes)

@app.route("/amigos/agregar/<int:amigo_id>", methods=["POST"])
@login_required
def agregar_amigo(amigo_id):
    with get_db() as db:
        try:
            db.execute(
                "INSERT INTO amistades (usuario_id, amigo_id) VALUES (?, ?)",
                (session["usuario_id"], amigo_id)
            )
            db.commit()
            return jsonify({"status": "success"})
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Solicitud ya enviada"}), 400

@app.route("/amigos/aceptar/<int:amigo_id>", methods=["POST"])
@login_required
def aceptar_amigo(amigo_id):
    with get_db() as db:
        db.execute(
            "UPDATE amistades SET estado = 'aceptada' WHERE usuario_id = ? AND amigo_id = ?",
            (amigo_id, session["usuario_id"])
        )
        db.commit()
    return jsonify({"status": "success"})

# Botón de Pánico
@app.route("/panic", methods=["POST"])
@login_required
def panic_button():
    with get_db() as db:
        amigos = db.execute('''
            SELECT u.usuario, u.email 
            FROM amistades a
            JOIN usuarios u ON a.amigo_id = u.id
            WHERE a.usuario_id = ? AND a.estado = 'aceptada'
            ORDER BY RANDOM() 
            LIMIT 3
        ''', (session["usuario_id"],)).fetchall()
        
        # Simular notificación
        print(f"🚨 ALERTA: Notificando a {[a['usuario'] for a in amigos]}")
    
    return jsonify({
        "status": "success",
        "message": "Tus contactos han sido notificados",
        "notified": [a["usuario"] for a in amigos]
    })

@app.route("/contactos", methods=["GET", "POST"])
@login_required
def contactos():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        # Lógica para guardar el contacto (ajusta según necesites)
        return render_template("contactos.html", mensaje="Contacto guardado")
    return render_template("contactos.html")

# WebSockets (Chat)
@socketio.on('mensaje')
def handle_message(data):
    mensaje_filtrado = filtrar_mensaje(data['mensaje'])
    emit('nuevo_mensaje', {
        'remitente': session.get("usuario_id"),
        'mensaje': mensaje_filtrado
    }, broadcast=True)

@app.route("/diario", methods=["GET", "POST"])
@login_required
def diario():
    if request.method == "POST":
        pensamiento = request.form.get("pensamiento")
        # Lógica para guardar en el diario
        return render_template("diario.html", mensaje="Entrada guardada")
    return render_template("diario.html")

@app.route("/musica")
@login_required
def musica():
    return render_template("musica.html")  # Necesitarás crear este archivo

@app.route("/perfil")
@login_required
def perfil():
    with get_db() as db:
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE id = ?", 
            (session["usuario_id"],)
        ).fetchone()
    return render_template("perfil.html", usuario=usuario)


if __name__ == "__main__":
    socketio.run(app, debug=True)