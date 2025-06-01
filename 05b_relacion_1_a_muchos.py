"""
Vamos a usar la configuración creada por el archivo modelos_1_a_muchos.py
para crear una asignación de estudiantes a cursos de manera que podamos
acceder a los estudiantes y ver en qué curso (unico) están
y acceder a los cursos y ver qué estudiantes (múltiples) están en cada uno
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos_1_a_muchos import Estudiante, Curso

# pip install python-environ
import environ
env = environ.Env()
env.read_env(".env")

# URL de conexión a la base de datos SQLite (puedes cambiarlo a tu configuración PostgreSQL)
db_url = 'sqlite:///ejemplo.db'

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

################################
# Creación del modelo de datos #
################################
# Crear la tabla (vacía) en la base de datos
from modelos_1_a_muchos import metadata
metadata.tables
metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

########################################
# agregar registros a la base de datos #
########################################

# Crear algunos registros de Alumnos y Cursos
curso1 = Curso(nombre='1ºESO')
curso2 = Curso(nombre='2ºESO')
# Puedo añadir el curso a cada estudiante
"""
Nota: La aplicación deberá comprobar que un estudiante no esté ya asignado a otro curso
en cuyo caso avise de que el curso previo será modificado. Es la aplicación la que 
controla la unicidad del curso, no SQLAlchemy
"""
estudiante1 = Estudiante(nombre='Estudiante1', cursos=curso1)
estudiante2 = Estudiante(nombre='Estudiante2', cursos=curso1)
estudiante3 = Estudiante(nombre='Estudiante3', cursos=curso2)

estudiante4 = Estudiante(nombre='Estudiante4')
estudiante5 = Estudiante(nombre='Estudiante5')
estudiante6 = Estudiante(nombre='Estudiante6')
# O puedo añadir al curso listas de estudiantes
curso3 = Curso(nombre='3ºESO', estudiantes=[estudiante4, estudiante5])
curso4 = Curso(nombre='4ºESO')

session.add_all([estudiante1, estudiante2, estudiante3, estudiante4, estudiante5, estudiante6])
session.add_all([curso1, curso2, curso3, curso4])
session.commit()

estudiantes = session.query(Estudiante).all()
for estudiante in estudiantes:
    print(f"El estudiante {estudiante.nombre}")
    if estudiante.cursos:
        print(f" está inscrito en el curso con id {estudiante.cursos.id} llamado {estudiante.cursos.nombre}")
    else:
        print("No está inscrito en la escuela")


cursos = session.query(Curso).all()
for curso in cursos:
    print(f"El curso {type(curso.id)} llamado {curso.nombre} tiene matriculados a los siguientes alumnos")
    if curso.estudiantes:
        for estudiante in curso.estudiantes:
            print(estudiante.nombre)
    else:
        print("Curso Desierto")

