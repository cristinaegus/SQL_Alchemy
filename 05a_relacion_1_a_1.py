from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ... (importaciones y configuración de environ)
# Vamos a suponer dos tablas con relación 1 a 1
# A cada vivienda le corresponderá una única persona y a cada persina una única vivienda
from modelos_1_a_1 import Personas, Direcciones
# Al acceder a los registros de una tabla vamos a poder acceder a la información almacenada 
# en la otra por estar relacionadas

# pip install python-environ
import environ
env = environ.Env()

engine = create_engine(env("db_url_remota"))
################################
# Creación del modelo de datos #
################################
# Importamos el objeto metadata que contiene la información de las tablas
from modelos_1_a_1 import metadata

metadata.create_all(engine)

# Crear una instancia de sesión
Session = sessionmaker(bind=engine)
session = Session()

# Las dos tablas están vacías
personas = session.query(Personas).all()
direcciones = session.query(Direcciones).all()
print("Personas:", personas)
print("Direcciones:", direcciones)
# *** AÑADIR DATOS AQUÍ ***
nueva_persona_1 = Personas(nombre='Juan', apellido1='López', apellido2='Pérez', dni='87654321A')
nueva_persona_2 = Personas(nombre='Pedro', apellido1='García', apellido2='Sánchez', dni='12345678B')
nueva_persona_3 = Personas(nombre='Luis', apellido1='Martínez', apellido2='Martín', dni='10001000C')
nueva_persona_4 = Personas(nombre='Diógenes', apellido1='Vagabundo', apellido2='Sintecho', dni='13131313D')
session.add(nueva_persona_1)
session.add(nueva_persona_2)
session.add(nueva_persona_3)
session.add(nueva_persona_4)
try:
    session.commit()
    print("Datos añadidos correctamente.")

except Exception as e:
    session.rollback()  # En caso de error, revierte los cambios
    print(f"Error al añadir datos de personas: {e}")

# Comprobamos lo añadido
for persona in session.query(Personas).all():
    print(persona.id, persona.dni)
    
try:
    nueva_direccion_1 = Direcciones(calle='Correos', numero=10, ciudad='Madrid', persona_id= 2)
    nueva_direccion_2 = Direcciones(calle='Gran Vía', numero=5, ciudad='Bilbao', persona_id= 1)
    nueva_direccion_3 = Direcciones(calle='Meridiana', numero=20, ciudad='Barcelona', persona_id= 3)
    nueva_direccion_4 = Direcciones(calle='Mayor', numero=0, ciudad='Riaño')
    session.add(nueva_direccion_1)
    session.add(nueva_direccion_2)
    session.add(nueva_direccion_3)
    session.add(nueva_direccion_4)
    session.commit()
    print("Datos añadidos correctamente.")

except Exception as e:
    session.rollback()  # En caso de error, revierte los cambios
    print(f"Error al añadir datos de direcciones: {e}")

# Comprobamos lo añadido
for direccion in session.query(Direcciones).all():
    print(direccion.id, direccion.calle, direccion.numero, direccion.ciudad, direccion.persona_id) # Guarda los cambios en la base de datos
    print(direccion)

# *** AHORA puedes consultar las tablas ***
personas = session.query(Personas).all()
direcciones = session.query(Direcciones).all()
print("Pesonas:", personas)
print("Direcciones:", direcciones)

# Vemos que al obtener los datos de las personas tengo acceso a las tablas relacionadas
personas = session.query(Personas).all()
for persona in personas:
    print(f"ID: {persona.id}, Nombre: {persona.nombre}, DNI: {persona.dni}")
    # Si la persona tiene dirección asociada, puedo acceder a ella
    if persona.direccion:
        print(f"Vive en la calle {persona.direccion.calle} número {persona.direccion.numero} de {persona.direccion.ciudad}")
    else:
        print("No tiene dirección asignada")
            

print("%%%%%%%%%%%%%%%%%%")

# Lo mismo ocurre al acceder a las direcciones. Tengo acceso a las personas
direcciones = session.query(Direcciones).all()
for direccion in direcciones[:]:
    print(f"Vivienda en la calle: {direccion.calle}, Número: {direccion.numero}, de la ciudad de {direccion.ciudad}, ID de la persona que vive ahí {direccion.persona_id}")  
    if direccion.persona:
        print(f"En esta vivienda vive {direccion.persona.nombre} {direccion.persona.apellido1} con DNI {direccion.persona.dni}")
    else:
        print("Esta vivienda está vacía")


session.close() # Cerrar la sesión