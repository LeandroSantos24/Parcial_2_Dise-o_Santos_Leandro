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
