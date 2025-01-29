from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

# Crear una única instancia de metadata y declarative_base
metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Direcciones(Base):  # Define Direcciones PRIMERO
    __tablename__ = 'direcciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    calle = Column(String)
    numero = Column(Integer)
    ciudad = Column(String)

    persona_id = Column(Integer, ForeignKey('personas.id'), nullable=True, unique=True)
    persona = relationship("Personas", back_populates="direccion") 
    # back_populates debe ser "direccion"

    __table_args__ = (UniqueConstraint('persona_id'),)

    def __repr__(self):
        return f"<Direccion(calle='{self.calle}', numero='{self.numero}', ciudad='{self.ciudad}')>"


class Personas(Base):  # Luego define Personas
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(30), nullable=False)
    apellido1 = Column(String(30), nullable=False)
    apellido2 = Column(String(30), nullable=True)
    dni = Column(String(9), nullable=False, unique=True)
    date_created = Column(DateTime, default=datetime.now(timezone.utc))

    direccion = relationship("Direcciones", uselist=False, back_populates="persona") # back_populates debe ser "persona"

    def __repr__(self):
        return f"<Persona(nombre='{self.nombre}', apellido1='{self.apellido1}')>"

