# src/frontend/widgets/search_panel.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget

class SearchPanel(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por etiquetas...")

        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.perform_search)

        self.results_list = QListWidget()

        layout.addWidget(self.search_input)
        layout.addWidget(search_button)
        layout.addWidget(self.results_list)

        self.setLayout(layout)

    def perform_search(self):
        query = self.search_input.text().split('+')
        files = self.backend.search_engine.search_by_tags(query)
        self.results_list.clear()
        for file in files:
            self.results_list.addItem(file)
