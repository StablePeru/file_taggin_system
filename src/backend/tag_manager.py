# src/backend/tag_manager.py

from database.db_manager import DBManager
from database.models import Tag

class TagManager:
    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def add_tag(self, name: str, category: str):
        tag_id = self.db.add_tag(name, category)
        return tag_id

    def edit_tag(self, tag_id: int, new_name: str, new_category: str):
        self.db.update_tag(tag_id, new_name, new_category)

    def delete_tag(self, tag_id: int):
        self.db.delete_tag(tag_id)

    def get_all_tags(self):
        return self.db.get_tags()

    def get_tag_by_id(self, tag_id: int):
        return self.db.get_tag_by_id(tag_id)

    def get_tag_by_name_and_category(self, name: str, category: str):
        return self.db.get_tag_by_name_and_category(name, category)

    def organize_tags_by_category(self, category: str):
        return self.db.organize_tags_by_category(category)
