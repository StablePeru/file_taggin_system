# src/frontend/widgets/search_panel.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox, QListWidgetItem, QHBoxLayout, QComboBox, QDateEdit, QSpinBox
)
from PyQt5.QtCore import QDate
from .file_details import FileDetails

import datetime

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
        self.file_type_combo.addItems([".txt", ".pdf", ".jpg", ".png", ".docx", ".xlsx", ".py", ".md", ".mp4", ".avi", ".mkv"])  # Ampliar la lista
        filters_layout.addWidget(QLabel("Tipo de Archivo:"))
        filters_layout.addWidget(self.file_type_combo)

        # Tamaño máximo y unidad
        self.size_spin = QSpinBox()
        self.size_spin.setRange(0, 1000000)  # Ajustar el rango según sea necesario
        self.size_spin.setValue(0)
        self.size_spin.setSuffix(" ")

        self.size_unit_combo = QComboBox()
        self.size_unit_combo.addItems(["Bytes", "KB", "MB", "GB"])
        filters_layout.addWidget(QLabel("Tamaño Máximo:"))
        filters_layout.addWidget(self.size_spin)
        filters_layout.addWidget(self.size_unit_combo)

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
        size_value = self.size_spin.value()
        size_unit = self.size_unit_combo.currentText()
        date_qdate = self.date_edit.date()

        # Convertir tamaño a bytes según la unidad seleccionada
        if size_unit == "Bytes":
            size = size_value
        elif size_unit == "KB":
            size = size_value * 1024
        elif size_unit == "MB":
            size = size_value * 1024 * 1024
        elif size_unit == "GB":
            size = size_value * 1024 * 1024 * 1024
        else:
            size = None

        # Convertir fecha a timestamp
        date_datetime = datetime.datetime.combine(date_qdate.toPyDate(), datetime.time.min)
        date_timestamp = date_datetime.timestamp()

        if file_type == "Todos los Tipos":
            file_type = None
        if size_value == 0:
            size = None

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
