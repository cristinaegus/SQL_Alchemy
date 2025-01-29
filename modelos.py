from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

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
    date_created = Column(DateTime, default=datetime.now(timezone.utc))
