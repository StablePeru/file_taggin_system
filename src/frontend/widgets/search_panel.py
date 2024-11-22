# src/frontend/widgets/search_panel.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox

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
        layout.addWidget(self.results_list)

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
            return

        self.results_list.clear()
        for file in files:
            self.results_list.addItem(file)
