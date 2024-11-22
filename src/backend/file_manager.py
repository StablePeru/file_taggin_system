# src/backend/file_manager.py

import os
from database.db_manager import DBManager
from database.models import FileTag

class FileManager:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def list_files(self, directory: str):
        return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def get_file_metadata(self, file_path: str):
        stats = os.stat(file_path)
        return {
            'size': stats.st_size,
            'modified_time': stats.st_mtime,
            'type': os.path.splitext(file_path)[1]
        }

    def add_tag_to_file(self, file_path: str, tag_id: int):
        file_tag = FileTag(id=None, file_path=file_path, tag_id=tag_id)
        return self.db.add_file_tag(file_tag)

    def get_tags_for_file(self, file_path: str):
        return self.db.get_file_tags(file_path)

    def remove_tag_from_file(self, file_tag_id: int):
        self.db.delete_file_tag(file_tag_id)

    # Puedes agregar más funcionalidades según se necesiten
