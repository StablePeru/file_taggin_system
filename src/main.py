# src/main.py

import sys
import os
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow
from database.db_manager import DBManager
from backend.tag_manager import TagManager
from backend.file_manager import FileManager
from backend.search_engine import SearchEngine
from utils.logger import app_logger

class Backend:
    def __init__(self):
        # Crear directorio de logs si no existe
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            app_logger.info(f"Directorio de logs creado en {logs_dir}")

        self.db_manager = DBManager()
        self.tag_manager = TagManager(self.db_manager)
        self.file_manager = FileManager(self.db_manager)
        self.search_engine = SearchEngine(self.db_manager)
        # Inicializar otros componentes como AI, ElasticSearch, etc.

def main():
    app = QApplication(sys.argv)
    backend = Backend()
    window = MainWindow(backend)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
