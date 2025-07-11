# app/routes/legales.py

from flask import Blueprint, render_template

# ✅ Creamos el Blueprint 'legales'
legales_bp = Blueprint('legales', __name__)

# ✅ Ruta para Términos y Condiciones
@legales_bp.route('/terms')
def terms():
    return render_template('terms.html')

# ✅ Ruta para Política de Privacidad
@legales_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')
