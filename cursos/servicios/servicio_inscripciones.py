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
