"""
Archivo integrador generado automaticamente
Directorio: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos
Fecha: 2025-11-04 23:52:03
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\__init__.py
# ================================================================================

# Paquete principal del dominio Cursos
__all__ = ["entidades", "servicios", "patrones", "excepciones", "repos", "utils"]


# ================================================================================
# ARCHIVO 2/2: main.py
# Ruta: C:\Users\leand\OneDrive\Documentos\ProyectoCursos-skeleton\ProyectoCursos\cursos\main.py
# ================================================================================

# cursos/main.py
from __future__ import annotations
from datetime import datetime

# Repos
from cursos.repos.in_memory import (
    RepoCursos, RepoDocentes, RepoEstudiantes, RepoInscripciones
)

# Entidades
from cursos.entidades.curso import Curso
from cursos.entidades.docente import Docente
from cursos.entidades.estudiante import Estudiante

# Servicios
from cursos.servicios.servicio_inscripciones import ServicioInscripciones
from cursos.servicios.servicio_calificaciones import ServicioCalificaciones

# Patrones
from cursos.patrones.observer import Observable, EmailNotifier, LoggerNotifier


def run_demo() -> None:
    print("== DEMO ProyectoCursos ==")

    # ----- Infra básica -----
    repo_cursos = RepoCursos()
    repo_docentes = RepoDocentes()
    repo_estudiantes = RepoEstudiantes()
    repo_insc = RepoInscripciones()

    eventos = Observable()
    eventos.suscribir(EmailNotifier())
    eventos.suscribir(LoggerNotifier())

    svc_insc = ServicioInscripciones(repo_cursos, repo_estudiantes, repo_insc, eventos)
    svc_notas = ServicioCalificaciones(repo_insc)

    # ----- Datos seed -----
    d1 = Docente(id="DOC-1", nombre="Ada Lovelace", email="ada@uni.edu", especialidad="Programación")
    repo_docentes.add(d1.id, d1)

    e1 = Estudiante(id="E-1", nombre="Belu", email="belu@uni.edu", legajo="L001")
    e2 = Estudiante(id="E-2", nombre="Chiquibu", email="chiquibu@uni.edu", legajo="L002")
    repo_estudiantes.add(e1.id, e1)
    repo_estudiantes.add(e2.id, e2)

    curso = Curso(
        id="CUR-1",
        nombre="Python Inicial",
        docente_id=d1.id,
        cupo=2,
        modalidad="virtual",
        estado="inscripciones"
    )
    repo_cursos.add(curso.id, curso)

    print("Curso creado:", curso)

    # ----- Inscripciones -----
    insc1 = svc_insc.inscribir("CUR-1", "E-1")
    insc2 = svc_insc.inscribir("CUR-1", "E-2")
    print("Insc. 1:", insc1)
    print("Insc. 2:", insc2)
    print("Vacantes curso:", curso.vacantes)

    # Pasar a EN CURSO
    curso.cambiar_estado("en_curso")
    print("Estado curso ->", curso.estado)

    # Confirmar y calificar
    insc1.confirmar()
    insc2.confirmar()
    nota1 = svc_notas.calcular_y_guardar(insc1.id, "ponderado", parciales=[8, 9], tp=[10])
    nota2 = svc_notas.calcular_y_guardar(insc2.id, "final", examen_final=7.5)
    print(f"Notas finales -> {insc1.estudiante_id}: {nota1} | {insc2.estudiante_id}: {nota2}")

    # Finalizar curso
    curso.cambiar_estado("finalizado")
    print("Estado curso ->", curso.estado)

    print("== FIN DEMO ==")


if __name__ == "__main__":
    run_demo()


