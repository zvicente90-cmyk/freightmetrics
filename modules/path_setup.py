"""
Helper para configurar imports y paths de manera centralizada.
Evita repetir sys.path.insert() en cada archivo.
"""

import sys
from pathlib import Path


def setup_paths():
    """
    Configura los paths necesarios para importar módulos de la aplicación.
    Debe ser llamado una sola vez al inicio de app.py o en cada módulo.
    """
    # Agregar directorio padre del módulo actual al sys.path
    current_dir = Path(__file__).parent.parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    return current_dir


def get_app_root():
    """Retorna la ruta raíz de la aplicación"""
    return Path(__file__).parent.parent
