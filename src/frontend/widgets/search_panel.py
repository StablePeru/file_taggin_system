# src/frontend/widgets/search_panel.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox, QListWidgetItem, QHBoxLayout
)
from .file_details import FileDetails  # Importar el widget de detalles

class SearchPanel(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QPushButton("Panel de Búsqueda")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setEnabled(False)
        layout.addWidget(title)

        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por etiquetas separadas por '+' (ej. Trabajo+Urgente)")
        layout.addWidget(self.search_input)

        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.show_file_details)
        layout.addWidget(self.results_list)

        # Widget de detalles del archivo
        self.file_details_widget = FileDetails("", self.backend)
        self.file_details_widget.hide()  # Inicialmente oculto
        layout.addWidget(self.file_details_widget)

        self.setLayout(layout)

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Buscar", "Por favor, ingresa al menos una etiqueta para buscar.")
            return

        tags = [tag.strip() for tag in query.split('+') if tag.strip()]
        if not tags:
            QMessageBox.warning(self, "Buscar", "La búsqueda debe contener al menos una etiqueta válida.")
            return

        files = self.backend.search_engine.search_by_tags(tags)
        if not files:
            QMessageBox.information(self, "Buscar", "No se encontraron archivos con las etiquetas especificadas.")
            self.results_list.clear()
            self.file_details_widget.hide()
            return

        self.results_list.clear()
        for file in files:
            self.results_list.addItem(file)
        self.file_details_widget.hide()

    def show_file_details(self, item):
        file_path = item.text()
        self.file_details_widget.setParent(None)
        self.file_details_widget = FileDetails(file_path, self.backend)
        self.layout().addWidget(self.file_details_widget)
        self.file_details_widget.show()
