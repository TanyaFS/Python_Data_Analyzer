# Импортируем модуль json для работы с JSON-данными
import json
import sqlite3

# Импортируем класс Flask из библиотеки Flask и модуль request для работы с запросами
from flask import Flask, request  #

from init_db import init_db

# Создаем объект класса Flask, который представляет веб-приложение
app = Flask(__name__)

init_db()
# Декоратор @app.route() используется для определения URL-маршрута,
# который будет обрабатываться данной функцией. В данном случае, это '/api/v1/'
@app.route('/api/v1/')
def get_first_request():
    return "<h1>Hi</h1>"


@app.route('/api/v1/json/', methods=['POST'])
def get_json():
    data = request.get_json()
    test = data.get('test', '')
    if test == 88:
        return json.dumps({
            'name': 'Tanya',
            'age': 18
        })
    else:
        return "not found"

def get_db_connection():
    conn = sqlite3.connect('./database/contacts.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user():
    conn = get_db_connection()
    conn.execute('INSERT INTO users (surname, name, middle_name, phone, email) VALUES (?, ?, ?, ?, ?)',
                 ('Smith', 'John', 'Daniel', '777777777', 'j.smith@mail.com'))
    conn.commit()
    conn.close()


create_user()
app.run()

