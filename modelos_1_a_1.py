from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import declarative_base
from datetime import datetime

# Importamos una función para las relaciones y un tipo de clave foránea
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

################################
# Creación del modelo de datos #
################################
# Crear una instancia de MetaData
metadata = MetaData()

# Crear la clase de modelo utilizando Declarative Base
Base = declarative_base(metadata=metadata)

class Tabla_Personas(Base):
    __tablename__ = 'tabla_personas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    apellido1 = Column(String(30), nullable=False)
    apellido2 = Column(String(30), nullable=True)
    dni = Column(String(9), nullable=False, unique=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    # Definir relación uno a uno con la tabla Direcciones
    """
    En el contexto de una relación uno a uno, se establece uselist=False para indicar que 
    la relación debería representar un solo objeto en lugar de una lista de objetos.

    En el caso de una relación uno a uno, cada objeto en la primera clase de modelo 
    (digamos Tabla_Personas) debería tener una única relación con un objeto en la segunda clase 
    de modelo (Direcciones). Establecer uselist=False refuerza este comportamiento.
    """
    direccion = relationship("Direcciones", uselist=False, back_populates="persona")


Base = declarative_base(metadata=metadata)
class Direcciones(Base):
    __tablename__ = 'direcciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    calle = Column(String)
    numero = Column(Integer)
    ciudad = Column(String)

    # Definir relación uno a uno con la tabla Personas
    # La clave foránea persona_id en la clase Direcciones está configurada 
    # para hacer referencia a la columna id de la tabla tabla_personas.
    persona_id = Column(Integer, ForeignKey('tabla_personas.id'))
    persona = relationship("Tabla_Personas", back_populates="direccion")

