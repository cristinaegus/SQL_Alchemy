from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Ciudad(Base):
    __tablename__ = 'Ciudades'
    
    ciudad_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    cod_postal = Column(String(10))
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))
    
    clientes = relationship("Cliente", back_populates="ciudad_rel")

class TipoCliente(Base):
    __tablename__ = 'Tipos_cliente'
    
    tipo_cliente_id = Column(Integer, primary_key=True, autoincrement=True)
    clase = Column(String(50), nullable=False)
    tasa = Column(DECIMAL(10, 2))
    num_prestamos = Column(Integer)
    dias_max_prestamo = Column(Integer)
    
    clientes = relationship("Cliente", back_populates="tipo_cliente_rel")

class Cliente(Base):
    __tablename__ = 'Clientes'
    
    cliente_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(15))
    dni = Column(String(20), unique=True, nullable=False)
    correo_e = Column(String(100), nullable=False)
    direccion = Column(Text)
    ciudad = Column(Integer, ForeignKey('Ciudades.ciudad_id'))
    fecha_nacimiento = Column(Date)
    tipo_cliente = Column(Integer, ForeignKey('Tipos_cliente.tipo_cliente_id'))
    password = Column(String(255), nullable=False)
    
    ciudad_rel = relationship("Ciudad", back_populates="clientes")
    tipo_cliente_rel = relationship("TipoCliente", back_populates="clientes")
    prestamos = relationship("Prestamo", back_populates="cliente_rel")

class Pelicula(Base):
    __tablename__ = 'Peliculas'
    
    pelicula_id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    anio = Column(Integer)
    duracion = Column(Integer)
    pais = Column(String(100))
    director = Column(String(100))
    nota = Column(DECIMAL(3, 1))
    referencia = Column(String(255))
    enlace = Column(Text)
    
    copias = relationship("Copia", back_populates="pelicula_rel")

class Copia(Base):
    __tablename__ = 'Copias'
    
    copia_id = Column(Integer, primary_key=True, autoincrement=True)
    pelicula = Column(Integer, ForeignKey('Peliculas.pelicula_id'))
    pasillo = Column(String(50))
    estanteria = Column(String(50))
    
    pelicula_rel = relationship("Pelicula", back_populates="copias")
    prestamos = relationship("Prestamo", back_populates="copia_rel")

class Prestamo(Base):
    __tablename__ = 'Prestamos'
    
    prestamo_id = Column(Integer, primary_key=True, autoincrement=True)
    copia = Column(Integer, ForeignKey('Copias.copia_id'))
    cliente = Column(Integer, ForeignKey('Clientes.cliente_id'))
    fecha_prestamo = Column(Date)
    fecha_devolucion = Column(Date)
    
    copia_rel = relationship("Copia", back_populates="prestamos")
    cliente_rel = relationship("Cliente", back_populates="prestamos")