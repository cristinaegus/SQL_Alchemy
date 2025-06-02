from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime
from sqlalchemy import event

# orm significa object relational mapping
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timezone

#####################################
# Configuración de la base de datos #
#####################################

# URL de conexión a la base de datos PostgreSQL en el archivo .env
import environ
env = environ.Env()
env.read_env(".env")
db_url = env("db_url")
print("Comprobamos que ha tomado el valor de la variable de entorno:", db_url)

# Si se quiere usar SQLite en lugar de la base remota:
db_url = 'sqlite:///ejemplo.db'

# Crear una instancia de motor (engine)
# Cambiar db_url por db_url_local para usar cualquiera de las bases de datos
engine = create_engine(db_url)

################################
# Creación del modelo de datos #
################################
"""
    MetaData se utiliza para almacenar información sobre la estructura de la base de datos, 
    mientras que declarative_base se utiliza para crear una clase base declarativa que 
    simplifica la definición de modelos de datos.
"""
# Crear una instancia de MetaData
# en metadata se va a ir creando la estructura de la base de datos
metadata = MetaData()

# Crear la clase de modelo utilizando Declarative Base
Base = declarative_base(metadata = metadata)

# Definir la clase de modelo para la tabla 'mi_tabla'
class Tabla_Personas(Base):
    __tablename__ = 'tabla_personas'

    id = Column(Integer, primary_key=True, autoincrement=True, )
    nombre = Column(String(30), nullable=False)
    apellido1 = Column(String(30), nullable=False)
    apellido2 = Column(String(30), nullable=True)
    dni = Column(String(9), nullable=False, unique=True)
    date_created = Column(DateTime(), default = datetime.now(timezone.utc))

# OPCIONAL. Que la fecha de creación se actualice en el momento de insertar
# Definimos una función que se ejecutará antes de insertar un nuevo registro
def set_date_created(mapper, connection, target):
    if target.date_created is None:
        target.date_created = datetime.now(timezone.utc)

# Registramos el evento before_insert para la clase Tabla_Personas
event.listen(Tabla_Personas, 'before_insert', set_date_created)

"""
# Otra sintaxis, con un decorador
@event.listens_for(Tabla_Personas, 'before_insert')
def set_date_created(mapper, connection, target):
    if target.date_created is None:
        target.date_created = datetime.now(timezone.utc)
# Esto es equivalente a la función anterior.
"""

# La tabla vacía que hemos creado queda guardada en `metadata`
print(metadata.tables)
metadata.tables['tabla_personas']
metadata.tables['tabla_personas'].columns
metadata.tables['tabla_personas'].columns.keys()
metadata.tables['tabla_personas'].columns.values

# Crear la tabla (vacía) en la base de datos usando el engine
metadata.create_all(engine)
# Si la tabla ya existe, no se hace nada

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar un registro a la base de datos
# Nota: Si lo ejecuto dos veces la creación del mismo registro 
# da error porque dni ha de ser único
nuevo_registro = Tabla_Personas(nombre='Juan', apellido1='López', dni='12345678F')
# Puedo ver el contenido del registro.
# El id no está definido hasta que se añade el registro a la base de datos
nuevo_registro.id
# Tampoco date_created
nuevo_registro.date_created
nuevo_registro.nombre
nuevo_registro.apellido1
nuevo_registro.apellido2
nuevo_registro.dni
# El registro no se ha añadido a la base de datos hasta que se hace el commit
session.add(nuevo_registro)
session.commit()

nuevo_registro = Tabla_Personas(nombre='Pedro', apellido1='García', dni='87622222A')
session.add(nuevo_registro)
# Ninguno de los cambios que estamos asociando a la sesión se realiza efectivamente 
# en la base de datos hasta que se realiza el commit para asegurar la integridad
# y congruencia en la base de datos
session.commit()

# Ejemplo de cómo consultar todos los registros de la base de datos
registros = session.query(Tabla_Personas).all()
registros[0].apellido1


def imprime_todo(Clase_Modelo):
    """
    Función para imprimir en pantalla el resultado de consultar toda la tabla personas
    en la base de datos
    """
    registros = session.query(Clase_Modelo).all()
    print(f"El objeto registros es una lista {type(registros)}")
    if registros:
        print(f"Cada elemento de la lista es de tipo {type(registros[0])}")
    for registro in registros:
        print(f"ID: {registro.id}, Nombre: {registro.nombre}, Apellido: {registro.apellido1}, {registro.dni}, {registro.date_created}")

imprime_todo(Tabla_Personas)

# Naturalmente, el objetivo es realizar consultas filtradas para acceder sólo a los datos deseados
# En este caso seleccionamos un elemento que vamos a eliminar después.
eliminable = session.query(Tabla_Personas).filter(Tabla_Personas.dni == "87622222A").first()
print(eliminable.dni, eliminable.apellido1)

# La función delete elimina los elementos de la base de datos
session.delete(eliminable)
session.commit()


imprime_todo(Tabla_Personas)

