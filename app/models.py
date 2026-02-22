import os
import sqlite3

from app.config import DATABASE, DATA_DIR


def get_connection():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()

    cursor = conn.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    if count == 0:
        seed_db(conn)

    conn.close()


def seed_db(conn):
    users = [
        ('Иван Петров', 'ivan@example.com'),
        ('Мария Сидорова', 'maria@example.com'),
        ('Алексей Козлов', 'alexey@example.com'),
        ('Елена Новикова', 'elena@example.com'),
        ('Дмитрий Волков', 'dmitry@example.com'),
    ]
    conn.executemany(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        users
    )
    conn.commit()


def get_all_users():
    conn = get_connection()
    cursor = conn.execute('SELECT id, name, email FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users


def create_user(name, email):
    conn = get_connection()
    cursor = conn.execute(
        'INSERT INTO users (name, email) VALUES (?, ?)',
        (name, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return get_user_by_id(user_id)


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.execute(
        'SELECT id, name, email FROM users WHERE id = ?',
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return dict(row)
