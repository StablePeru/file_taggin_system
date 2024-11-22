# src/frontend/main_window.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QInputDialog
from .widgets.tag_editor import TagEditor
from .widgets.search_panel import SearchPanel

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
            for file_path in files:
                # Aquí puedes implementar la lógica para etiquetar cada archivo seleccionado
                # Por ahora, vamos a pedir al usuario que seleccione una etiqueta para cada archivo
                tags = self.backend.tag_manager.get_all_tags()
                if not tags:
                    QMessageBox.warning(self, "Etiquetar Archivo", "No hay etiquetas disponibles. Por favor, agrega etiquetas primero.")
                    return

                tag_names = [f"{tag.name} ({tag.category})" for tag in tags]
                tag, ok = QInputDialog.getItem(self, "Seleccionar Etiqueta", f"Selecciona una etiqueta para el archivo:\n{file_path}", tag_names, 0, False)
                if ok and tag:
                    # Obtener el ID de la etiqueta seleccionada
                    selected_tag = None
                    for t in tags:
                        tag_display = f"{t.name} ({t.category})"
                        if tag_display == tag:
                            selected_tag = t
                            break
                    if selected_tag:
                        self.backend.file_manager.add_tag_to_file(file_path, selected_tag.id)
                        QMessageBox.information(self, "Etiquetar Archivo", f"Archivo '{file_path}' etiquetado con '{selected_tag.name}'.")
            # Actualizar los resultados de búsqueda si es necesario
