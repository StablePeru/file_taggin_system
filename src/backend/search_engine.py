# src/backend/search_engine.py
import os
from database.db_manager import DBManager
from database.models import Tag, FileTag

class SearchEngine:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def search_by_tags(self, tags: list):
        if not tags:
            return []

        # Obtener IDs de las etiquetas
        cursor = self.db.conn.cursor()
        placeholder = ','.join(['?'] * len(tags))
        cursor.execute(f'SELECT id FROM tags WHERE name IN ({placeholder})', tags)
        tag_ids = [row[0] for row in cursor.fetchall()]

        if not tag_ids:
            return []

        # Buscar archivos que tengan todas las etiquetas
        files = set()
        for tag_id in tag_ids:
            cursor.execute('SELECT file_path FROM file_tags WHERE tag_id = ?', (tag_id,))
            tag_files = set([row[0] for row in cursor.fetchall()])
            if not files:
                files = tag_files
            else:
                files = files.intersection(tag_files)

        return list(files)

    def advanced_filters(self, files, date_modified=None, file_type=None, size=None):
        filtered_files = []
        for file in files:
            metadata = self.get_file_metadata(file)
            if date_modified:
                if metadata['modified_time'] < date_modified:
                    continue
            if file_type:
                if metadata['type'] != file_type:
                    continue
            if size:
                if metadata['size'] > size:
                    continue
            filtered_files.append(file)
        return filtered_files

    def get_file_metadata(self, file_path: str):
        stats = os.stat(file_path)
        return {
            'size': stats.st_size,
            'modified_time': stats.st_mtime,
            'type': os.path.splitext(file_path)[1]
        }

    def get_preview(self, file_path: str):
        # Implementar la lógica para generar una vista previa
        # Por ejemplo, generar miniaturas para imágenes, fragmentos para texto, etc.
        pass
