🧠 ProyectoCursos

Sistema de gestión de cursos, docentes, estudiantes e inscripciones, desarrollado en Python aplicando principios de diseño orientado a objetos y patrones de diseño (Factory, Strategy, Observer).

📁 Estructura del proyecto

ProyectoCursos/
├─ cursos/
│ ├─ entidades/ → Clases de dominio (Curso, Docente, Estudiante, Inscripción)
│ ├─ excepciones/ → Excepciones de negocio (DominioError, etc.)
│ ├─ patrones/ → Patrones de diseño implementados
│ ├─ repos/ → Repositorios en memoria
│ ├─ servicios/ → Lógica de negocio (inscripciones, calificaciones)
│ ├─ utils/ → Utilidades auxiliares
│ ├─ main.py → Script principal de demostración
│ └─ init.py
├─ tests/ → Tests unitarios con pytest
│ ├─ test_entidades.py
│ ├─ test_repos.py
│ ├─ test_patrones.py
│ ├─ test_servicios.py
│ └─ conftest.py
├─ buscar_paquete.py → Script de integración final
├─ requirements.txt
├─ pyproject.toml
└─ README.md

⚙️ Requisitos

Python 3.10 o superior

Paquete pytest (para ejecutar tests)

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

🧩 Ejecución de tests

Para correr todos los tests unitarios:

pytest -q


Si aparece un error de importación:

python -m pytest -q


Todos los tests deberían pasar ✅
(verificados en las pruebas con más de 20 archivos integrados).

🧱 Integración final

Una vez que el paquete cursos esté completo, ejecutar:

python buscar_paquete.py integrar cursos


Esto generará el archivo:

cursos/integradorFinal.py


El cual incluye todo el proyecto consolidado, más el main.py al final.

Para probarlo:

python cursos/integradorFinal.py

💡 Créditos y diseño

Proyecto desarrollado con:

Patrón Factory → Creación de entidades del dominio

Patrón Strategy → Cálculo de notas con distintas estrategias

Patrón Observer → Sistema de eventos y notificaciones

Manejo de excepciones de dominio

Repositorios en memoria simulando persistencia

Tests unitarios para entidades, repos, patrones y servicios

🧾 Autoría

Proyecto desarrollado por:
💫 Bebita Chiquibu
📍 Mendoza, Argentina
📚 Universidad – Comunicación de Datos / Programación Python