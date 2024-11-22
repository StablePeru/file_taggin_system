# Sistema Personalizado de Etiquetado de Archivos

## Descripción

Una herramienta para etiquetar y organizar archivos más allá de las limitaciones de las estructuras tradicionales de carpetas. Este sistema permite agregar metadatos personalizados (etiquetas) a los archivos, haciéndolos buscables y clasificables según criterios definidos por el usuario, sin importar dónde estén almacenados.

## Características Principales

- **Gestión de Etiquetas:**
  - Asigna múltiples etiquetas a cualquier archivo.
  - Edita o elimina etiquetas fácilmente.
  - Organiza etiquetas en categorías.

- **Funcionalidad de Búsqueda:**
  - Encuentra archivos usando etiquetas o combinaciones de etiquetas.
  - Filtros avanzados como fecha de modificación, tipo de archivo o tamaño.
  - Muestra resultados de búsqueda con vistas previas.

- **Interfaz de Usuario:**
  - Interfaz sencilla de arrastrar y soltar para etiquetar archivos.
  - Nube de etiquetas o vista en árbol para una navegación fácil.
  - Modo oscuro opcional y configuraciones personalizables.

## Tecnologías

- **Frontend:** PyQt5
- **Backend:** Python
- **Base de Datos:** SQLite
- **Control de Versiones:** GitHub

## Instalación

1. **Clonar el Repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/file_tagging_system.git
   cd file_tagging_system
   ```

2. **Crear y Activar un Entorno Virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar las Dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Ejecutar la Aplicación:**

   ```bash
   python src/main.py
   ```

2. **Agregar Etiquetas:**
   
   Ve al módulo de gestión de etiquetas para crear nuevas etiquetas.

3. **Etiquetar Archivos:**

   Usa el botón "Agregar Archivos" para seleccionar y etiquetar archivos.

4. **Buscar Archivos:**

   Utiliza el panel de búsqueda para encontrar archivos etiquetados.

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
pytest
```

## Contribuciones

¡Contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request para cualquier mejora o corrección.

## Licencia

MIT

## Crear un Archivo de Licencia (Opcional)

Si deseas, puedes agregar una licencia. Por ejemplo, para la licencia MIT:

Crea un archivo `LICENSE` en la raíz del proyecto con el contenido de la [Licencia MIT](https://opensource.org/licenses/MIT).

## Agregar y Hacer Commit de la Documentación

```bash
git add README.md LICENSE
git commit -m "Add initial README and license"
git push
´´´
