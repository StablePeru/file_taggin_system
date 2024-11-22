# src/database/models.py

import sqlite3

class Tag:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

class FileTag:
    def __init__(self, id, file_path, tag_id):
        self.id = id
        self.file_path = file_path
        self.tag_id = tag_id

# Puedes agregar más modelos según las necesidades futuras, como Categoría, Versiones, etc.
