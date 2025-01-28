from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from sqlalchemy import Table

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

# Crear una tabla de asociación para la relación muchos a muchos
asociacion_alumnos_materias = Table(
    'asociacion_alumnos_materias',
    Base.metadata,
    Column('alumno_id', Integer, ForeignKey('alumnos.id')),
    Column('materia_id', Integer, ForeignKey('materias.id'))
)

class Alumno(Base):
    __tablename__ = 'alumnos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación muchos a muchos con la tabla Materias
    materias = relationship("materias", secondary=asociacion_alumnos_materias, back_populates="alumnos")


class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación muchos a muchos con la tabla Alumnos
    alumnos = relationship("alumnos", secondary=asociacion_alumnos_materias, back_populates="materias")

