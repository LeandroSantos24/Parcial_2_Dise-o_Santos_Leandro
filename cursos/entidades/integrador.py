"""
Archivo integrador generado automaticamente
Directorio: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades
Fecha: 2025-11-04 23:52:03
Total de archivos integrados: 5
"""

# ================================================================================
# ARCHIVO 1/5: __init__.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\__init__.py
# ================================================================================

# entidades del dominio Cursos


# ================================================================================
# ARCHIVO 2/5: curso.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\curso.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/5: docente.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\docente.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/5: estudiante.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\estudiante.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/5: inscripcion.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\inscripcion.py
# ================================================================================

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


