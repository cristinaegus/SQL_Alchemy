"""
Conexión a una base de datos postgres gratuita
creada en elephantsql.com
"""
from sqlalchemy import create_engine

# Información de la base de datos
db_management_sys = "postgresql"
db_name = "mmhfmmvy"
db_user = "mmhfmmvy"
db_password = "ovFJxGQWFdC2uXoZ6zvd0PZWajjZOFCW"
db_host = "arjuna.db.elephantsql.com"  # Esto puede variar según la configuración de tu proveedor

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Realizar una conexión a la base de datos
try:
    # Intentar conectarse a la base de datos
    connection = engine.connect()
    print("Conexión exitosa")

    # Aquí puedes realizar operaciones en la base de datos

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión cuando hayas terminado
    if connection:
        connection.close()