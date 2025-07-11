# app/routes/legales.py

from flask import Blueprint, render_template

legales_bp = Blueprint('legales', __name__)

@legales_bp.route('/terms')
def terms():
    return render_template('terms.html')

@legales_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')
