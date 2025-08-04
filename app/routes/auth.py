# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_babel import _
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# 🔐 Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(_('Bienvenido de nuevo, %(username)s!', username=username), 'success')

            # Redirige a bienvenida si no aceptó términos
            if not user.accepted_terms:
                return redirect(url_for('home.welcome'))
            # Después de iniciar sesión y aceptar términos lleva al feed directamente
            return redirect(url_for('home.feed'))

        flash(_('Credenciales inválidas. Intenta de nuevo.'), 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

# 📝 Registro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # opcional, depende del form
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(_('El usuario "%(username)s" ya existe. Elige otro nombre.', username=username), 'warning')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)

        # Nuevo usuario se crea con foto por defecto y accepted_terms=False
        new_user = User(username=username, email=email, password=hashed_password, profile_picture='default.png')
        db.session.add(new_user)
        db.session.commit()

        flash(_('Usuario creado con éxito. Ahora puedes iniciar sesión.'), 'success')
        login_user(new_user)
        return redirect(url_for('home.welcome'))

    return render_template('register.html')

# 🔓 Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('Sesión cerrada correctamente.'), 'info')
    return redirect(url_for('auth.login'))

# 🔐 Login con Google (futuro)
"""
@auth_bp.route('/login/google')
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash(_('Error al obtener datos de Google.'), 'danger')
        return redirect(url_for('auth.login'))

    user_info = resp.json()
    email = user_info["email"]
    username = user_info.get("name", email.split("@")[0])

    user = User.query.filter_by(username=username).first()
    if not user:
        new_user = User(username=username, password="oauth_google", profile_picture='default.png')
        db.session.add(new_user)
        db.session.commit()
        user = new_user

    login_user(user)
    flash(_('Bienvenido %(username)s!', username=username), 'success')

    if not user.accepted_terms:
        return redirect(url_for('home.welcome'))
    return redirect(url_for('home.home'))
"""
