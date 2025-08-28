"""
Rutas para la página de configuración (ajustes) de la aplicación.

La página de configuración centraliza opciones como el cambio de
idioma, la selección de tema (oscuro/claro), información de la app
y enlaces legales.  Esta vista es accesible desde el menú principal
de la aplicación y requiere que el usuario esté autenticado.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from flask_babel import _

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/settings')
@login_required
def settings():
    """Renderiza la página de configuración para el usuario autenticado."""
    return render_template('settings.html')