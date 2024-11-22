# src/backend/file_manager.py

import os
from database.db_manager import DBManager
from database.models import FileTag
from utils.logger import app_logger

class FileManager:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def list_files(self, directory: str):
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        app_logger.info(f"Listados {len(files)} archivos en el directorio {directory}.")
        return files

    def get_file_metadata(self, file_path: str):
        try:
            stats = os.stat(file_path)
            metadata = {
                'size': stats.st_size,
                'modified_time': stats.st_mtime,
                'type': os.path.splitext(file_path)[1]
            }
            app_logger.info(f"Obtenida metadata para el archivo {file_path}: {metadata}")
            return metadata
        except FileNotFoundError:
            app_logger.error(f"Archivo no encontrado: {file_path}")
            return {
                'size': 0,
                'modified_time': 0,
                'type': ''
            }

    def add_tags_to_file(self, file_path: str, tag_ids: list):
        for tag_id in tag_ids:
            self.add_tag_to_file(file_path, tag_id)

    def add_tag_to_file(self, file_path: str, tag_id: int):
        file_tag = FileTag(id=None, file_path=file_path, tag_id=tag_id)
        file_tag_id = self.db.add_file_tag(file_tag)
        app_logger.info(f"Etiqueta ID {tag_id} asignada al archivo {file_path} (FileTag ID: {file_tag_id})")
        return file_tag_id

    def get_tags_for_file(self, file_path: str):
        file_tags = self.db.get_file_tags(file_path)
        app_logger.info(f"Obtenidas {len(file_tags)} etiquetas para el archivo {file_path}.")
        return file_tags

    def remove_tag_from_file(self, file_tag_id: int):
        self.db.delete_file_tag(file_tag_id)
        app_logger.info(f"Etiqueta del archivo eliminada: FileTag ID {file_tag_id}")
    
    def get_all_tagged_files(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT DISTINCT file_path FROM file_tags')
        rows = cursor.fetchall()
        return [FileTag(file_path=row[0], tag_id=None) for row in rows]  # tag_id=None es irrelevante aquí
