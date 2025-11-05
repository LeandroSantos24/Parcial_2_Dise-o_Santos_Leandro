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
