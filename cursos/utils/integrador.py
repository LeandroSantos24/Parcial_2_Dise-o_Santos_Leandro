"""
Archivo integrador generado automaticamente
Directorio: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils
Fecha: 2025-11-04 23:52:03
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\__init__.py
# ================================================================================

# utils del dominio Cursos


# ================================================================================
# ARCHIVO 2/3: config.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\config.py
# ================================================================================

class Config:
    """Singleton de configuración (completar)."""
    _instance = None
    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# ================================================================================
# ARCHIVO 3/3: logging_conf.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\logging_conf.py
# ================================================================================

def setup_logging(level: str = "INFO"):
    """Config de logging (completar)."""
    pass


