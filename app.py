import sqlite3

# Импортируем класс Flask из библиотеки flask, модуль request для работы с запросами
from flask import Flask, request, render_template, url_for, flash, redirect, abort

from init_db import init_db

# Создаем объект класса Flask, который представляет веб-приложение
app = Flask(__name__)  # Application initialization
app.config['SECRET_KEY'] = 'infoChart'

init_db()


# Декоратор @app.route() используется для определения URL-маршрута,
# который будет обрабатываться данной функцией. В данном случае, это '/create'

# Описываем CRUD операции: create, read, update, delete
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['firstname']
        middle_name = request.form['middle_name']
        phone = request.form['phone']
        email = request.form['email']

        if not surname or not name or not phone or not email:
            flash('one or more fields are required')
            return render_template('create.html')
        if not phone.isdigit():
            flash('phone should be a number')
            return render_template('create.html')
        else:
            int_phone = int(phone)
            conn = get_db_connection()
            conn.execute('INSERT INTO users (surname, name, middle_name, phone, email) '
                         'VALUES (?, ?, ?, ?, ?)',
                         (surname, name, middle_name, int_phone, email.lower()))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)


@app.route('/search', methods=['POST'])
def search():
    data = request.form['filter']
    if not data:
        flash('name is required')

    search_like = data + '%'
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users WHERE surname LIKE ? OR name LIKE ?',
                         (search_like, search_like)).fetchall()
    conn.close()

    return render_template('index.html', users=users)


@app.route('/<int:user_id>/edit', methods=('GET', 'POST'))
def edit(user_id):
    user_to_edit = get_user_by(user_id)

    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['firstname']
        middle_name = request.form['middle_name']
        phone = request.form['phone']
        email = request.form['email']

        if not surname or not name or not phone or not email:
            flash('one or more fields are required')
            return return_error('edit.html', user_to_edit)

        if not phone.isdigit():
            flash('phone should be a number')
            return return_error('edit.html', user_to_edit)

        int_phone = int(phone)

        conn = get_db_connection()
        conn.execute('UPDATE users SET name = ?, surname = ?, middle_name = ?, phone = ?, email = ?, updated_at = '
                     'CURRENT_TIMESTAMP'
                     ' WHERE id = ?',
                     (name, surname, middle_name, int_phone, email, user_id))
        conn.commit()

        updated_user = conn.execute('SELECT * FROM users WHERE id = ?',
                                    (user_id,)).fetchone()
        conn.close()

        return render_template('index.html', users=[updated_user])

    return render_template('edit.html', user=user_to_edit)


@app.route('/<int:user_id>/delete', methods=('POST',))
def delete(user_id):
    user = get_user_by(user_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user['surname']))
    return redirect(url_for('index'))


def return_error(link, user_id):
    return render_template(link, user=user_id)


def get_db_connection():
    conn = sqlite3.connect('./database/contacts.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


app.run()  # Start of the application
