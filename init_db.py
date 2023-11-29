import sqlite3


def init_db():
    connection = sqlite3.connect('./database/contacts.db')

    with open('schema.sql') as file:
        connection.executescript(file.read())
