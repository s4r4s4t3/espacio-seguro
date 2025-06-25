from flask import Flask, render_template, request, redirect, session
import random
from datetime import datetime
import os

# Usuario temporal para pruebas
usuarios = {
    "eze": "verde123"
}

def cargar_usuarios():
    usuarios = {}
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r", encoding="utf-8") as f:
            for linea in f:
                usuario, clave, emoji, color = linea.strip().split(",")
                usuarios[usuario] = {"clave": clave, "emoji": emoji, "color": color}
    return usuarios


app = Flask(__name__)
app.secret_key = "espacio_seguro_123"  # Clave secreta para usar sesiones

frases_apoyo = [
    "Respirá profundo. No estás solo/a.",
    "Esto también pasará.",
    "Confía en tu capacidad para sanar.",
    "Hoy puede ser difícil, pero no es para siempre.",
    "Eres más fuerte de lo que creés.",
]

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/mensajes")
def ver_mensajes():
    try:
        with open("publicaciones.txt", "r", encoding="utf-8") as archivo:
            mensajes = archivo.readlines()[-5:]  # solo últimos 5
    except FileNotFoundError:
        mensajes = []

    return render_template("mensajes.html", mensajes=mensajes)

frases_por_categoria = {
    "1": [
        "No estás solo/a.",
        "Puedes superarlo.",
        "Respira profundo. Cuenta hasta diez.",
        "Eres más fuerte de lo que crees.",
        "Confía en tu capacidad para sanar.",
        "Hoy es un nuevo día para empezar de nuevo.",
        "Está bien sentir lo que sientes.",
        "Esto también pasará.",
        "Eres valioso/a, no importa cómo te sientas."
    ],
    "2": [
        "Suelta el control, solo observa.",
        "Concéntrate en el presente.",
        "Todo estará bien.",
        "Soy capaz de manejar esto.",
        "Estoy a salvo."
    ],
    "3": [
        "Si necesitas hablar, estoy aquí.",
        "Cuéntame qué necesitás.",
        "Estoy acá para escucharte.",
        "No estás solo/a en esto, busquemos ayuda juntos."
    ],
    "4": [
        "Recordá tus fortalezas.",
        "Lo que sentís no te define.",
        "La ansiedad no es permanente.",
        "Sos capaz de encontrar la calma.",
        "La vida es un 10% de lo que te sucede y un 90% de cómo reaccionás ante ello."
    ]
}

@app.route("/frases", methods=["GET", "POST"])
def frases():
    frase_elegida = None
    if request.method == "POST":
        categoria = request.form.get("categoria")
        if categoria in frases_por_categoria:
            frase_elegida = random.choice(frases_por_categoria[categoria])
    return render_template("frases.html", frase=frase_elegida)


import os

def obtener_contactos():
    if os.path.exists("contactos.txt"):
        with open("contactos.txt", "r", encoding="utf-8") as f:
            return [linea.strip() for linea in f if linea.strip()]
    return []

@app.route("/contencion")
def contencion():
    contactos = obtener_contactos()
    return render_template("contencion.html", contactos=contactos)

@app.route("/contactos", methods=["GET", "POST"])
def contactos():
    mensaje = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if nombre:
            with open("contactos.txt", "a", encoding="utf-8") as f:
                f.write(nombre + "\n")
            mensaje = f"El contacto '{nombre}' fue agregado correctamente."
    return render_template("contactos.html", mensaje=mensaje)

@app.route("/historial")
def historial():
    try:
        with open("publicaciones.txt", "r", encoding="utf-8") as f:
            publicaciones = [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        publicaciones = []
    return render_template("historial.html", publicaciones=publicaciones)

@app.route("/diario", methods=["GET", "POST"])
def diario():
    mensaje = None
    if request.method == "POST":
        pensamiento = request.form.get("pensamiento", "").strip()
        if pensamiento:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open("diario_personal.txt", "a", encoding="utf-8") as f:
                f.write(f"[{fecha}] {pensamiento}\n")
            mensaje = "Tu pensamiento fue guardado en privado."
    return render_template("diario.html", mensaje=mensaje)

@app.route("/ver_diario")
def ver_diario():
    try:
        with open("diario_personal.txt", "r", encoding="utf-8") as f:
            entradas = [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        entradas = []
    return render_template("ver_diario.html", entradas=entradas)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        contrasena = request.form.get("contrasena", "").strip()
        usuarios = cargar_usuarios()

        if usuario in usuarios and usuarios[usuario]["clave"] == contrasena:
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
    else:
        return redirect("/")
    
@app.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = None
    if request.method == "POST":
        usuario = request.form.get("usuario").strip()
        contrasena = request.form.get("contrasena").strip()
        emoji = request.form.get("emoji").strip()
        color = request.form.get("color").strip()

        if not os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "w", encoding="utf-8") as f:
                pass

        with open("usuarios.txt", "a", encoding="utf-8") as f:
            f.write(f"{usuario},{contrasena},{emoji},{color}\n")

        mensaje = f"Cuenta creada para '{usuario}' 🌿"
    return render_template("registro.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
    
