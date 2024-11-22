# src/frontend/widgets/search_panel.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox, QListWidgetItem, QHBoxLayout, QComboBox, QDateEdit, QSpinBox
)
from PyQt5.QtCore import QDate
from .file_details import FileDetails

class SearchPanel(QWidget):
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QPushButton("Panel de Búsqueda")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setEnabled(False)
        layout.addWidget(title)

        # Campo de búsqueda de etiquetas
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por etiquetas separadas por '+' (ej. Trabajo+Urgente)")
        layout.addWidget(self.search_input)

        # Filtros avanzados
        filters_layout = QHBoxLayout()

        # Tipo de archivo
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItem("Todos los Tipos")
        self.file_type_combo.addItems([".txt", ".pdf", ".jpg", ".png", ".docx", ".xlsx", ".py", ".md"])  # Puedes ampliar esta lista
        filters_layout.addWidget(QLabel("Tipo de Archivo:"))
        filters_layout.addWidget(self.file_type_combo)

        # Tamaño máximo en KB
        self.size_spin = QSpinBox()
        self.size_spin.setRange(0, 100000)  # 0 para sin límite
        self.size_spin.setSuffix(" KB")
        filters_layout.addWidget(QLabel("Tamaño Máximo:"))
        filters_layout.addWidget(self.size_spin)

        # Fecha de modificación
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        filters_layout.addWidget(QLabel("Modificado Después de:"))
        filters_layout.addWidget(self.date_edit)

        layout.addLayout(filters_layout)

        # Botón de búsqueda
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.perform_search)
        layout.addWidget(search_button)

        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.show_file_details)
        layout.addWidget(self.results_list)

        # Widget de detalles del archivo
        self.file_details_widget = FileDetails("", self.backend)
        self.file_details_widget.hide()  # Inicialmente oculto
        layout.addWidget(self.file_details_widget)

        self.setLayout(layout)

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Buscar", "Por favor, ingresa al menos una etiqueta para buscar.")
            return

        tags = [tag.strip() for tag in query.split('+') if tag.strip()]
        if not tags:
            QMessageBox.warning(self, "Buscar", "La búsqueda debe contener al menos una etiqueta válida.")
            return

        # Obtener los archivos que coinciden con las etiquetas
        files = self.backend.search_engine.search_by_tags(tags)
        if not files:
            QMessageBox.information(self, "Buscar", "No se encontraron archivos con las etiquetas especificadas.")
            self.results_list.clear()
            self.file_details_widget.hide()
            return

        # Aplicar filtros avanzados
        file_type = self.file_type_combo.currentText()
        size_kb = self.size_spin.value()
        date_qdate = self.date_edit.date()
        date_modified = date_qdate.toPyDate().toordinal()  # Convertir a timestamp

        if date_modified:
            # Convertir fecha a timestamp
            import datetime
            date_datetime = datetime.datetime.combine(date_qdate.toPyDate(), datetime.time.min)
            date_timestamp = date_datetime.timestamp()
        else:
            date_timestamp = None

        if file_type == "Todos los Tipos":
            file_type = None
        if size_kb == 0:
            size = None
        else:
            size = size_kb * 1024  # Convertir a bytes

        filtered_files = self.backend.search_engine.advanced_filters(
            files,
            date_modified=date_timestamp,
            file_type=file_type,
            size=size
        )

        if not filtered_files:
            QMessageBox.information(self, "Buscar", "No se encontraron archivos que coincidan con los filtros especificados.")
            self.results_list.clear()
            self.file_details_widget.hide()
            return

        self.results_list.clear()
        for file in filtered_files:
            self.results_list.addItem(file)
        self.file_details_widget.hide()

    def show_file_details(self, item):
        file_path = item.text()
        self.file_details_widget.setParent(None)
        self.file_details_widget = FileDetails(file_path, self.backend)
        self.layout().addWidget(self.file_details_widget)
        self.file_details_widget.show()
