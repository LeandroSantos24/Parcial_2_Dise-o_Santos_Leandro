from cursos.repos.in_memory import RepoCursos, RepoDocentes, RepoEstudiantes, RepoInscripciones
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante
from cursos.entidades.inscripcion import Inscripcion
from datetime import datetime

def test_repo_crud_y_filtros():
    rc = RepoCursos()
    rd = RepoDocentes()
    re = RepoEstudiantes()
    ri = RepoInscripciones()

    rc.add("C1", Curso(id="C1", nombre="Redes", docente_id="D1", cupo=20))
    rc.add("C2", Curso(id="C2", nombre="Python", docente_id="D1", cupo=20, estado="inscripciones"))
    rd.add("D1", Docente(id="D1", nombre="Ada", email="ada@uni.edu"))
    re.add("E1", Estudiante(id="E1", nombre="Belu", email="belu@uni.edu", legajo="L1"))
    ri.add("I1", Inscripcion(id="I1", curso_id="C2", estudiante_id="E1", fecha=datetime.now()))

    assert rc.count() == 2
    assert [c.id for c in rc.buscar_por_docente("D1")] == ["C1","C2"]
    assert [c.id for c in rc.abiertos_a_inscripcion()] == ["C2"]
    assert rd.activos()[0].id == "D1"
    assert re.activos()[0].id == "E1"
    assert ri.por_curso("C2")[0].id == "I1"
