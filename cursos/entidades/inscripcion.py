# cursos/entidades/inscripcion.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional
from cursos.excepciones.dominio import DominioError

EstadoInscripcion = Literal["pendiente", "confirmada", "cancelada"]

@dataclass(slots=True)
class Inscripcion:
    id: str
    curso_id: str
    estudiante_id: str
    fecha: datetime
    estado: EstadoInscripcion = "pendiente"
    nota_final: Optional[float] = None  # 0..10, opcional

    def __post_init__(self) -> None:
        if not self.id:
            raise DominioError("Inscripción: id obligatorio.")
        if not self.curso_id:
            raise DominioError("Inscripción: curso_id obligatorio.")
        if not self.estudiante_id:
            raise DominioError("Inscripción: estudiante_id obligatorio.")
        self.estado = self.estado.lower().strip()
        if self.estado not in {"pendiente", "confirmada", "cancelada"}:
            raise DominioError("Estado de inscripción inválido.")
        if not isinstance(self.fecha, datetime):
            raise DominioError("La fecha debe ser un datetime.")
        if self.nota_final is not None:
            self._validar_nota(self.nota_final)

    # --- Reglas de negocio simples ---
    def confirmar(self) -> None:
        if self.estado == "cancelada":
            raise DominioError("No se puede confirmar una inscripción cancelada.")
        self.estado = "confirmada"

    def cancelar(self) -> None:
        if self.estado == "cancelada":
            return
        self.estado = "cancelada"

    def set_nota_final(self, nota: float) -> None:
        if self.estado != "confirmada":
            raise DominioError("Solo se puede cargar nota a inscripciones confirmadas.")
        self._validar_nota(nota)
        self.nota_final = float(nota)

    # --- Helpers ---
    @staticmethod
    def _validar_nota(n: float) -> None:
        try:
            n = float(n)
        except Exception as _:
            raise DominioError("La nota debe ser numérica.")
        if not (0.0 <= n <= 10.0):
            raise DominioError("La nota debe estar entre 0 y 10.")

    def __repr__(self) -> str:
        nf = "–" if self.nota_final is None else self.nota_final
        return (f"Inscripcion(id={self.id!r}, curso_id={self.curso_id!r}, "
                f"estudiante_id={self.estudiante_id!r}, estado={self.estado!r}, "
                f"nota_final={nf})")
