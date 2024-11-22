# src/database/db_manager.py

import sqlite3
from models import Tag, FileTag

class DBManager:
    def __init__(self, db_path='tags.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                tag_id INTEGER,
                FOREIGN KEY(tag_id) REFERENCES tags(id)
            )
        ''')
        # Crear otras tablas según se necesiten
        self.conn.commit()

    def add_tag(self, tag: Tag):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO tags (name, category) VALUES (?, ?)', (tag.name, tag.category))
        self.conn.commit()
        return cursor.lastrowid

    def get_tags(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, category FROM tags')
        rows = cursor.fetchall()
        return [Tag(*row) for row in rows]

    # Implementar otras operaciones CRUD
