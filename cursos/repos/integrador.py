"""
Archivo integrador generado automaticamente
Directorio: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos
Fecha: 2025-11-04 23:52:03
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\__init__.py
# ================================================================================

# repos del dominio Cursos


# ================================================================================
# ARCHIVO 2/3: base.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\base.py
# ================================================================================

# cursos/repos/base.py
from __future__ import annotations
from typing import Dict, Generic, Iterable, List, Optional, TypeVar, Callable

T = TypeVar("T")


class Repo(Generic[T]):
    """
    Repositorio genérico in-memory.
    - Guarda objetos por id (string).
    - Ofrece CRUD básico y utilidades de consulta.
    """

    def __init__(self) -> None:
        self._data: Dict[str, T] = {}

    # --- CRUD ---
    def add(self, id_: str, obj: T, *, overwrite: bool = False) -> None:
        if not overwrite and id_ in self._data:
            raise KeyError(f"Ya existe un objeto con id '{id_}'.")
        self._data[id_] = obj

    def get(self, id_: str) -> Optional[T]:
        return self._data.get(id_)

    def update(self, id_: str, obj: T) -> None:
        if id_ not in self._data:
            raise KeyError(f"No existe id '{id_}' para actualizar.")
        self._data[id_] = obj

    def remove(self, id_: str) -> bool:
        return self._data.pop(id_, None) is not None

    # --- Utilidades ---
    def exists(self, id_: str) -> bool:
        return id_ in self._data

    def count(self) -> int:
        return len(self._data)

    def all(self) -> List[T]:
        return list(self._data.values())

    def keys(self) -> List[str]:
        return list(self._data.keys())

    def clear(self) -> None:
        self._data.clear()

    def find(self, predicado: Callable[[T], bool]) -> List[T]:
        """Filtra por función booleana."""
        return [obj for obj in self._data.values() if predicado(obj)]

    # Iteración (por si querés usar for-in)
    def __iter__(self):
        return iter(self._data.values())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={len(self._data)})"


# ================================================================================
# ARCHIVO 3/3: in_memory.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\in_memory.py
# ================================================================================

# cursos/repos/in_memory.py
from __future__ import annotations
from typing import List
from .base import Repo
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante
from cursos.entidades.inscripcion import Inscripcion


class RepoCursos(Repo[Curso]):
    def buscar_por_docente(self, docente_id: str) -> List[Curso]:
        return self.find(lambda c: c.docente_id == docente_id)

    def abiertos_a_inscripcion(self) -> List[Curso]:
        return self.find(lambda c: c.estado == "inscripciones")


class RepoDocentes(Repo[Docente]):
    def activos(self) -> List[Docente]:
        return self.find(lambda d: d.activo)


class RepoEstudiantes(Repo[Estudiante]):
    def activos(self) -> List[Estudiante]:
        return self.find(lambda e: e.activo)


class RepoInscripciones(Repo[Inscripcion]):
    def por_curso(self, curso_id: str) -> List[Inscripcion]:
        return self.find(lambda i: i.curso_id == curso_id)

    def por_estudiante(self, estudiante_id: str) -> List[Inscripcion]:
        return self.find(lambda i: i.estudiante_id == estudiante_id)

    def confirmadas(self) -> List[Inscripcion]:
        return self.find(lambda i: i.estado == "confirmada")


