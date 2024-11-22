# src/frontend/main_window.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from widgets.tag_editor import TagEditor
from widgets.search_panel import SearchPanel

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sistema de Etiquetado de Archivos")
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.tag_editor = TagEditor(self.backend)
        self.search_panel = SearchPanel(self.backend)

        layout.addWidget(self.tag_editor)
        layout.addWidget(self.search_panel)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()
