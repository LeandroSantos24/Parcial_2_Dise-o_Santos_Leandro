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
