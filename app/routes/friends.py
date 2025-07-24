# app/routes/friends.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_babel import _
from app.models import User, FriendRequest, db

amigos_bp = Blueprint('amigos', __name__)

@amigos_bp.route('/amigos')
@login_required
def amigos():
    # Amigos aceptados
    amigos = User.query.join(
        FriendRequest, ((FriendRequest.sender_id == User.id) | (FriendRequest.receiver_id == User.id))
    ).filter(FriendRequest.status == 'accepted') \
     .filter((FriendRequest.sender_id == current_user.id) | (FriendRequest.receiver_id == current_user.id)) \
     .filter(User.id != current_user.id) \
     .all()

    # Solicitudes recibidas: con JOIN para username real
    solicitudes_query = (
        db.session.query(FriendRequest, User.username)
        .join(User, FriendRequest.sender_id == User.id)
        .filter(FriendRequest.receiver_id == current_user.id, FriendRequest.status == 'pending')
        .all()
    )
    solicitudes = [
        {
            "id": solicitud.id,
            "sender_id": solicitud.sender_id,
            "sender_username": username
        }
        for solicitud, username in solicitudes_query
    ]

    # Todos los demás usuarios
    usuarios = User.query.filter(User.id != current_user.id).all()

    return render_template("amigos.html", usuarios=usuarios, amigos=amigos, solicitudes=solicitudes)

@amigos_bp.route('/enviar_solicitud/<int:user_id>')
@login_required
def enviar_solicitud(user_id):
    if not FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=user_id).first():
        nueva = FriendRequest(sender_id=current_user.id, receiver_id=user_id)
        db.session.add(nueva)
        db.session.commit()
        flash(_("Solicitud enviada"), "info")
    return redirect(url_for('amigos.amigos'))

@amigos_bp.route('/aceptar/<int:solicitud_id>')
@login_required
def aceptar(solicitud_id):
    solicitud = FriendRequest.query.get_or_404(solicitud_id)
    if solicitud.receiver_id == current_user.id:
        solicitud.status = 'accepted'
        db.session.commit()
        flash(_("Solicitud aceptada"), "success")
    return redirect(url_for('amigos.amigos'))

@amigos_bp.route('/rechazar/<int:solicitud_id>')
@login_required
def rechazar(solicitud_id):
    solicitud = FriendRequest.query.get_or_404(solicitud_id)
    if solicitud.receiver_id == current_user.id:
        solicitud.status = 'rejected'
        db.session.commit()
        flash(_("Solicitud rechazada"), "danger")
    return redirect(url_for('amigos.amigos'))
