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
