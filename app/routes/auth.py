# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# ----------------------------
# Ruta de Login Normal
# ----------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('Credenciales inválidas. Intenta de nuevo.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

# ----------------------------
# Ruta de Registro
# ----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El usuario ya existe. Elige otro nombre.')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password, profile_picture='default.png')
        db.session.add(new_user)
        db.session.commit()

        flash('Usuario creado con éxito. Ahora puedes iniciar sesión.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# ----------------------------
# Ruta de Logout
# ----------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ----------------------------
# Ruta de Login con Google
# ----------------------------
@auth_bp.route('/login/google')
def login_google():
    # 👇 Aquí pondrás la lógica de OAuth real
    # Por ahora, dejaremos un redirect de prueba
    flash('Función de login con Google aún en desarrollo.')
    return redirect(url_for('auth.login'))

