# src/frontend/widgets/tag_selection_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout

class TagSelectionDialog(QDialog):
    def __init__(self, tag_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Etiquetas")
        self.setModal(True)
        self.selected_tags = []

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        for tag in tag_names:
            item = QListWidgetItem(tag)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Aceptar")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_selected_tags(self):
        return [item.text() for item in self.list_widget.selectedItems()]