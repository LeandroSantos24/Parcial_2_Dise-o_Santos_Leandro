from datetime import datetime
import pytest
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante
from cursos.entidades.inscripcion import Inscripcion
from cursos.excepciones.dominio import DominioError

def test_curso_flujo_basico():
    c = Curso(id="CUR-1", nombre="Python", docente_id="DOC-1", cupo=2, modalidad="virtual")
    assert c.vacantes == 2
    c.cambiar_estado("inscripciones")
    c.inscribir("E-1")
    c.inscribir("E-2")
    assert c.vacantes == 0
    with pytest.raises(DominioError):
        c.inscribir("E-3")  # sin vacante
    c.cambiar_estado("en_curso")
    with pytest.raises(DominioError):
        c.cambiar_estado("planificacion")  # transición inválida
    c.cambiar_estado("finalizado")
    assert c.estado == "finalizado"

def test_docente_y_estudiante_validaciones():
    Docente(id="D1", nombre="Ada", email="ada@uni.edu")
    with pytest.raises(DominioError):
        Docente(id="D2", nombre="Turing", email="turing#uni")  # email inválido
    Estudiante(id="E1", nombre="Belu", email="belu@uni.edu", legajo="L001")
    with pytest.raises(DominioError):
        Estudiante(id="E2", nombre="Belu", email="sin_arroba", legajo="L002")

def test_inscripcion_confirmar_y_nota():
    i = Inscripcion(id="I1", curso_id="CUR-1", estudiante_id="E-1", fecha=datetime.now())
    assert i.estado == "pendiente"
    i.confirmar()
    i.set_nota_final(9.0)
    assert i.nota_final == 9.0
    with pytest.raises(DominioError):
        i.set_nota_final(11.0)  # fuera de rango
