import sqlite3
import os

if os.path.exists('database.db'):
    os.remove('database.db')

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''\
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    key CHAR(36) NOT NULL
)\
''')

cursor.execute('''\
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    FOREIGN KEY(id_user) REFERENCES users(id)              
)\
''')