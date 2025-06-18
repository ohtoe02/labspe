from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from prometheus_client import start_http_server, Counter, Histogram, generate_latest
import random
import time
import sqlite3
import hashlib
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # Уязвимость: слабый секретный ключ
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Создаем папку для загрузок
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Метрики Prometheus
REQUESTS = Counter('app_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['method', 'endpoint'])
LOGIN_ATTEMPTS = Counter('login_attempts_total', 'Total login attempts', ['status'])

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    # Добавляем тестового пользователя
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                      ('admin', hashlib.md5('admin123'.encode()).hexdigest(), 'admin@example.com'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Пользователь уже существует
    conn.close()

@app.route('/')
def index():
    REQUESTS.labels(method='GET', endpoint='/').inc()
    return render_template('index.html', user=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Уязвимость: SQL инъекция
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            session['user_id'] = user[0]
            LOGIN_ATTEMPTS.labels(status='success').inc()
            flash('Успешный вход!', 'success')
            return redirect(url_for('dashboard'))
        else:
            LOGIN_ATTEMPTS.labels(status='failed').inc()
            flash('Неверные учетные данные!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            # Уязвимость: слабое хеширование паролей (MD5)
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                          (username, hashlib.md5(password.encode()).hexdigest(), email))
            conn.commit()
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Пользователь уже существует!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не выбран!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран!', 'error')
            return redirect(request.url)
        
        # Уязвимость: недостаточная проверка типов файлов
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash(f'Файл {filename} успешно загружен!', 'success')
        
    return render_template('upload.html')

@app.route('/admin')
def admin():
    # Уязвимость: отсутствие проверки прав доступа
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Уязвимость: выполнение системных команд
    if request.args.get('cmd'):
        try:
            result = subprocess.check_output(request.args.get('cmd'), shell=True, text=True)
            return f"<pre>{result}</pre>"
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template('admin.html')

@app.route('/health')
def health():
    REQUESTS.labels(method='GET', endpoint='/health').inc()
    return jsonify(status="OK")

@app.route('/stress')
def stress():
    start = time.time()
    time.sleep(random.uniform(0.1, 1.0))  # Имитация нагрузки
    latency = time.time() - start
    REQUEST_LATENCY.labels(method='GET', endpoint='/stress').observe(latency)
    return jsonify(status="Stress test completed")

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы!', 'info')
    return redirect(url_for('index'))

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    init_db()
    start_http_server(8000)  # Экспорт метрик на порт 8000
    app.run(host='0.0.0.0', port=5000, debug=True)  # Уязвимость: debug=True в продакшене
