import os

def leer_archivo(nombre):
    try:
        with open(nombre, "r", encoding="utf-8") as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        return []

def escribir_archivo(nombre, contenido, modo="a"):
    os.makedirs(os.path.dirname(nombre), exist_ok=True)
    with open(nombre, modo, encoding="utf-8") as f:
        f.write(str(contenido) + "\n")