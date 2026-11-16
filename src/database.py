import sqlite3
import os

DB_PATH = "data/users.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            email TEXT,
            password TEXT,
            state TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user(chat_id, email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (chat_id, email, password, state)
        VALUES (?, ?, ?, 'active')
    ''', (chat_id, email, password))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id, email, password FROM users')
    users = cursor.fetchall()
    conn.close()
    return users
