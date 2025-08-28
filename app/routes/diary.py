# app/routes/diary.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.models import db, DiaryEntry  # Usar 'app.' para evitar problemas con imports relativos

# === Blueprint del Diario ===
diary_bp = Blueprint('diary', __name__)

# === Ruta principal del Diario Personal ===
@diary_bp.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if not content:
            flash(_('No podés guardar una entrada vacía.'), 'warning')
        else:
            new_entry = DiaryEntry(content=content, author=current_user)
            db.session.add(new_entry)
            db.session.commit()
            flash(_('Entrada guardada con éxito.'), 'success')
            return redirect(url_for('diary.diary'))

    # Mostrar entradas propias (ordenadas por fecha descendente)
    entries = DiaryEntry.query.filter_by(author=current_user).order_by(DiaryEntry.date_created.desc()).all()
    return render_template('diary.html', entries=entries)
