# src/frontend/widgets/tagged_files_list.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QMessageBox, QLabel, QHBoxLayout
)
from .file_details import FileDetails
from .tag_selection_dialog import TagSelectionDialog

class TaggedFilesList(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Archivos Etiquetados")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Lista de archivos etiquetados
        self.files_list = QListWidget()
        self.refresh_files()
        self.files_list.itemDoubleClicked.connect(self.show_file_details)
        layout.addWidget(self.files_list)

        # Botones de acción
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Editar Etiquetas")
        edit_button.clicked.connect(self.edit_tags)
        button_layout.addStretch()
        button_layout.addWidget(edit_button)

        layout.addLayout(button_layout)

        # Widget de detalles del archivo
        self.file_details_widget = FileDetails("", self.backend)
        self.file_details_widget.hide()  # Inicialmente oculto
        layout.addWidget(self.file_details_widget)

        self.setLayout(layout)

    def refresh_files(self):
        self.files_list.clear()
        # Obtener todos los archivos etiquetados
        all_file_tags = self.backend.file_manager.get_all_tagged_files()
        unique_files = list(set([ft.file_path for ft in all_file_tags]))
        for file in unique_files:
            self.files_list.addItem(file)

    def show_file_details(self, item):
        file_path = item.text()
        self.file_details_widget.setParent(None)
        self.file_details_widget = FileDetails(file_path, self.backend)
        self.layout().addWidget(self.file_details_widget)
        self.file_details_widget.show()

    def edit_tags(self):
        selected_items = self.files_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Editar Etiquetas", "Por favor, selecciona al menos un archivo para editar sus etiquetas.")
            return

        for item in selected_items:
            file_path = item.text()
            tags = self.backend.tag_manager.get_all_tags()
            if not tags:
                QMessageBox.warning(self, "Editar Etiquetas", "No hay etiquetas disponibles. Por favor, agrega etiquetas primero.")
                return

            # Crear una lista de etiquetas para selección
            tag_names = [f"{tag.name} ({tag.category})" for tag in tags]

            # Obtener etiquetas actuales del archivo
            current_file_tags = self.backend.file_manager.get_tags_for_file(file_path)
            current_tag_displays = [f"{tag.name} ({tag.category})" for tag in tags if tag.id in [ft.tag_id for ft in current_file_tags]]

            # Crear y mostrar el diálogo de selección de etiquetas, pasando el file_path
            tag_selection_dialog = TagSelectionDialog(file_path, tag_names, self)
            # Preseleccionar las etiquetas actuales
            tag_selection_dialog.list_widget.clearSelection()
            for i in range(tag_selection_dialog.list_widget.count()):
                item_widget = tag_selection_dialog.list_widget.item(i)
                if item_widget.text() in current_tag_displays:
                    item_widget.setSelected(True)

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
                    # Eliminar todas las etiquetas actuales
                    for ft in current_file_tags:
                        self.backend.file_manager.remove_tag_from_file(ft.id)
                    # Asignar las nuevas etiquetas al archivo
                    self.backend.file_manager.add_tags_to_file(file_path, selected_tag_ids)
                    QMessageBox.information(
                        self, "Editar Etiquetas",
                        f"Etiquetas actualizadas para el archivo '{file_path}'."
                    )
        self.refresh_files()
        self.file_details_widget.hide()
