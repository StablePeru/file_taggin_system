# src/backend/tag_manager.py

from database.db_manager import DBManager

class TagManager:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def add_tag(self, file_path: str, tag: str, category: str):
        # Lógica para añadir una etiqueta a un archivo
        pass

    def edit_tag(self, tag_id: int, new_tag: str):
        # Lógica para editar una etiqueta existente
        pass

    def delete_tag(self, tag_id: int):
        # Lógica para eliminar una etiqueta
        pass

    def get_tags(self, file_path: str):
        # Obtener todas las etiquetas asociadas a un archivo
        pass

    def organize_tags_by_category(self, category: str):
        # Organizar etiquetas en una categoría específica
        pass
