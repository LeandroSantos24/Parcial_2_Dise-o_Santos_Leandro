import pytest
from cursos.repos.in_memory import RepoCursos, RepoEstudiantes, RepoInscripciones
from cursos.entidades.curso import Curso
from cursos.entidades.estudiante import Estudiante
from cursos.servicios.servicio_inscripciones import ServicioInscripciones
from cursos.servicios.servicio_calificaciones import ServicioCalificaciones
from cursos.patrones.observer import Observable
from cursos.excepciones.dominio import DominioError

def setup_ctx():
    rc, re, ri = RepoCursos(), RepoEstudiantes(), RepoInscripciones()
    rc.add("CUR-1", Curso(id="CUR-1", nombre="Python", docente_id="D1", cupo=1, estado="inscripciones"))
    re.add("E-1", Estudiante(id="E-1", nombre="Belu", email="b@u.edu", legajo="L1"))
    re.add("E-2", Estudiante(id="E-2", nombre="Ana", email="a@u.edu", legajo="L2"))
    obs = Observable()
    return rc, re, ri, obs

def test_inscribir_y_calificar():
    rc, re, ri, obs = setup_ctx()
    svc = ServicioInscripciones(rc, re, ri, obs)
    insc = svc.inscribir("CUR-1", "E-1")
    with pytest.raises(DominioError):
        svc.inscribir("CUR-1", "E-1")  # duplicado
    with pytest.raises(DominioError):
        svc.inscribir("CUR-1", "E-2")  # sin cupo

    insc.confirmar()
    svc2 = ServicioCalificaciones(ri)
    nota = svc2.calcular_y_guardar(insc.id, "final", examen_final=8.0)
    assert nota == 8.0
