# cursos/entidades/estudiante.py
from __future__ import annotations
from dataclasses import dataclass
from cursos.excepciones.dominio import DominioError


@dataclass(slots=True)
class Estudiante:
    id: str
    nombre: str
    email: str
    legajo: str
    activo: bool = True

    def __post_init__(self) -> None:
        if not self.id or not self.nombre:
            raise DominioError("Estudiante: id y nombre son obligatorios.")
        if "@" not in self.email:
            raise DominioError("Estudiante: email inválido.")
        if not self.legajo:
            raise DominioError("Estudiante: legajo obligatorio.")

    def deshabilitar(self) -> None:
        self.activo = False

    def habilitar(self) -> None:
        self.activo = True

    def __repr__(self) -> str:
        return f"Estudiante(id={self.id!r}, nombre={self.nombre!r}, legajo={self.legajo!r}, activo={self.activo})"
