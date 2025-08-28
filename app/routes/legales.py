# app/routes/legales.py

from flask import Blueprint, render_template

# === Blueprint para legales (Términos y Privacidad) ===
legales_bp = Blueprint('legales', __name__)

# === Ruta: Términos y Condiciones ===
@legales_bp.route('/terms')
def terms():
    return render_template('terms.html')

# === Ruta: Política de Privacidad ===
@legales_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')
