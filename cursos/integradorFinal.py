"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos
Fecha de generacion: 2025-11-04 23:52:03
Total de archivos integrados: 22
Total de directorios procesados: 7
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. __init__.py
#   2. main.py
#
# DIRECTORIO: entidades
#   3. __init__.py
#   4. curso.py
#   5. docente.py
#   6. estudiante.py
#   7. inscripcion.py
#
# DIRECTORIO: excepciones
#   8. __init__.py
#   9. dominio.py
#
# DIRECTORIO: patrones
#   10. __init__.py
#   11. factory.py
#   12. observer.py
#   13. strategy.py
#
# DIRECTORIO: repos
#   14. __init__.py
#   15. base.py
#   16. in_memory.py
#
# DIRECTORIO: servicios
#   17. __init__.py
#   18. servicio_calificaciones.py
#   19. servicio_inscripciones.py
#
# DIRECTORIO: utils
#   20. __init__.py
#   21. config.py
#   22. logging_conf.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/22: __init__.py
# Directorio: .
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\__init__.py
# ==============================================================================

# Paquete principal del dominio Cursos
__all__ = ["entidades", "servicios", "patrones", "excepciones", "repos", "utils"]


# ==============================================================================
# ARCHIVO 2/22: main.py
# Directorio: .
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\main.py
# ==============================================================================

# cursos/main.py
from __future__ import annotations
from datetime import datetime

# Repos
from cursos.repos.in_memory import (
    RepoCursos, RepoDocentes, RepoEstudiantes, RepoInscripciones
)

# Entidades
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante

# Servicios
from cursos.servicios.servicio_inscripciones import ServicioInscripciones
from cursos.servicios.servicio_calificaciones import ServicioCalificaciones

# Patrones
from cursos.patrones.observer import Observable, EmailNotifier, LoggerNotifier


def run_demo() -> None:
    print("== DEMO ProyectoCursos ==")

    # ----- Infra básica -----
    repo_cursos = RepoCursos()
    repo_docentes = RepoDocentes()
    repo_estudiantes = RepoEstudiantes()
    repo_insc = RepoInscripciones()

    eventos = Observable()
    eventos.suscribir(EmailNotifier())
    eventos.suscribir(LoggerNotifier())

    svc_insc = ServicioInscripciones(repo_cursos, repo_estudiantes, repo_insc, eventos)
    svc_notas = ServicioCalificaciones(repo_insc)

    # ----- Datos seed -----
    d1 = Docente(id="DOC-1", nombre="Ada Lovelace", email="ada@uni.edu", especialidad="Programación")
    repo_docentes.add(d1.id, d1)

    e1 = Estudiante(id="E-1", nombre="Belu", email="belu@uni.edu", legajo="L001")
    e2 = Estudiante(id="E-2", nombre="Chiquibu", email="chiquibu@uni.edu", legajo="L002")
    repo_estudiantes.add(e1.id, e1)
    repo_estudiantes.add(e2.id, e2)

    curso = Curso(
        id="CUR-1",
        nombre="Python Inicial",
        docente_id=d1.id,
        cupo=2,
        modalidad="virtual",
        estado="inscripciones"
    )
    repo_cursos.add(curso.id, curso)

    print("Curso creado:", curso)

    # ----- Inscripciones -----
    insc1 = svc_insc.inscribir("CUR-1", "E-1")
    insc2 = svc_insc.inscribir("CUR-1", "E-2")
    print("Insc. 1:", insc1)
    print("Insc. 2:", insc2)
    print("Vacantes curso:", curso.vacantes)

    # Pasar a EN CURSO
    curso.cambiar_estado("en_curso")
    print("Estado curso ->", curso.estado)

    # Confirmar y calificar
    insc1.confirmar()
    insc2.confirmar()
    nota1 = svc_notas.calcular_y_guardar(insc1.id, "ponderado", parciales=[8, 9], tp=[10])
    nota2 = svc_notas.calcular_y_guardar(insc2.id, "final", examen_final=7.5)
    print(f"Notas finales -> {insc1.estudiante_id}: {nota1} | {insc2.estudiante_id}: {nota2}")

    # Finalizar curso
    curso.cambiar_estado("finalizado")
    print("Estado curso ->", curso.estado)

    print("== FIN DEMO ==")


if __name__ == "__main__":
    run_demo()



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 3/22: __init__.py
# Directorio: entidades
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\__init__.py
# ==============================================================================

# entidades del dominio Cursos


# ==============================================================================
# ARCHIVO 4/22: curso.py
# Directorio: entidades
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\curso.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 5/22: docente.py
# Directorio: entidades
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\docente.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 6/22: estudiante.py
# Directorio: entidades
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\estudiante.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 7/22: inscripcion.py
# Directorio: entidades
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\entidades\inscripcion.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 8/22: __init__.py
# Directorio: excepciones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\excepciones\__init__.py
# ==============================================================================

# excepciones del dominio Cursos


