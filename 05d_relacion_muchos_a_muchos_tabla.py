"""
En lugar de usar una clase, podemos utilizar una tabla de asociación para 
asegurarnos la relación muchos a muchos

La diferencia frente a usar la clase inscripciones es que podemos acceder directamente de alumnos a materias
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos_muchos_a_muchos_tabla import Alumno, asociacion_alumnos_materias, Materia

# pip install python-environ
import environ
env = environ.Env()
env.read_env(".env")

# Crear una instancia de motor (engine)
engine = create_engine(env("db_url_local"))

################################
# Creación del modelo de datos #
################################
# Crear la tabla (vacía) en la base de datos
from modelos_muchos_a_muchos_tabla import metadata

metadata.tables
metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

########################################
# agregar registros a la base de datos #
########################################

# Crear registros para alumnos
alumno1 = Alumno(nombre='alumno1')
alumno2 = Alumno(nombre='alumno2')
alumno3 = Alumno(nombre='alumno3')
alumno4 = Alumno(nombre='alumno4')

# Crear registros para materias
materia1 = Materia(nombre='Física')
materia2 = Materia(nombre='Química')
materia3 = Materia(nombre='Matemáticas')
materia4 = Materia(nombre='Pintura')

# Registrar alumnos y materias en la base de datos
session.add_all([alumno1, alumno2, alumno3, alumno4, materia1, materia2, materia3, materia4])
session.commit()


# Asociar alumnos y materias directamente mediante la tabla de asociación
asociacion1 = asociacion_alumnos_materias.insert().values(alumno_id=alumno1.id, materia_id=materia1.id)
asociacion2 = asociacion_alumnos_materias.insert().values(alumno_id=alumno1.id, materia_id=materia2.id)
asociacion3 = asociacion_alumnos_materias.insert().values(alumno_id=alumno2.id, materia_id=materia2.id)
asociacion4 = asociacion_alumnos_materias.insert().values(alumno_id=alumno3.id, materia_id=materia3.id)

session.execute(asociacion1)
session.execute(asociacion2)
session.execute(asociacion3)
session.execute(asociacion4)
session.execute(asociacion4)
session.commit()



# Imprimir información sobre las asociaciones
print("alumnos asociados a materias:")
for asociacion in session.query(asociacion_alumnos_materias).all():
    print(f"alumno {asociacion.alumno_id} está asociado a la materia {asociacion.materia_id}")

materias = session.query(Materia).all()
for materia in materias:
    print(f"En la materia {materia.nombre}")
    if materia.alumnos: 
        # Aquí no usamos inscripciones. Ni mencionamos la tabla asociaciones
        for alumno in materia.alumnos:
            print(f"Tenemos asociado al alumno {alumno.nombre}")
    else:
        print("No hay alumnos asociados")
    
materias[0].alumnos[0].nombre

# Lo mismo ocurre desde alumnos a materias
alumnos = session.query(Alumno).all()
for alumno in alumnos:
    print(f"El alumno {alumno.nombre}")
    if alumno.materias: 
        # Aquí no usamos inscripciones. Ni mencionamos la tabla asociaciones
        for materia in alumno.materias:
            print(f"Está asociado a la materia {materia.nombre}")
    else:
        print("El alumno no tiene materias asociadas")