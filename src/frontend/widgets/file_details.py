# src/frontend/widgets/file_details.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout
)

class FileDetails(QWidget):
    def __init__(self, file_path, backend, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Mostrar la ruta del archivo
        file_label = QLabel(f"Archivo: {self.file_path}")
        file_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(file_label)

        # Lista de etiquetas
        self.tag_list = QListWidget()
        self.refresh_tags()
        layout.addWidget(self.tag_list)

        # Botones de acción
        button_layout = QHBoxLayout()
        add_tag_button = QPushButton("Agregar Etiqueta")
        add_tag_button.clicked.connect(self.add_tag)

        remove_tag_button = QPushButton("Eliminar Etiqueta")
        remove_tag_button.clicked.connect(self.remove_tag)

        button_layout.addWidget(add_tag_button)
        button_layout.addWidget(remove_tag_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def refresh_tags(self):
        self.tag_list.clear()
        file_tags = self.backend.file_manager.get_tags_for_file(self.file_path)
        for ft in file_tags:
            tag = self.backend.tag_manager.get_tag_by_id(ft.tag_id)
            if tag:
                self.tag_list.addItem(f"{tag.name} ({tag.category})")

    def add_tag(self):
        tags = self.backend.tag_manager.get_all_tags()
        if not tags:
            QMessageBox.warning(self, "Agregar Etiqueta", "No hay etiquetas disponibles. Por favor, agrega etiquetas primero.")
            return

        # Crear una lista de etiquetas para selección
        tag_names = [f"{tag.name} ({tag.category})" for tag in tags]

        # Crear y mostrar el diálogo de selección de etiquetas
        from widgets.tag_selection_dialog import TagSelectionDialog
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
                self.backend.file_manager.add_tags_to_file(self.file_path, selected_tag_ids)
                QMessageBox.information(
                    self, "Agregar Etiqueta",
                    f"Etiquetas agregadas al archivo '{self.file_path}'."
                )
                self.refresh_tags()

    def remove_tag(self):
        selected_item = self.tag_list.currentItem()
        if selected_item:
            tag_display = selected_item.text()
            name_part = tag_display.split(' (')[0]
            category_part = tag_display.split(' (')[1].rstrip(')')

            confirm = QMessageBox.question(
                self, "Eliminar Etiqueta",
                f"¿Estás seguro de eliminar la etiqueta '{name_part}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                # Obtener el ID de la etiqueta
                tag = self.backend.tag_manager.get_tag_by_name_and_category(name_part, category_part)
                if tag:
                    # Obtener el FileTag correspondiente
                    file_tags = self.backend.file_manager.get_tags_for_file(self.file_path)
                    for ft in file_tags:
                        if ft.tag_id == tag.id:
                            self.backend.file_manager.remove_tag_from_file(ft.id)
                            break
                    QMessageBox.information(
                        self, "Eliminar Etiqueta",
                        f"Etiqueta '{name_part}' eliminada del archivo '{self.file_path}'."
                    )
                    self.refresh_tags()
        else:
            QMessageBox.warning(self, "Eliminar Etiqueta", "Por favor, selecciona una etiqueta para eliminar.")
