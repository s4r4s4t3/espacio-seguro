from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from frases import frases_por_categoria
import sqlite3
import os
import random

app = Flask(__name__)
app.secret_key = "espacio_seguro_123"
DATABASE = 'database.db'

# ---- Funciones de Base de Datos ----
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        # Tabla de usuarios
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario TEXT PRIMARY KEY,
                clave TEXT NOT NULL,
                emoji TEXT,
                color TEXT
            )
        ''')
        # Tabla de publicaciones
        db.execute('''
            CREATE TABLE IF NOT EXISTS publicaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                mensaje TEXT NOT NULL
            )
        ''')
        # Tabla de diario
        db.execute('''
            CREATE TABLE IF NOT EXISTS diario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                entrada TEXT NOT NULL
            )
        ''')
        # Tabla de contactos
        db.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')
        
        # Usuario demo
        if not db.execute('SELECT 1 FROM usuarios WHERE usuario = "eze"').fetchone():
            db.execute(
                'INSERT INTO usuarios VALUES (?, ?, ?, ?)',
                ("eze", generate_password_hash("verde123"), "🌿", "#2e8b57")
            )
        db.commit()

init_db()

# ---- Rutas ----
@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect("/inicio-personalizado")
    return render_template("inicio.html")

@app.route("/mensajes")
def ver_mensajes():
    with get_db() as db:
        mensajes = db.execute('''
            SELECT fecha, mensaje FROM publicaciones 
            ORDER BY fecha DESC LIMIT 5
        ''').fetchall()
    return render_template("mensajes.html", mensajes=mensajes)

@app.route("/frases", methods=["GET", "POST"])
def frases():
    frase_elegida = None
    if request.method == "POST":
        categoria = request.form.get("categoria")
        if categoria in frases_por_categoria:
            frase_elegida = random.choice(frases_por_categoria[categoria])
    return render_template("frases.html", frase=frase_elegida)

@app.route("/contencion")
def contencion():
    with get_db() as db:
        contactos = db.execute('SELECT nombre FROM contactos').fetchall()
    return render_template("contencion.html", contactos=contactos)

@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    mensaje = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre:
            with get_db() as db:
                db.execute('INSERT INTO contactos (nombre) VALUES (?)', (nombre,))
                db.commit()
            mensaje = f"Contacto '{nombre}' agregado"
    return render_template("contactos.html", mensaje=mensaje)

@app.route("/historial")
def historial():
    with get_db() as db:
        publicaciones = db.execute('SELECT fecha, mensaje FROM publicaciones ORDER BY fecha DESC').fetchall()
    return render_template("historial.html", publicaciones=publicaciones)

@app.route("/diario", methods=["GET", "POST"])
def diario():
    mensaje = None
    if request.method == "POST":
        entrada = request.form.get("pensamiento", "").strip()
        if entrada:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            with get_db() as db:
                db.execute('INSERT INTO diario (fecha, entrada) VALUES (?, ?)', (fecha, entrada))
                db.commit()
            mensaje = "Entrada guardada en tu diario"
    return render_template("diario.html", mensaje=mensaje)

@app.route("/ver_diario")
def ver_diario():
    with get_db() as db:
        entradas = db.execute('SELECT fecha, entrada FROM diario ORDER BY fecha DESC').fetchall()
    return render_template("ver_diario.html", entradas=entradas)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        
        with get_db() as db:
            user = db.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()

        if user and check_password_hash(user['clave'], contrasena):
            session["usuario"] = user['usuario']
            session["emoji"] = user['emoji']
            session["color"] = user['color']
            return redirect("/inicio-personalizado")
        else:
            error = "Credenciales incorrectas"
    
    return render_template("inicio.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/inicio-personalizado")
def inicio_personalizado():
    if "usuario" in session:
        return render_template("inicio_personalizado.html",
                            usuario=session["usuario"],
                            emoji=session.get("emoji", ""),
                            color=session.get("color", "#2e8b57"))
    return redirect("/")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = None
    if request.method == "POST":
        usuario = request.form.get("usuario").strip()
        contrasena = generate_password_hash(request.form.get("contrasena").strip())
        emoji = request.form.get("emoji").strip()
        color = request.form.get("color").strip()

        try:
            with get_db() as db:
                db.execute(
                    'INSERT INTO usuarios VALUES (?, ?, ?, ?)',
                    (usuario, contrasena, emoji, color)
                )
                db.commit()
            mensaje = f"Cuenta creada para '{usuario}' 🌿"
        except sqlite3.IntegrityError:
            mensaje = "⚠️ El usuario ya existe"
    
    return render_template("registro.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)