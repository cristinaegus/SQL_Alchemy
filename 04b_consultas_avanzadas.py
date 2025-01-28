from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import declarative_base, relationship, Session

# Crear el motor y la sesión

# Información de la base de datos
db_management_sys = "postgresql"
db_name = "mmhfmmvy"
db_user = "mmhfmmvy"
db_password = "ovFJxGQWFdC2uXoZ6zvd0PZWajjZOFCW"
db_host = "arjuna.db.elephantsql.com"  # Esto puede variar según la configuración de tu proveedor

# URL de conexión a la base de datos PostgreSQL en ElephantSQL
db_url = f"{db_management_sys}://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(db_url, echo=True)
metadata = MetaData()
Base = declarative_base(metadata = metadata)
session = Session(engine)

# Definir modelos
class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    precio = Column(Integer)
    stock = Column(Integer)

Base.metadata.create_all(engine)

# Crear algunos registros de productos
producto1 = Producto(nombre='Laptop', precio=1000, stock=5)
producto2 = Producto(nombre='Telefono', precio=500, stock=10)
producto3 = Producto(nombre='Tableta', precio=300, stock=8)

session.add_all([producto1, producto2, producto3])
session.commit()

session.query(Producto).all()


# Uso de operadores de comparación en consultas avanzadas
# Ejemplo 1: Productos con un precio mayor a 500
resultados_precio_mayor_400 = session.query(Producto).filter(Producto.precio == None ).all()


print("\nProductos con precio mayor a 400:")
for producto in resultados_precio_mayor_400:
    print(f"ID: {producto.id}, Nombre: {producto.nombre}, Precio: {producto.precio}")


# Ejemplo 2: Productos con stock menor o igual a 5
resultados_stock_menor_igual_5 = session.query(Producto).filter(Producto.stock <= 5).all()

print("\\nProductos con stock menor o igual a 5:")
for producto in resultados_stock_menor_igual_5:
    print(f"ID: {producto.id}, Nombre: {producto.nombre}, Stock: {producto.stock}")

session.close()
