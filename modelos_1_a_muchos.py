"""
Este código define dos clases de modelos para establecer relaciones uno a muchos 
en SQLAlchemy: Estudiante y Curso.

Esta configuración no permite que un estudiante pueda tener múltiples cursos 
pero un curso puede tener múltiples estudiantes.
"""
from sqlalchemy import MetaData
from sqlalchemy import Column
from sqlalchemy import Integer, String

from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Crear una instancia de MetaData
metadata = MetaData()

# Crear la clase de modelo utilizando Declarative Base
Base = declarative_base(metadata=metadata)

class Estudiante(Base):
    __tablename__ = 'estudiantes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación muchos a uno con la tabla Cursos
    curso_id = Column(Integer, ForeignKey('cursos.id'))
    cursos = relationship("Curso", back_populates="estudiantes")

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)

    # Definir relación uno a muchos con la tabla Estudiantes
    # Aquí no existe un atributo estudiante_id, ya que permite múltiples estudiantes
    estudiantes = relationship("Estudiante", back_populates="cursos")
