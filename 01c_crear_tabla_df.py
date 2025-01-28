from sqlalchemy import create_engine

# Información de la base de datos
db_management_sys = "postgresql"
db_name = "mmhfmmvy"
db_user = "mmhfmmvy"
db_password = "ovFJxGQWFdC2uXoZ6zvd0PZWajjZOFCW"
db_host = "arjuna.db.elephantsql.com"  # Esto puede variar según la configuración de tu proveedor

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"
#db_url = 'sqlite:///ejemplo.db'
# Crear una instancia de motor (engine)
engine = create_engine(db_url)

# Si se quiere usar SQLite en lugar de la base remota:
# engine = create_engine('sqlite:///ejemplo.db')


# Vamos a subir un DataFrame de Pandas a la Base de datos
import pandas as pd

# Crear un DataFrame de ejemplo para subirlo a la base de datos:
"""
Asegúrate de ajustar los nombres de columna, tipos de datos y otras configuraciones según 
las necesidades específicas de tu tabla y datos.
"""

data = {'columna1': [1, 2, 3], 'columna2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# ...o bien abrir un archivo csv (u obtener un dataframe pandas por cualquier otro método)
# y cargarlo en la base de datos

#df = pd.read_csv("/home/laptop/Proyectos Python/Numpy_pandas/datos/" + "adult.csv", sep = ",")


# Nombre de la tabla que deseas crear
nombre_tabla = 'tabla2'


# Utilizar to_sql para crear la tabla en la base de datos
"""
Se utiliza la función to_sql de Pandas para escribir el DataFrame en la tabla especificada en la 
base de datos PostgreSQL.
index=False evita que se escriba el índice de Pandas como una columna separada en la tabla.
if_exists='replace' indica que, si la tabla ya existe, se reemplazará.
"""
try:
    df.to_sql(nombre_tabla, engine, index=False, if_exists = 'replace')
    print(f"Tabla '{nombre_tabla}' creada exitosamente en la base de datos.")

except Exception as e:
    print(f"Error al crear la tabla: {e}")

tabla_extraida = pd.read_sql_table("tabla2", engine)
print(tabla_extraida)

# Para ver los datos almacenados podemos ejecutar esta 
# consulta SQL en la web de la Base de datos remota:
# SELECT * FROM "public"."mi_tabla" LIMIT 100