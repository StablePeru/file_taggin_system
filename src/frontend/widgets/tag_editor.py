# src/frontend/widgets/tag_editor.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget

class TagEditor(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tag_list = QListWidget()
        self.refresh_tags()

        add_button = QPushButton("Agregar Etiqueta")
        add_button.clicked.connect(self.add_tag)

        edit_button = QPushButton("Editar Etiqueta")
        edit_button.clicked.connect(self.edit_tag)

        delete_button = QPushButton("Eliminar Etiqueta")
        delete_button.clicked.connect(self.delete_tag)

        layout.addWidget(self.tag_list)
        layout.addWidget(add_button)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def refresh_tags(self):
        self.tag_list.clear()
        tags = self.backend.tag_manager.get_tags()
        for tag in tags:
            self.tag_list.addItem(f"{tag.name} ({tag.category})")

    def add_tag(self):
        # Implementar lógica para agregar una etiqueta
        pass

    def edit_tag(self):
        # Implementar lógica para editar una etiqueta seleccionada
        pass

    def delete_tag(self):
        # Implementar lógica para eliminar una etiqueta seleccionada
        pass
