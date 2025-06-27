from flask import Flask, render_template, session, redirect, url_for
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

# Conexión a tu PostgreSQL existente
def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

# Rutas básicas (sin funcionalidad compleja)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# --- Rutas que deben funcionar YA ---
@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/amigos')
def amigos():
    return render_template('amigos.html')

if __name__ == '__main__':
    app.run()