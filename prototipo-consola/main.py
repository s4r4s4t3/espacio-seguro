import random
from datetime import datetime

# Frases organizadas por categoría
frases = {
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
        "Cuéntame qué necesitas.",
        "Estoy aquí para escucharte.",
        "No estás solo/a en esto, busquemos ayuda juntos."
    ],
    "4": [
        "Recuerda tus fortalezas.",
        "Lo que sientes no te define.",
        "La ansiedad no es permanente.",
        "Eres capaz de encontrar la calma.",
        "La vida es un 10% de lo que te sucede y un 90% de cómo reaccionas ante ello."
    ]
}

publicaciones = []

def mostrar_menu():
    print("\n🌱 Bienvenido/a a tu espacio seguro\n")
    print("1. Publicar cómo me siento")
    print("2. Elegir una frase de contención")
    print("3. Ver mensajes recientes")
    print("4. Ver historial completo (archivo)")
    print("5. Botón de contención (emergencia emocional)")
    print("6. Agregar contacto de confianza")
    print("7. Salir")

def publicar_mensaje():
    estado = input("💬 ¿Cómo te sentís hoy?: ")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    publicaciones.append({"fecha": fecha, "mensaje": estado})
    print("✅ Gracias por compartir. Tu mensaje fue guardado.")

    with open("publicaciones.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {estado}\n")

def elegir_frase():
    print("\n📚 ¿Qué tipo de frase necesitás?")
    print("1. Aliento y empoderamiento")
    print("2. Calmar la mente")
    print("3. Buscar apoyo")
    print("4. Recordar tu fuerza")
    tipo = input("Elegí una opción (1-4): ")
    if tipo in frases:
        print("\n💌 " + random.choice(frases[tipo]))
    else:
        print("❌ Opción no válida.")

def ver_mensajes():
    if publicaciones:
        print("\n📒 Mensajes recientes:")
        for pub in publicaciones[-5:]:
            print(f"[{pub['fecha']}] {pub['mensaje']}")
    else:
        print("📭 Todavía no hay publicaciones.")

def ver_historial_guardado():
    try:
        with open("publicaciones.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.readlines()
            if contenido:
                print("\n🗂️ Historial de publicaciones guardadas:")
                for linea in contenido[-10:]:
                    print(linea.strip())
            else:
                print("📭 El archivo está vacío.")
    except FileNotFoundError:
        print("⚠️ Aún no hay archivo de historial creado.")

def agregar_contacto():
    nombre = input("👥 Nombre del contacto de confianza a agregar: ")
    if nombre.strip():
        with open("contactos.txt", "a", encoding="utf-8") as archivo:
            archivo.write(nombre.strip() + "\n")
        print(f"✅ Contacto '{nombre}' agregado correctamente.")
    else:
        print("⚠️ Nombre no válido. Intentá nuevamente.")

def obtener_contactos():
    try:
        with open("contactos.txt", "r", encoding="utf-8") as archivo:
            return [linea.strip() for linea in archivo if linea.strip()]
    except FileNotFoundError:
        return []

def boton_de_contencion():
    print("\n🚨 BOTÓN DE CONTENCIÓN ACTIVADO")
    print("💓 Respirá conmigo...")
    print("🕊️ No tenés que resolver todo ahora mismo.")
    print("📩 Estamos con vos. Esto no es el final.")

    contactos = obtener_contactos()
    if contactos:
        print("\n📲 Notificando a tus contactos de confianza:")
        for contacto in contactos:
            print(f"👉 {contacto} fue avisado simbólicamente.")
    else:
        print("⚠️ Aún no agregaste contactos de confianza. Podés sumarlos desde el menú.")

# Bucle principal
while True:
    mostrar_menu()
    opcion = input("\nElegí una opción (1-7): ")

    if opcion == "1":
        publicar_mensaje()
    elif opcion == "2":
        elegir_frase()
    elif opcion == "3":
        ver_mensajes()
    elif opcion == "4":
        ver_historial_guardado()
    elif opcion == "5":
        boton_de_contencion()
    elif opcion == "6":
        agregar_contacto()
    elif opcion == "7":
        print("👋 Gracias por usar este espacio. Que tengas un día amable con vos mismo/a.")
        break
    else:
        print("❌ Opción no válida. Intentá nuevamente.")