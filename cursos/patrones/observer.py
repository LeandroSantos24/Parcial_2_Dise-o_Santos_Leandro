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
