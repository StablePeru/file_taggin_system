# src/frontend/widgets/tag_editor.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QInputDialog, QMessageBox

class TagEditor(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QPushButton("Gestión de Etiquetas")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setEnabled(False)
        layout.addWidget(title)

        # Lista de etiquetas
        self.tag_list = QListWidget()
        self.refresh_tags()
        layout.addWidget(self.tag_list)

        # Botones de acción
        button_layout = QHBoxLayout()
        add_button = QPushButton("Agregar Etiqueta")
        add_button.clicked.connect(self.add_tag)

        edit_button = QPushButton("Editar Etiqueta")
        edit_button.clicked.connect(self.edit_tag)

        delete_button = QPushButton("Eliminar Etiqueta")
        delete_button.clicked.connect(self.delete_tag)

        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def refresh_tags(self):
        self.tag_list.clear()
        tags = self.backend.tag_manager.get_all_tags()
        for tag in tags:
            self.tag_list.addItem(f"{tag.name} ({tag.category})")

    def add_tag(self):
        name, ok = QInputDialog.getText(self, "Agregar Etiqueta", "Nombre de la Etiqueta:")
        if ok and name:
            category, ok_cat = QInputDialog.getText(self, "Agregar Etiqueta", "Categoría de la Etiqueta:")
            if ok_cat and category:
                self.backend.tag_manager.add_tag(name, category)
                self.refresh_tags()

    def edit_tag(self):
        selected_item = self.tag_list.currentItem()
        if selected_item:
            current_text = selected_item.text()
            name_part = current_text.split(' (')[0]
            category_part = current_text.split(' (')[1].rstrip(')')

            new_name, ok = QInputDialog.getText(self, "Editar Etiqueta", "Nuevo Nombre de la Etiqueta:", text=name_part)
            if ok and new_name:
                new_category, ok_cat = QInputDialog.getText(self, "Editar Etiqueta", "Nueva Categoría de la Etiqueta:", text=category_part)
                if ok_cat and new_category:
                    # Obtener el ID de la etiqueta actual
                    tags = self.backend.tag_manager.get_all_tags()
                    for tag in tags:
                        if tag.name == name_part and tag.category == category_part:
                            self.backend.tag_manager.edit_tag(tag.id, new_name, new_category)
                            break
                    self.refresh_tags()
        else:
            QMessageBox.warning(self, "Editar Etiqueta", "Por favor, selecciona una etiqueta para editar.")

    def delete_tag(self):
        selected_item = self.tag_list.currentItem()
        if selected_item:
            current_text = selected_item.text()
            name_part = current_text.split(' (')[0]
            category_part = current_text.split(' (')[1].rstrip(')')

            confirm = QMessageBox.question(self, "Eliminar Etiqueta", f"¿Estás seguro de eliminar la etiqueta '{name_part}'?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                # Obtener el ID de la etiqueta actual
                tags = self.backend.tag_manager.get_all_tags()
                for tag in tags:
                    if tag.name == name_part and tag.category == category_part:
                        self.backend.tag_manager.delete_tag(tag.id)
                        break
                self.refresh_tags()
        else:
            QMessageBox.warning(self, "Eliminar Etiqueta", "Por favor, selecciona una etiqueta para eliminar.")
