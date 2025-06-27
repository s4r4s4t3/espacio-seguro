from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.home'))

        else:
            flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_input = request.form['password']

        # Validación: nombre de usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("⚠️ Ese nombre de usuario ya está registrado. Elegí otro.", "danger")
            return redirect(url_for('auth.register'))

        # Validación: email ya existe
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("⚠️ Ese correo electrónico ya está en uso. Probá con otro.", "danger")
            return redirect(url_for('auth.register'))

        # Crear usuario nuevo
        password = generate_password_hash(password_input, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Usuario registrado con éxito", "success")
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/crear-usuario')
def crear_usuario():
    from werkzeug.security import generate_password_hash
    from app.models import User
    from app import db

    username = "prueba"
    email = "prueba@email.com"
    password = "1234"

    # Evitar duplicado
    if User.query.filter_by(username=username).first():
        return "El usuario ya existe."

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    nuevo_usuario = User(username=username, email=email, password=hashed_password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return "Usuario creado con éxito: usuario = prueba / contraseña = 1234"
