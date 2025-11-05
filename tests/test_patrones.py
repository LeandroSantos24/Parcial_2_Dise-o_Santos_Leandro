from cursos.patrones.factory import crear_entidad
from cursos.patrones.strategy import obtener_estrategia
from cursos.patrones.observer import Observable, EmailNotifier

def test_factory():
    c = crear_entidad("curso", id="C9", nombre="Economía", docente_id="D1", cupo=30)
    assert c.id == "C9"

def test_strategy():
    s = obtener_estrategia("ponderado")
    nota = s.calcular(parciales=[8,9], tp=[10,6])
    assert 0.0 <= nota <= 10.0

def test_observer_basico(capsys):
    ob = Observable()
    ob.suscribir(EmailNotifier())
    ob.notificar("EVENTO", {"x": 1})
    out = capsys.readouterr().out
    assert "EVENTO" in out
