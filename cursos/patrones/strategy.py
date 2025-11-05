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
