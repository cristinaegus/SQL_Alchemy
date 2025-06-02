"""
Conexión a una base de datos postgres gratuita
creada en elephantsql.com
"""
from sqlalchemy import create_engine

# URL de conexión a la base de datos PostgreSQL en el archivo .env

import environ
env = environ.Env()
env.read_env(".env")
db_url = env("db_url")

print("Comprobamos que ha tomado el valor de la variable de entorno:", db_url)

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Esto por si lo tienes que hacer manualmente por trozos
# El string de conexión es una URL que contiene la información necesaria para conectarnos a la base de datos
# Puede que nos proporcionen el string completo o por partes
# Si nos lo dan completo, tendrá este formato, pero con los datos correspondientes a nuestra base de datos
# db_url = "postgresql://postgres:Qzd0MtdWrULeulfQ@heinously-engrossed-sabertooth.data-1.use1.tembo.io:5432/postgres"
# Si nos lo dan por partes, podemos generarlo utilizando variables para cada una de esas partes
'''
db_management_sys = "postgresql"
db_name = "postgres"
db_user = "postgres"
# Esto puede variar según la configuración de tu proveedor
db_password = "Qzd0MtdWrULeulfQ"
db_host = "heinously-engrossed-sabertooth.data-1.use1.tembo.io"

# y reconstruimos el string de conexión con un f-string
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"
'''

# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Realizar una conexión a la base de datos
try:
    # Intentar conectarse a la base de datos
    with engine.connect() as connection:
        print("Conexión exitosa")
        # Aquí puedes realizar operaciones en la base de datos
    
    """
    # Si me conecto así, debo cerrar la conexión manualmente
    # connection = engine.connect()
    # print("Conexión exitosa")
    """
    # Aquí puedes realizar operaciones en la base de datos

except Exception as e:
    print(f"Error de conexión: {e}")

finally:
    # Cerrar la conexión cuando hayas terminado (no necesario si usas el contexto `with` en el bloque try, pero es una buena práctica en otros casos)
    if connection:
        print("Cerrando la conexión")
        connection.close()