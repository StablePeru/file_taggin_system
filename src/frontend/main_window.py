# src/frontend/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from widgets.tag_editor import TagEditor
from widgets.search_panel import SearchPanel
from widgets.tag_selection_dialog import TagSelectionDialog

class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sistema de Etiquetado de Archivos")
        self.setGeometry(100, 100, 800, 600)  # Puedes ajustar el tamaño según prefieras
        self.setAcceptDrops(True)  # Habilitar arrastrar y soltar

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Barra de Herramientas Superior
        top_bar = QHBoxLayout()
        title = QLabel("Sistema de Etiquetado de Archivos")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        # Botón para agregar archivos
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
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar Archivos", "", "Todos los Archivos (*)")
        if files:
            self.tag_files(files)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        files = [url.toLocalFile() for url in urls]
        if files:
            self.tag_files(files)

    def tag_files(self, files):
        for file_path in files:
            # Obtener todas las etiquetas disponibles
            tags = self.backend.tag_manager.get_all_tags()
            if not tags:
                QMessageBox.warning(self, "Etiquetar Archivo", "No hay etiquetas disponibles. Por favor, agrega etiquetas primero.")
                return

            # Crear una lista de etiquetas para selección
            tag_names = [f"{tag.name} ({tag.category})" for tag in tags]

            # Crear y mostrar el diálogo de selección de etiquetas
            tag_selection_dialog = TagSelectionDialog(tag_names, self)
            if tag_selection_dialog.exec_():
                selected_tags = tag_selection_dialog.get_selected_tags()
                if selected_tags:
                    # Obtener los IDs de las etiquetas seleccionadas
                    selected_tag_ids = []
                    for tag_display in selected_tags:
                        for tag in tags:
                            display = f"{tag.name} ({tag.category})"
                            if display == tag_display:
                                selected_tag_ids.append(tag.id)
                                break
                    # Asignar las etiquetas al archivo
                    self.backend.file_manager.add_tags_to_file(file_path, selected_tag_ids)
                    QMessageBox.information(
                        self, "Etiquetar Archivo",
                        f"Archivo '{file_path}' etiquetado con {len(selected_tag_ids)} etiquetas."
                    )
