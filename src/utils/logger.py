# src/utils/logger.py

import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Configura y retorna un logger."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

# Configurar un logger global para la aplicación
app_logger = setup_logger('app_logger', os.path.join(os.path.dirname(__file__), '..', 'logs', 'app.log'))
