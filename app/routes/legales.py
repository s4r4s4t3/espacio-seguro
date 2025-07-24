# app/routes/legales.py

from flask import Blueprint, render_template

# ✅ Blueprint para legales (términos y privacidad)
legales_bp = Blueprint('legales', __name__)

# Términos y Condiciones
@legales_bp.route('/terms')
def terms():
    # Renderiza la plantilla de términos y condiciones
    return render_template('terms.html')

# Política de Privacidad
@legales_bp.route('/privacy')
def privacy():
    # Renderiza la plantilla de privacidad
    return render_template('privacy.html')
