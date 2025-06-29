# app/routes/ai.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

ai_bp = Blueprint('ai', __name__)

# Lista de respuestas simuladas
RESPUESTAS_IA = [
    "Gracias por contarme eso. Estoy acá para escucharte.",
    "Te entiendo, seguí contándome lo que sentís.",
    "Estoy orgulloso de vos por compartirlo.",
    "No estás solo/a, contá conmigo.",
    "¿Querés que hablemos de otra cosa?"
]

@ai_bp.route('/ia', methods=['GET', 'POST'])
@login_required
def ia():
    historial = []

    if request.method == 'POST':
        mensaje_usuario = request.form.get('mensaje')
        if mensaje_usuario:
            # Simular respuesta de IA
            respuesta_ia = RESPUESTAS_IA[len(mensaje_usuario) % len(RESPUESTAS_IA)]
            historial.append(('Tú', mensaje_usuario))
            historial.append(('Espacio IA', respuesta_ia))

    return render_template('ai.html', historial=historial, user=current_user)
