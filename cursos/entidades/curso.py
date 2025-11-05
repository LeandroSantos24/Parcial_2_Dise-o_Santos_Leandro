# cursos/entidades/curso.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Literal, Optional
from cursos.excepciones.dominio import DominioError

Modalidad = Literal["presencial", "virtual", "mixta"]
Estado = Literal["planificacion", "inscripciones", "en_curso", "finalizado", "cancelado"]

ESTADOS_VALIDOS: set[str] = {"planificacion", "inscripciones", "en_curso", "finalizado", "cancelado"}
MODALIDADES_VALIDAS: set[str] = {"presencial", "virtual", "mixta"}

# Transiciones permitidas de estado (máquina simple)
TRANSICIONES: dict[Estado, set[Estado]] = {
    "planificacion": {"inscripciones", "cancelado"},
    "inscripciones": {"en_curso", "cancelado"},
    "en_curso": {"finalizado", "cancelado"},
    "finalizado": set(),      # estado terminal
    "cancelado": set(),       # estado terminal
}

@dataclass(slots=True)
class Curso:
    id: str
    nombre: str
    docente_id: str
    cupo: int
    modalidad: Modalidad = "presencial"
    estado: Estado = "planificacion"
    alumnos_ids: List[str] = field(default_factory=list)
    horarios: Optional[List[str]] = None  # ej: ["Lu 18-20", "Mi 18-20"]

    # --------- Validaciones básicas ---------
    def __post_init__(self) -> None:
        self.modalidad = self.modalidad.lower().strip()
        self.estado = self.estado.lower().strip()

        if not self.id or not self.nombre:
            raise DominioError("Curso: id y nombre son obligatorios.")

        if self.modalidad not in MODALIDADES_VALIDAS:
            raise DominioError(f"Modalidad inválida: {self.modalidad}. "
                               f"Debe ser una de {sorted(MODALIDADES_VALIDAS)}.")

        if self.estado not in ESTADOS_VALIDOS:
            raise DominioError(f"Estado inválido: {self.estado}. "
                               f"Debe ser uno de {sorted(ESTADOS_VALIDOS)}.")

        if self.cupo < 0:
            raise DominioError("El cupo no puede ser negativo.")

        # Normalizar alumnos únicos
        self.alumnos_ids = list(dict.fromkeys(self.alumnos_ids))  # quita duplicados preservando orden
        if len(self.alumnos_ids) > self.cupo:
            raise DominioError("Hay más alumnos inscriptos que el cupo disponible.")

    # --------- Propiedades útiles ---------
    @property
    def vacantes(self) -> int:
        return max(0, self.cupo - len(self.alumnos_ids))

    def tiene_cupo(self) -> bool:
        return self.vacantes > 0

    # --------- Reglas de negocio ---------
    def cambiar_estado(self, nuevo: Estado) -> None:
        nuevo = nuevo.lower().strip()
        if nuevo not in ESTADOS_VALIDOS:
            raise DominioError(f"Estado inválido: {nuevo}")

        permitidos = TRANSICIONES.get(self.estado, set())
        if nuevo not in permitidos:
            raise DominioError(f"Transición no permitida: {self.estado} → {nuevo}")

        # Reglas extra
        if nuevo == "en_curso" and len(self.alumnos_ids) == 0:
            raise DominioError("No se puede iniciar un curso sin alumnos inscriptos.")
        if nuevo == "finalizado" and self.estado != "en_curso":
            raise DominioError("Solo se puede finalizar un curso que está 'en_curso'.")

        self.estado = nuevo

    def set_cupo(self, nuevo_cupo: int) -> None:
        if nuevo_cupo < len(self.alumnos_ids):
            raise DominioError(
                f"No se puede reducir el cupo ({nuevo_cupo}) por debajo de inscriptos actuales ({len(self.alumnos_ids)})."
            )
        if nuevo_cupo < 0:
            raise DominioError("El cupo no puede ser negativo.")
        self.cupo = nuevo_cupo

    def inscribir(self, estudiante_id: str) -> None:
        if self.estado != "inscripciones":
            raise DominioError("Las inscripciones no están habilitadas en el estado actual.")
        if estudiante_id in self.alumnos_ids:
            raise DominioError("El estudiante ya está inscripto en este curso.")
        if not self.tiene_cupo():
            raise DominioError("No hay vacantes disponibles.")
        self.alumnos_ids.append(estudiante_id)

    def desinscribir(self, estudiante_id: str) -> None:
        if self.estado not in {"inscripciones", "en_curso"}:
            raise DominioError("No se puede desinscribir en el estado actual.")
        try:
            self.alumnos_ids.remove(estudiante_id)
        except ValueError:
            raise DominioError("El estudiante no figura como inscripto.")

    # --------- Representación ---------
    def __repr__(self) -> str:
        return (
            f"Curso(id={self.id!r}, nombre={self.nombre!r}, docente_id={self.docente_id!r}, "
            f"cupo={self.cupo}, modalidad={self.modalidad!r}, estado={self.estado!r}, "
            f"inscriptos={len(self.alumnos_ids)}, vacantes={self.vacantes})"
        )
