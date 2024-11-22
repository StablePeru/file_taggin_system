# test_db.py

from src.database.db_manager import DBManager
from src.database.models import Tag, FileTag

def test_db():
    db = DBManager()

    # Añadir una etiqueta
    tag = Tag(id=None, name="Trabajo", category="Profesional")
    tag_id = db.add_tag(tag)
    print(f"Tag añadido con ID: {tag_id}")

    # Obtener todas las etiquetas
    tags = db.get_tags()
    for t in tags:
        print(f"ID: {t.id}, Nombre: {t.name}, Categoría: {t.category}")

    # Actualizar la etiqueta
    db.update_tag(tag_id, "Trabajo Actualizado", "Profesional")

    # Obtener la etiqueta actualizada
    updated_tags = db.get_tags()
    for t in updated_tags:
        print(f"ID: {t.id}, Nombre: {t.name}, Categoría: {t.category}")

    # Eliminar la etiqueta
    db.delete_tag(tag_id)
    print("Tag eliminado.")

    # Cerrar la conexión
    db.close()

if __name__ == "__main__":
    test_db()
