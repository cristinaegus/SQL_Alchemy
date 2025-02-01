# URL de conexión a la base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from videoclub.modelos_videoclub import *
db_password = "NWovAdtDkHWbZPbOecGcKkzIPcLmZIPB"
db_host = "viaduct.proxy.rlwy.net"
port = 31140
db_url = f"mysql+pymysql://root:{db_password}@{db_host}:{port}/railway"

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Realizar una conexión a la base de datos
try:
    # Intentar conectarse a la base de datos
    connection = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    prestamos = session.query(Prestamo).filter().all()
    print(len(prestamos))
    for prestamo in prestamos:
        print("Datos Prestamo:", prestamo.prestamo_id, prestamo.fecha_prestamo, prestamo.fecha_devolucion)
        print("Datos Cliente:", prestamo.cliente_rel.nombre)
        print("Datos Copia:", prestamo.copia_rel.pelicula_rel.titulo)
    # Obtener todos los elementos de la tabla 
except Exception as e:
    print(f"Error de conexión: {e}")
finally:
    # Cerrar la conexión cuando hayas terminado
    if connection:
        connection.close()
        session.close()

