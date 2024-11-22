# src/frontend/main_window.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from widgets.tag_editor import TagEditor
from widgets.search_panel import SearchPanel

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sistema de Etiquetado de Archivos")
        self.setGeometry(100, 100, 800, 600)  # Puedes ajustar el tamaño según prefieras

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Barra de Herramientas Superior
        top_bar = QHBoxLayout()
        title = QLabel("Sistema de Etiquetado de Archivos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        # Botón para arrastrar y soltar archivos (implementación básica)
        self.upload_button = QPushButton("Agregar Archivos")
        self.upload_button.clicked.connect(self.upload_files)
        top_bar.addWidget(self.upload_button)

        main_layout.addLayout(top_bar)

        # Widgets principales
        self.tag_editor = TagEditor(self.backend)
        self.search_panel = SearchPanel(self.backend)

        main_layout.addWidget(self.tag_editor)
        main_layout.addWidget(self.search_panel)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.show()

    def upload_files(self):
        # Implementar la lógica para arrastrar y soltar archivos o seleccionar archivos
        from PyQt5.QtWidgets import QFileDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos", "", "Todos los Archivos (*)")
        if files:
            # Por ahora, simplemente mostrar los archivos seleccionados
            # Más adelante, implementaremos la lógica para etiquetarlos
            print("Archivos seleccionados:", files)
