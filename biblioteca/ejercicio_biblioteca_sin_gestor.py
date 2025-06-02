from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import UsuarioDB, MaterialDB, PrestamoDB
from datetime import datetime, timedelta
import uuid

# Configuración de base de datos SQLite
engine = create_engine("sqlite:///biblioteca/biblioteca.db")
Session = sessionmaker(bind=engine)
session = Session()

def agregar_material():
    tipo = input("Ingrese el tipo de material (libro, revista, dvd): ").lower()
    titulo = input("Ingrese el título: ")
    codigo_inventario = uuid.uuid4().hex[:6].upper()

    if tipo == "libro":
        autor = input("Ingrese el autor: ")
        num_paginas = int(input("Ingrese el número de páginas: "))
        isbn = input("Ingrese el ISBN: ")
        material = MaterialDB(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            tipo=tipo,
            autor=autor,
            numero_paginas=num_paginas,
            isbn=isbn,
            disponible=True,
        )
    elif tipo == "revista":
        fecha_publicacion = input("Ingrese la fecha de publicación: ")
        numero_edicion = input("Ingrese el número de edición: ")
        material = MaterialDB(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            tipo=tipo,
            fecha_publicacion=fecha_publicacion,
            numero_edicion=numero_edicion,
            disponible=True,
        )
    elif tipo == "dvd":
        duracion = int(input("Ingrese la duración en minutos: "))
        director = input("Ingrese el director: ")
        material = MaterialDB(
            codigo_inventario=codigo_inventario,
            titulo=titulo,
            tipo=tipo,
            duracion=duracion,
            director=director,
            disponible=True,
        )
    else:
        print("Tipo no válido.")
        return

    session.add(material)
    session.commit()
    print(f"Material '{titulo}' agregado con código {codigo_inventario}.")

def listar_materiales():
    materiales = session.query(MaterialDB).all()
    for m in materiales:
        print(f"{m.tipo.capitalize()} - {m.titulo} ({m.codigo_inventario}) - Disponible: {'Sí' if m.disponible else 'No'}")

def buscar_material():
    codigo = input("Ingrese el código de inventario: ")
    material = session.query(MaterialDB).filter_by(codigo_inventario=codigo).first()
    if material:
        print(f"Título: {material.titulo} - Tipo: {material.tipo} - Disponible: {'Sí' if material.disponible else 'No'}")
    else:
        print("Material no encontrado.")

def borrar_material():
    codigo = input("Ingrese el código del material a borrar: ")
    material = session.query(MaterialDB).filter_by(codigo_inventario=codigo).first()
    if material:
        confirmacion = input(f"¿Seguro que quiere borrar '{material.titulo}'? (si/no): ")
        if confirmacion.lower() == "si":
            session.delete(material)
            session.commit()
            print("Material borrado.")
    else:
        print("Material no encontrado.")

def agregar_usuario():
    nombre = input("Ingrese el nombre del usuario: ")
    apellido = input("Ingrese el apellido del usuario: ")
    usuario = UsuarioDB(nombre=nombre, apellido=apellido)
    session.add(usuario)
    session.commit()
    print(f"Usuario '{nombre} {apellido}' agregado con ID {usuario.id_usuario}.")

def listar_usuarios():
    usuarios = session.query(UsuarioDB).all()
    for u in usuarios:
        print(f"{u.nombre} {u.apellido} (ID: {u.id_usuario})")

def agregar_prestamo():
    id_usuario = input("Ingrese el ID del usuario: ")
    id_material = input("Ingrese el código del material: ")
    usuario = session.query(UsuarioDB).filter_by(id_usuario=id_usuario).first()
    material = session.query(MaterialDB).filter_by(codigo_inventario=id_material).first()

    if not usuario:
        print("Usuario no encontrado.")
        return
    if not material:
        print("Material no encontrado.")
        return
    if not material.disponible:
        print("El material no está disponible.")
        return

    prestamo = PrestamoDB(
        id_usuario=id_usuario,
        id_material=id_material,
        fecha_prestamo=datetime.now(),
        fecha_devolucion=datetime.now() + timedelta(days=14)
    )
    material.disponible = False
    session.add(prestamo)
    session.commit()
    print("Préstamo registrado con éxito.")

def listar_prestamos():
    prestamos = session.query(PrestamoDB).all()
    for p in prestamos:
        print(f"Usuario: {p.id_usuario} - Material: {p.id_material} - Devuelve el {p.fecha_devolucion.date()}")

def main():
    while True:
        print("\n--- Menú Biblioteca ---")
        print("1. Agregar material")
        print("2. Listar materiales")
        print("3. Buscar material")
        print("4. Borrar material")
        print("5. Agregar usuario")
        print("6. Listar usuarios")
        print("7. Agregar préstamo")
        print("8. Listar préstamos")
        print("q. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_material()
        elif opcion == "2":
            listar_materiales()
        elif opcion == "3":
            buscar_material()
        elif opcion == "4":
            borrar_material()
        elif opcion == "5":
            agregar_usuario()
        elif opcion == "6":
            listar_usuarios()
        elif opcion == "7":
            agregar_prestamo()
        elif opcion == "8":
            listar_prestamos()
        elif opcion == "q":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
