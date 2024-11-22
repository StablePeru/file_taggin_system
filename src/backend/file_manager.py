# src/backend/file_manager.py

import os

class FileManager:
    def __init__(self):
        pass

    def list_files(self, directory: str):
        return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def get_file_metadata(self, file_path: str):
        stats = os.stat(file_path)
        return {
            'size': stats.st_size,
            'modified_time': stats.st_mtime,
            'type': os.path.splitext(file_path)[1]
        }

    # Otras funcionalidades relacionadas con archivos
