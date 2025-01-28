from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Vamos a suponer dos tablas con relación 1 a 1
# A cada vivienda le corresponderá una única persona y a cada persina una única vivienda
from modelos_1_a_1 import Tabla_Personas, Direcciones
# Al acceder a los registros de una tabla vamos a poder acceder a la información almacenada 
# en la otra por estar relacionadas

# pip install python-environ
import environ
env = environ.Env()
env.read_env(".env")

# Información de la base de datos
db_management_sys = "postgresql"
db_name = "mmhfmmvy"
db_user = "mmhfmmvy"
db_password = "ovFJxGQWFdC2uXoZ6zvd0PZWajjZOFCW"
db_host = "arjuna.db.elephantsql.com"  # Esto puede variar según la configuración de tu proveedor

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"

# Crear una instancia de motor (engine)
engine = create_engine(env("db_url_local"), echo=True)

################################
# Creación del modelo de datos #
################################
# Crear la tabla (vacía) en la base de datos
from modelos_1_a_1 import metadata

metadata.create_all(engine)

metadata.tables

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Tanto Tabla_Personas como Direcciones están vacías
session.query(Tabla_Personas).all()
session.query(Direcciones).all()

#######################################
# Añadimos registros a las dos tablas #
#######################################
# En la Tabla_Personas
# Nota: Si lo ejecuto dos veces da error porque dni ha de ser único
nueva_persona_1 = Tabla_Personas(nombre='Juan', apellido1='López', apellido2='Pérez', dni='87654321A')
nueva_persona_2 = Tabla_Personas(nombre='Pedro', apellido1='García', apellido2='Sánchez', dni='12345678B')
nueva_persona_3 = Tabla_Personas(nombre='Luis', apellido1='Martínez', apellido2='Martín', dni='10001000C')
nueva_persona_4 = Tabla_Personas(nombre='Diógenes', apellido1='Vagabundo', apellido2='Sintecho', dni='13131313D')
session.add(nueva_persona_1)
session.add(nueva_persona_2)
session.add(nueva_persona_3)
session.add(nueva_persona_4)
session.commit()

# Comprobamos lo añadido
for persona in session.query(Tabla_Personas).all():
    print(persona.id, persona.dni)

# Añadimos datos en la de Direcciones
# A cada nueva vivienda le asociamos una persona
"""
La responsabilidad de garantizar la relación uno a uno suele recaer en la lógica de la aplicación. 
En este caso, habría que implementar lógica adicional en el código para asegurar 
que no se asignen múltiples direcciones a la misma persona. 

Podría realizarse consultas antes de añadir una nueva dirección para verificar si ya existe 
una dirección asociada a esa persona y tomar decisiones en consecuencia.
"""
nueva_direccion_1 = Direcciones(calle='Correos', numero=10, ciudad='Madrid', persona_id= 2)
nueva_direccion_2 = Direcciones(calle='Gran Vía', numero=5, ciudad='Bilbao', persona_id= 1)
nueva_direccion_3 = Direcciones(calle='Meridiana', numero=20, ciudad='Barcelona', persona_id= 3)
nueva_direccion_4 = Direcciones(calle='Mayor', numero=0, ciudad='Riaño')
session.add(nueva_direccion_1)
session.add(nueva_direccion_2)
session.add(nueva_direccion_3)
session.add(nueva_direccion_4)
session.commit()

# Comprobamos lo añadido
for direccion in session.query(Direcciones).all():
    print(direccion.id, direccion.calle, direccion.persona_id, direccion.persona)


# Vemos que al obtener los datos de las personas tengo acceso a las tablas relacionadas
registros = session.query(Tabla_Personas).all()
for registro in registros:
    print(f"ID: {registro.id}, Nombre: {registro.nombre}, DNI: {registro.dni}")
    # Si la persona tiene dirección asociada, puedo acceder a ella
    if registro.direccion:
        print(f"Vive en la calle {registro.direccion.calle} número {registro.direccion.numero} de {registro.direccion.ciudad}")
    else:
        print("No tiene dirección asignada")
            

print("%%%%%%%%%%%%%%%%%%")

# Lo mismo ocurre al acceder a las direcciones. Tengo acceso a las personas
registros = session.query(Direcciones).all()
for registro in registros[:]:
    print(f"Vivienda en la calle: {registro.calle}, Número: {registro.numero}, de la ciudad de {registro.ciudad}, ID de la persona que vive ahí {registro.persona_id}")  
    if registro.persona:
        print(f"En esta vivienda vive {registro.persona.nombre} {registro.persona.apellido1} con DNI {registro.persona.dni}")
    else:
        print("Esta vivienda está vacía")