# ==============================================================================
# ARCHIVO 9/22: dominio.py
# Directorio: excepciones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\excepciones\dominio.py
# ==============================================================================

class DominioError(Exception):
    """Excepción base de dominio."""
    pass



################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 10/22: __init__.py
# Directorio: patrones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\__init__.py
# ==============================================================================

# patrones del dominio Cursos


# ==============================================================================
# ARCHIVO 11/22: factory.py
# Directorio: patrones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\factory.py
# ==============================================================================

# cursos/patrones/factory.py
from __future__ import annotations
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante
from cursos.entidades.inscripcion import Inscripcion
from datetime import datetime

def crear_entidad(tipo: str, **kwargs):
    t = tipo.lower().strip()
    if t == "curso":
        return Curso(**kwargs)
    if t == "docente":
        return Docente(**kwargs)
    if t == "estudiante":
        return Estudiante(**kwargs)
    if t == "inscripcion":
        # default de fecha si no viene
        kwargs.setdefault("fecha", datetime.now())
        return Inscripcion(**kwargs)
    raise ValueError(f"Tipo no soportado: {tipo}")


# ==============================================================================
# ARCHIVO 12/22: observer.py
# Directorio: patrones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\observer.py
# ==============================================================================

# cursos/patrones/observer.py
from __future__ import annotations
from typing import Protocol, Any, Dict, List

class Observador(Protocol):
    def actualizar(self, evento: str, payload: Dict[str, Any]) -> None: ...

class Observable:
    def __init__(self) -> None:
        self._subs: List[Observador] = []

    def suscribir(self, obs: Observador) -> None:
        self._subs.append(obs)

    def desuscribir(self, obs: Observador) -> None:
        try:
            self._subs.remove(obs)
        except ValueError:
            pass

    def notificar(self, evento: str, payload: Dict[str, Any]) -> None:
        for obs in list(self._subs):
            obs.actualizar(evento, payload)

# Observadores de ejemplo
class EmailNotifier:
    def actualizar(self, evento: str, payload: Dict[str, Any]) -> None:
        # Simulación: reemplazable por envío real
        print(f"[EMAIL] {evento} → {payload}")

class LoggerNotifier:
    def actualizar(self, evento: str, payload: Dict[str, Any]) -> None:
        print(f"[LOG] {evento} :: {payload}")


# ==============================================================================
# ARCHIVO 13/22: strategy.py
# Directorio: patrones
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\strategy.py
# ==============================================================================

# cursos/patrones/strategy.py
from __future__ import annotations
from abc import ABC, abstractmethod

class EstrategiaCalculo(ABC):
    @abstractmethod
    def calcular(self, *, parciales: list[float] | None = None,
                 tp: list[float] | None = None,
                 examen_final: float | None = None) -> float: ...

    @staticmethod
    def _promedio(nums: list[float] | None) -> float:
        nums = nums or []
        if not nums:
            return 0.0
        return sum(nums) / len(nums)

    @staticmethod
    def _clip(n: float) -> float:
        return max(0.0, min(10.0, n))


class CalculoSimple(EstrategiaCalculo):
    def calcular(self, *, parciales=None, tp=None, examen_final=None) -> float:
        # promedio de todo lo que venga
        datos = []
        if parciales: datos += parciales
        if tp: datos += tp
        if examen_final is not None: datos.append(examen_final)
        if not datos:
            return 0.0
        return self._clip(sum(datos) / len(datos))


class CalculoPonderado(EstrategiaCalculo):
    def calcular(self, *, parciales=None, tp=None, examen_final=None) -> float:
        p = self._promedio(parciales)
        t = self._promedio(tp)
        nota = p * 0.7 + t * 0.3
        return self._clip(nota)


class CalculoFinal(EstrategiaCalculo):
    def calcular(self, *, parciales=None, tp=None, examen_final=None) -> float:
        return self._clip(float(examen_final or 0.0))


def obtener_estrategia(nombre: str) -> EstrategiaCalculo:
    nombre = (nombre or "").lower().strip()
    if nombre in {"simple", "promedio"}:
        return CalculoSimple()
    if nombre in {"ponderado", "70-30"}:
        return CalculoPonderado()
    if nombre in {"final", "examen_final"}:
        return CalculoFinal()
    # default razonable
    return CalculoPonderado()



################################################################################
# DIRECTORIO: repos
################################################################################

# ==============================================================================
# ARCHIVO 14/22: __init__.py
# Directorio: repos
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\__init__.py
# ==============================================================================

# repos del dominio Cursos


# ==============================================================================
# ARCHIVO 15/22: base.py
# Directorio: repos
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\base.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 16/22: in_memory.py
# Directorio: repos
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\repos\in_memory.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 17/22: __init__.py
# Directorio: servicios
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\servicios\__init__.py
# ==============================================================================

# servicios del dominio Cursos


# ==============================================================================
# ARCHIVO 18/22: servicio_calificaciones.py
# Directorio: servicios
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\servicios\servicio_calificaciones.py
# ==============================================================================

