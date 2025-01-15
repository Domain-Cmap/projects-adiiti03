import os
import sqlite3

def database_connection():
    if not os.path.isfile('database.db'):
        connection = sqlite3.connect('database.db')
        with open('schema.sql') as f:
            connection.executescript(f.read())
    else:
        connection = sqlite3.connect('database.db')
    return connection

def insert_into_users(name, password):
    with database_connection() as connection:
        connection.execute(
            'INSERT INTO users (name, password) VALUES (?, ?)',
            (name, password)
        )

def get_all_users_data():
    with database_connection() as connection:
        return connection.execute('SELECT * FROM users').fetchall()

def insert_into_assets(user_id, coin, amount, date):
    with database_connection() as connection:
        connection.execute(
            'INSERT INTO assets (user_id, coin, amount, date) VALUES (?, ?, ?, ?)',
            (user_id, coin, amount, date)
        )

def get_all_asset_data():
    with database_connection() as connection:
        return connection.execute('SELECT * FROM assets').fetchall()
