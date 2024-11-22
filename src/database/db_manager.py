# src/database/db_manager.py

import sqlite3
from .models import Tag, FileTag  # Importación relativa

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

    # Operaciones CRUD para Tags
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

    def update_tag(self, tag_id: int, new_name: str, new_category: str):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE tags SET name = ?, category = ? WHERE id = ?', (new_name, new_category, tag_id))
        self.conn.commit()

    def delete_tag(self, tag_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        self.conn.commit()

    # Operaciones CRUD para FileTags
    def add_file_tag(self, file_tag: FileTag):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO file_tags (file_path, tag_id) VALUES (?, ?)', (file_tag.file_path, file_tag.tag_id))
        self.conn.commit()
        return cursor.lastrowid

    def get_file_tags(self, file_path: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ft.id, ft.file_path, ft.tag_id
            FROM file_tags ft
            JOIN tags t ON ft.tag_id = t.id
            WHERE ft.file_path = ?
        ''', (file_path,))
        rows = cursor.fetchall()
        return [FileTag(*row) for row in rows]

    def delete_file_tag(self, file_tag_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM file_tags WHERE id = ?', (file_tag_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
