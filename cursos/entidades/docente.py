# cursos/entidades/docente.py
from __future__ import annotations
from dataclasses import dataclass
from cursos.excepciones.dominio import DominioError

@dataclass(slots=True)
class Docente:
    id: str
    nombre: str
    email: str
    especialidad: str | None = None
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.id or not self.nombre:
            raise DominioError("Docente: id y nombre son obligatorios.")
        if "@" not in self.email:
            raise DominioError("Docente: email inválido.")

    def deshabilitar(self) -> None:
        self.activo = False

    def habilitar(self) -> None:
        self.activo = True

    def __repr__(self) -> str:
        return (
            f"Docente(id={self.id!r}, nombre={self.nombre!r}, "
            f"email={self.email!r}, activo={self.activo})"
        )
