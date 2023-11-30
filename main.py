# Импортируем модуль json для работы с JSON-данными
import json
import sqlite3

# Импортируем класс Flask из библиотеки Flask и модуль request для работы с запросами
from flask import Flask, request, flash  #

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


@app.route('/api/v1/users/create/', methods=['POST'])
def create_user():
    # fields = request.form.keys()
    # ok = False
    # for item in fields:
    #     if item == 'name':
    #         ok = True
    #         break
    # if not ok:
    #     return 'error: field "name" does not exist in request'
    surname = request.form['surname']
    name = request.form['name']
    middle_name = request.form['middle_name']
    phone = request.form['phone']
    email = request.form['email']

    if not surname or not name or not phone or not email:
        return 'one or more fields are required'

    conn = get_db_connection()
    conn.execute('INSERT INTO users (surname, name, middle_name, phone, email) VALUES (?, ?, ?, ?, ?)',
                 (surname, name, middle_name, phone, email.lower()))
    conn.commit()
    conn.close()
    list1 = ['1', '2']

    return list1


app.run()

