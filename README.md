# SafeSpace — Instagram-like Upgrade (PRO)

## Despliegue rápido (Render + Supabase + Cloudinary)
1. **Variables de entorno (Render)**
   - `DATABASE_URL` (Supabase Postgres)
   - `SECRET_KEY`
   - `CLOUDINARY_URL` (formato `cloudinary://KEY:SECRET@CLOUD_NAME`)
   - `PREFERRED_URL_SCHEME=https`
2. **Build & Start**
   - Python 3.11; `pip install -r requirements.txt`
   - Start: `gunicorn wsgi:app` (o `python app.py` en dev)
3. **Babel/i18n**
   - `pip install Babel Flask-Babel`
   - `npm run i18n:extract && npm run i18n:update && npm run i18n:compile`
4. **Sockets**
   - Usa Eventlet en Render si necesitas WebSockets estables: `web: gunicorn -k eventlet -w 1 wsgi:app`
5. **Cloudinary**
   - Las imágenes usan `f_auto,q_auto` + `srcset`; no subas videos pesados por ahora.

## Feature flags
- Stories, doble-tap like, PWA offline: ya incluidos y aditivos.

## Tests
- `pytest -q` (ver carpeta `/tests`).

