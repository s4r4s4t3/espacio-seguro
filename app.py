from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from frases import frases_por_categoria
from utils import leer_archivo, escribir_archivo
import os
import random

app = Flask(__name__)
app.secret_key = "espacio_seguro_123"  # Clave secreta para usar sesiones

def cargar_usuarios():
    """Carga usuarios desde el archivo usuarios.txt"""
    usuarios = {}
    lineas = leer_archivo("usuarios.txt")
    for linea in lineas:
        usuario, clave_hash, emoji, color = linea.strip().split(",")
        usuarios[usuario] = {
            "clave": clave_hash,
            "emoji": emoji,
            "color": color
        }
    return usuarios

@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect("/inicio-personalizado")
    return render_template("inicio.html")

@app.route("/mensajes")
def ver_mensajes():
    mensajes = leer_archivo("publicaciones.txt")[-5:]  # solo últimos 5
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
    contactos = leer_archivo("contactos.txt")
    return render_template("contencion.html", contactos=contactos)

@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    mensaje = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre:
            escribir_archivo("contactos.txt", nombre)
            mensaje = f"El contacto '{nombre}' fue agregado correctamente."
    return render_template("contactos.html", mensaje=mensaje)

@app.route("/historial")
def historial():
    publicaciones = leer_archivo("publicaciones.txt")
    return render_template("historial.html", publicaciones=publicaciones)

@app.route("/diario", methods=["GET", "POST"])
def diario():
    mensaje = None
    if request.method == "POST":
        pensamiento = request.form.get("pensamiento", "").strip()
        if pensamiento:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            escribir_archivo("diario_personal.txt", f"[{fecha}] {pensamiento}")
            mensaje = "Tu pensamiento fue guardado en privado."
    return render_template("diario.html", mensaje=mensaje)

@app.route("/ver_diario")
def ver_diario():
    entradas = leer_archivo("diario_personal.txt")
    return render_template("ver_diario.html", entradas=entradas)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        usuarios = cargar_usuarios()

        if usuario in usuarios and check_password_hash(usuarios[usuario]["clave"], contrasena):
            session["usuario"] = usuario
            session["emoji"] = usuarios[usuario]["emoji"]
            session["color"] = usuarios[usuario]["color"]
            return redirect("/inicio-personalizado")
        else:
            error = "Usuario o contraseña incorrectos. Intentá de nuevo."

    return render_template("inicio.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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
        contrasena = request.form.get("contrasena").strip()
        emoji = request.form.get("emoji").strip()
        color = request.form.get("color").strip()

        clave_hash = generate_password_hash(contrasena)
        escribir_archivo("usuarios.txt", f"{usuario},{clave_hash},{emoji},{color}")

        mensaje = f"Cuenta creada para '{usuario}' 🌿"
    return render_template("registro.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)