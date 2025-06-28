# diary.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, DiaryEntry

# Creamos el Blueprint para el diario
diary_bp = Blueprint('diary', __name__)

# Ruta principal del diario
@diary_bp.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('No podés guardar una entrada vacía.')
        else:
            # Crear nueva entrada asociada al usuario actual
            new_entry = DiaryEntry(content=content, author=current_user)
            db.session.add(new_entry)
            db.session.commit()
            flash('Entrada guardada con éxito.')
            return redirect(url_for('diary.diary'))

    # Mostrar todas las entradas del usuario ordenadas por fecha
    entries = DiaryEntry.query.filter_by(author=current_user).order_by(DiaryEntry.date_created.desc()).all()
    return render_template('diary.html', entries=entries)
