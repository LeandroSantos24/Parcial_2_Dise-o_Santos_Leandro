"""
Archivo integrador generado automaticamente
Directorio: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones
Fecha: 2025-11-04 23:52:03
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\__init__.py
# ================================================================================

# patrones del dominio Cursos


# ================================================================================
# ARCHIVO 2/4: factory.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\factory.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/4: observer.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\observer.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/4: strategy.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\patrones\strategy.py
# ================================================================================

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


