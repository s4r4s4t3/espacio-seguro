<<<<<<< HEAD
from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    # For local dev; in Render use gunicorn with eventlet
=======
# wsgi.py — entrypoint para Render (Gunicorn)
# Expone `app` y compila traducciones (.po -> .mo) en el arranque.

from app import create_app, socketio  # tu proyecto ya expone estas referencias

# Crear la app de Flask (tu factory existente)
app = create_app()

# --- Compilación automática de traducciones (.po -> .mo) en el arranque ---
def _compile_translations_once():
    """
    Para evitar pasos manuales en Render, compilamos los .po a .mo al iniciar.
    Si por algún motivo falla, no es fatal: la app igualmente levanta.
    """
    try:
        import os, glob
        from babel.messages import pofile, mofile

        translations_root = os.path.join(os.path.dirname(__file__), "translations")
        if not os.path.isdir(translations_root):
            return

        for po_path in glob.glob(os.path.join(translations_root, "*", "LC_MESSAGES", "messages.po")):
            try:
                with open(po_path, "r", encoding="utf-8") as f:
                    catalog = pofile.read_po(f)

                mo_path = po_path[:-2] + "mo"  # reemplaza .po -> .mo
                os.makedirs(os.path.dirname(mo_path), exist_ok=True)
                with open(mo_path, "wb") as f:
                    mofile.write_mo(f, catalog)
            except Exception:
                # Continuamos con el siguiente idioma si uno falla
                continue
    except Exception:
        # No hacemos nada si Babel no está disponible o hay otro error global
        pass

_compile_translations_once()

# Nota: Gunicorn levantará `app` usando el Procfile.
# Para desarrollo local, podrías usar:
if __name__ == "__main__":
    # Esto no se usa en Render (ahí corre gunicorn),
    # pero te sirve localmente si lo necesitás.
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
    socketio.run(app, host="0.0.0.0", port=5000)
