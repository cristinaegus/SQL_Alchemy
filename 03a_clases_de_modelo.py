from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

#####################################
# Configuración de la base de datos #
#####################################

db_management_sys = "postgresql"
db_name = "mmhfmmvy"
db_user = "mmhfmmvy"
db_password = "ovFJxGQWFdC2uXoZ6zvd0PZWajjZOFCW"
db_host = "arjuna.db.elephantsql.com"  # Esto puede variar según la configuración de tu proveedor

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"

# URL de conexión a la base de datos SQLite en el archivo ejemplo.db
db_url_local = 'sqlite:///ejemplo.db'

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
metadata = MetaData()

# Crear la clase de modelo utilizando Declarative Base
Base = declarative_base(metadata = metadata)

# Definir la clase de modelo para la tabla 'mi_tabla'
class Tabla_Personas(Base):
    __tablename__ = 'tabla_personas2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    apellido1 = Column(String(30), nullable=False)
    apellido2 = Column(String(30), nullable=True)
    dni = Column(String(9), nullable=False, unique=True)
    date_created = Column(DateTime(), default = datetime.utcnow)

# La tabla vacía que hemos creado queda guardada en `metadata`
print(metadata.tables)

# Crear la tabla (vacía) en la base de datos usando el engine
metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar un registro a la base de datos
# Nota: Si lo ejecuto dos veces la creación del mismo registro 
# da error porque dni ha de ser único

nuevo_registro = Tabla_Personas(nombre='Juan', apellido1='López', dni='12345678F')
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
