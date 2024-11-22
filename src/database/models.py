# src/database/models.py

import sqlite3

class Tag:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

class FileTag:
    def __init__(self, file_path, tag_id):
        self.file_path = file_path
        self.tag_id = tag_id

# Otros modelos según se necesiten
