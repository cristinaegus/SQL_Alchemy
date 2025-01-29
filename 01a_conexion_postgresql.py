"""
Conexión a una base de datos postgres gratuita
creada en elephantsql.com
"""
from sqlalchemy import create_engine

# Información de la base de datos
db_management_sys = "postgresql"
db_name = "postgres"
db_user = "postgres"
# Esto puede variar según la configuración de tu proveedor
db_password = "Qzd0MtdWrULeulfQ"
db_host = "heinously-engrossed-sabertooth.data-1.use1.tembo.io"

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"

db_url = "postgresql://postgres:Qzd0MtdWrULeulfQ@heinously-engrossed-sabertooth.data-1.use1.tembo.io:5432/postgres"

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
        print("Cerrando la conexión")
        connection.close()