# cursos/servicios/servicio_calificaciones.py
from __future__ import annotations
from cursos.repos.in_memory import RepoInscripciones
from cursos.patrones.strategy import obtener_estrategia
from cursos.excepciones.dominio import DominioError


class ServicioCalificaciones:
    """
    Usa Strategy para calcular notas finales según esquema elegido.
    """

    def __init__(self, repo_inscripciones: RepoInscripciones):
        self.repo_inscripciones = repo_inscripciones

    def calcular_y_guardar(
        self,
        inscripcion_id: str,
        esquema: str,
        *,
        parciales: list[float] | None = None,
        tp: list[float] | None = None,
        examen_final: float | None = None,
    ) -> float:
        insc = self.repo_inscripciones.get(inscripcion_id)
        if not insc:
            raise DominioError("Inscripción inexistente.")

        if insc.estado != "confirmada":
            raise DominioError("Solo se puede calificar inscripciones confirmadas.")

        estrategia = obtener_estrategia(esquema)
        nota = estrategia.calcular(parciales=parciales, tp=tp, examen_final=examen_final)
        insc.set_nota_final(nota)
        return nota


# ==============================================================================
# ARCHIVO 19/22: servicio_inscripciones.py
# Directorio: servicios
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\servicios\servicio_inscripciones.py
# ==============================================================================

# cursos/servicios/servicio_inscripciones.py
from __future__ import annotations
from datetime import datetime
from cursos.repos.in_memory import RepoCursos, RepoEstudiantes, RepoInscripciones
from cursos.entidades.inscripcion import Inscripcion
from cursos.excepciones.dominio import DominioError
from cursos.patrones.observer import Observable


class ServicioInscripciones:
    """
    Orquesta el proceso de inscripción:
      - valida existencia de curso y estudiante
      - evita duplicados
      - controla cupo y estado del curso
      - notifica a observadores (ej. email/log)
    """

    def __init__(
        self,
        repo_cursos: RepoCursos,
        repo_estudiantes: RepoEstudiantes,
        repo_inscripciones: RepoInscripciones,
        eventos: Observable | None = None,
    ):
        self.repo_cursos = repo_cursos
        self.repo_estudiantes = repo_estudiantes
        self.repo_inscripciones = repo_inscripciones
        self.eventos = eventos

    # --- Crear inscripción ---
    def inscribir(self, curso_id: str, estudiante_id: str) -> Inscripcion:
        curso = self.repo_cursos.get(curso_id)
        est = self.repo_estudiantes.get(estudiante_id)
        if curso is None:
            raise DominioError("Curso inexistente.")
        if est is None:
            raise DominioError("Estudiante inexistente.")

        # Reglas de curso
        if curso.estado != "inscripciones":
            raise DominioError("El curso no está abierto a inscripciones.")
        if not curso.tiene_cupo():
            raise DominioError("El curso no tiene vacantes disponibles.")

        # Evitar duplicado
        duplicadas = self.repo_inscripciones.find(
            lambda i: i.curso_id == curso_id and i.estudiante_id == estudiante_id
        )
        if duplicadas:
            raise DominioError("El estudiante ya está inscripto en este curso.")

        # Crear inscripción
        insc = Inscripcion(
            id=f"I-{len(self.repo_inscripciones._data)+1}",
            curso_id=curso_id,
            estudiante_id=estudiante_id,
            fecha=datetime.now(),
        )
        self.repo_inscripciones.add(insc.id, insc)
        curso.alumnos_ids.append(estudiante_id)

        # Notificar
        if self.eventos:
            self.eventos.notificar(
                "INSCRIPCION_NUEVA",
                {"curso_id": curso_id, "estudiante_id": estudiante_id, "fecha": insc.fecha.isoformat()},
            )

        return insc

    # --- Cancelar inscripción ---
    def cancelar(self, inscripcion_id: str) -> None:
        insc = self.repo_inscripciones.get(inscripcion_id)
        if not insc:
            raise DominioError("Inscripción inexistente.")
        insc.cancelar()
        if self.eventos:
            self.eventos.notificar("INSCRIPCION_CANCELADA", {"id": inscripcion_id})



################################################################################
# DIRECTORIO: utils
################################################################################

# ==============================================================================
# ARCHIVO 20/22: __init__.py
# Directorio: utils
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\__init__.py
# ==============================================================================

# utils del dominio Cursos


# ==============================================================================
# ARCHIVO 21/22: config.py
# Directorio: utils
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\config.py
# ==============================================================================

class Config:
    """Singleton de configuración (completar)."""
    _instance = None
    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# ==============================================================================
# ARCHIVO 22/22: logging_conf.py
# Directorio: utils
# Ruta completa: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\utils\logging_conf.py
# ==============================================================================

def setup_logging(level: str = "INFO"):
    """Config de logging (completar)."""
    pass



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 22
# Generado: 2025-11-04 23:52:03
################################################################################
