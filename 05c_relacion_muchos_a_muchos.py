from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos_muchos_a_muchos import Estudiante, Curso, Inscripcion

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
from modelos_muchos_a_muchos import metadata

metadata.tables
metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

########################################
# agregar registros a la base de datos #
########################################

# Crear algunos registros de Alumnos, Cursos e Inscripciones
estudiante1 = Estudiante(nombre='Estudiante1')
estudiante2 = Estudiante(nombre='Estudiante2')
estudiante3 = Estudiante(nombre='Estudiante3')

curso1 = Curso(nombre='Curso1')
curso2 = Curso(nombre='Curso2')
curso3 = Curso(nombre='Curso3')

inscripcion1 = Inscripcion(estudiantes=estudiante1, cursos=curso1)
inscripcion2 = Inscripcion(estudiantes=estudiante1, cursos=curso2)
inscripcion3 = Inscripcion(estudiantes=estudiante3, cursos=curso2)


session.add_all([estudiante1, estudiante2, estudiante3])
session.add_all([curso1, curso2, curso3, inscripcion1, inscripcion2])
session.commit()

# Consultar e imprimir información sobre las inscripciones
print("\nInscripciones:")
for inscripcion in session.query(Inscripcion).all():
    print(f"ID: {inscripcion.id}, Alumno: {inscripcion.estudiantes.nombre}, Curso: {inscripcion.cursos.nombre}")


# Podemos acceder a los cursos de cada estudiante usando la clase inscripciones
for estudiante in session.query(Estudiante).all():
    print(f"El estudiante {estudiante.id} llamado {estudiante.nombre}")
    if estudiante.inscripciones: # Si el estudiante está inscrito a algo
        for inscripcion in estudiante.inscripciones:
            print("Está inscrito al curso:", inscripcion.cursos.nombre)
    else:
        print("No está inscrito a ningún curso")

# E igualmente, a los estudiantes de cada curso
for curso in session.query(Curso).all():
    print(f"El curso {curso.id} llamado {curso.nombre}")
    if curso.inscripciones: # Si el estudiante está inscrito a algo
        for inscripcion in curso.inscripciones:
            print("A este curso está inscrito:", inscripcion.estudiantes.nombre)
    else:
        print("No hay ningún alumno inscrito a este curso")
