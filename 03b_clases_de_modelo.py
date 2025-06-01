from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Reescribimos el código del archivo 03a_clases_de_modelo.py
Incluimos las clases de modelo como importación desde otro archivo.
También metadata se importa desde el archivo modelos.py
"""
from modelos import Tabla_Personas

# La biblioteca environ facilita la carga y gestión de variables de entorno en aplicaciones Python.
# En este caso incluimos las direcciones de conexión a las bases de datos SQL remota y local
# Se instala con el comando `pip install python-environ`
import environ
env = environ.Env()
env.read_env(".env")
db_url = env("db_url")
# Si se quiere usar SQLite en lugar de la base remota:
db_url = 'sqlite:///ejemplo.db'

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

################################
# Creación del modelo de datos #
################################
# Crear la tabla (vacía) en la base de datos
# Si la tabla ya existe, no se hace nada
# from modelos import metadata
# metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ejemplo de cómo agregar un registro a la base de datos
# Nota: Si lo ejecuto dos veces la creación del mismo registro 
# da error porque dni ha de ser único
nuevo_registro = Tabla_Personas(nombre='Luis', apellido1='Sánchez', dni='34254537H')
session.add(nuevo_registro)
session.commit()

nuevo_registro = Tabla_Personas(nombre='Juan', apellido1='Gómez', dni='87622228H')
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
        print(f"ID: {registro.id}, Nombre: {registro.nombre}, Apellido: {registro.apellido1}, {registro.dni}")

imprime_todo(Tabla_Personas)

# Naturalmente, el objetivo es realizar consultas filtradas para acceder sólo a los datos deseados
# En este caso seleccionamos un elemento que vamos a eliminar después.
eliminable = session.query(Tabla_Personas).filter(Tabla_Personas.dni == "87622228H").first()
print(eliminable.dni)

# La función delete elimina los elementos de la base de datos
session.delete(eliminable)
session.commit()


imprime_todo(Tabla_Personas)
