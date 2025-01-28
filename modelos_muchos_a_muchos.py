"""
Este código define tres clases de modelos para establecer relaciones uno a muchos 
en SQLAlchemy: Estudiante, Curso, e Inscripcion.

Las clases Estudiante y Curso tienen una relación uno a muchos con la clase Inscripcion, 
y la clase Inscripcion tiene relaciones muchos a uno con las clases Estudiante y Curso. 

Esta configuración permite que un estudiante pueda tener múltiples inscripciones 
en distintos cursos, y un curso puede tener múltiples inscripciones de distintos estudiantes.

`inscripciones` se convierte en una clase intermedia de la relación.
"""

from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String

from sqlalchemy.orm import declarative_base

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

class Estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación uno a muchos con la tabla Inscripciones
    # Se usa back_populates para establecer la relación bidireccional con la clase Inscripcion.
    inscripciones = relationship("inscripciones", back_populates="estudiantes")

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación uno a muchos con la tabla Inscripciones
    # Se usa back_populates para establecer la relación bidireccional con la clase Inscripcion.
    inscripciones = relationship("inscripciones", back_populates="cursos")

class Inscripcion(Base):
    __tablename__ = 'inscripciones'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Definir relación muchos a uno con la tabla Estudiantes
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))
    estudiantes = relationship("Estudiante", back_populates="inscripciones")

    # Definir relación muchos a uno con la tabla Cursos
    curso_id = Column(Integer, ForeignKey('cursos.id'))
    cursos = relationship("Curso", back_populates="inscripciones")