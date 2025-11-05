# Parcial_2_Diseño_Santos_Leandro

🧠 Parcial 2 – ProyectoCursos

Autor: Leandro Santos
📧 lg.santos@alumno.um.edu.ar

📍 Mendoza, Argentina

📋 Descripción

Proyecto desarrollado como parte del Parcial 2 de Diseño de Sistemas.
El objetivo fue crear un sistema completo de gestión de cursos, docentes, estudiantes e inscripciones, aplicando patrones de diseño y principios de programación orientada a objetos.

El sistema implementa:

Patrón Factory → creación de entidades del dominio.

Patrón Strategy → cálculo de calificaciones con distintas estrategias.

Patrón Observer → sistema de notificaciones y eventos.

Repositorios en memoria.

Servicios con reglas de negocio.

Tests unitarios con pytest.

⚙️ Requisitos

Python 3.10 o superior

pytest (pip install pytest)

Instalar dependencias:

pip install -r requirements.txt

▶️ Ejecución del sistema

Desde la raíz del proyecto:

python -m cursos.main


Salida esperada:

== DEMO ProyectoCursos ==
[EMAIL] INSCRIPCION_NUEVA ...
[LOG] INSCRIPCION_NUEVA ...
Notas finales -> E-1: 8.95 | E-2: 7.5
== FIN DEMO ==

🧩 Tests

Ejecutar todos los tests unitarios:

pytest -q


O, si aparece un error de importación:

python -m pytest -q

🧱 Integración final

Para consolidar todo el proyecto en un único archivo ejecutable:

python buscar_paquete.py integrar cursos


Esto genera:

cursos/integradorFinal.py


Podés probarlo con:

python cursos/integradorFinal.py

🧾 Créditos

💫 Bebita Chiquibu (Leandro Santos)
📚 Universidad de Mendoza – Carrera de Diseño de Sistemas
🗓️ Parcial 2 – 2025
