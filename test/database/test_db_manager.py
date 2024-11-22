# tests/database/test_db_manager.py

import os
import pytest
from src.database.db_manager import DBManager
from src.database.models import Tag, FileTag

@pytest.fixture
def db():
    """
    Fixture para crear una instancia de DBManager con una base de datos temporal.
    Se elimina la base de datos después de cada prueba.
    """
    test_db_path = 'test_tags.db'
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    db = DBManager(db_path=test_db_path)
    yield db
    db.close()
    os.remove(test_db_path)

def test_add_and_get_tags(db):
    """
    Prueba la adición y recuperación de múltiples etiquetas para un archivo.
    """
    # Crear etiquetas
    tag1 = Tag(id=None, name="Trabajo", category="Profesional")
    tag2 = Tag(id=None, name="Urgente", category="Prioridad")
    tag3 = Tag(id=None, name="Personal", category="Privado")

    tag1_id = db.add_tag(tag1)
    tag2_id = db.add_tag(tag2)
    tag3_id = db.add_tag(tag3)

    # Asignar múltiples etiquetas a un archivo
    file_path = "/ruta/al/archivo1.txt"
    file_tag1 = FileTag(id=None, file_path=file_path, tag_id=tag1_id)
    file_tag2 = FileTag(id=None, file_path=file_path, tag_id=tag2_id)

    db.add_file_tag(file_tag1)
    db.add_file_tag(file_tag2)

    # Obtener etiquetas del archivo
    file_tags = db.get_file_tags(file_path)
    assert len(file_tags) == 2
    tag_ids = [ft.tag_id for ft in file_tags]
    assert tag1_id in tag_ids
    assert tag2_id in tag_ids
    assert tag3_id not in tag_ids
