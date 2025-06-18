from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import hashlib
import os
import subprocess

app = Flask(__name__)

app.secret_key = "simple123"

app.config['DEBUG'] = True

def init_db():
    """Инициализация простой базы данных"""
    conn = sqlite3.connect('simple.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            name TEXT,
            message TEXT
        )
    ''')
    conn.execute("INSERT OR IGNORE INTO messages (id, name, message) VALUES (1, 'Админ', 'Добро пожаловать!')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/messages')
def messages():
    """Страница с сообщениями"""
    conn = sqlite3.connect('simple.db')
    cursor = conn.execute("SELECT name, message FROM messages ORDER BY id DESC")
    messages_list = cursor.fetchall()
    conn.close()
    return render_template('messages.html', messages=messages_list)

@app.route('/add_message', methods=['POST'])
def add_message():
    """Добавление нового сообщения"""
    name = request.form.get('name', '')
    message = request.form.get('message', '')
    
    if not name or not message:
        flash('Заполните все поля!')
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('simple.db')
    query = f"INSERT INTO messages (name, message) VALUES ('{name}', '{message}')"
    try:
        conn.execute(query)
        conn.commit()
        flash('Сообщение добавлено!')
    except Exception as e:
        flash(f'Ошибка: {e}')
    finally:
        conn.close()
    
    return redirect(url_for('messages'))

@app.route('/search')
def search():
    """Поиск сообщений"""
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', results=[])
    
    conn = sqlite3.connect('simple.db')
    search_query = f"SELECT name, message FROM messages WHERE message LIKE '%{query}%'"
    try:
        cursor = conn.execute(search_query)
        results = cursor.fetchall()
    except Exception as e:
        results = []
        flash(f'Ошибка поиска: {e}')
    finally:
        conn.close()
    
    return render_template('search.html', results=results, query=query)

@app.route('/admin')
def admin():
    """Простая админ панель"""
    return render_template('admin.html')

@app.route('/admin/ping', methods=['POST'])
def admin_ping():
    """Админ функция - пинг сервера"""
    host = request.form.get('host', 'localhost')
    
    try:
        command = f"ping -c 1 {host}"
        result = subprocess.check_output(command, shell=True, text=True, timeout=5)
        return render_template('admin.html', ping_result=result)
    except Exception as e:
        return render_template('admin.html', ping_result=f"Ошибка: {e}")

@app.route('/health')
def health():
    """Проверка здоровья приложения"""
    return {"status": "OK", "message": "Simple security demo app"}

def weak_hash(password):
    """Слабая функция хеширования"""
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == '__main__':
    init_db()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
