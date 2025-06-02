# main.py
from GestorBiblioteca import GestorBiblioteca

app = GestorBiblioteca()

def menu():
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
        print("9. Información de usuario")
        print("q. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo = input("Tipo (libro/revista/dvd): ").lower()
            titulo = input("Título: ")
            if tipo == "libro":
                autor = input("Autor: ")
                isbn = input("ISBN: ")
                paginas = int(input("Número de páginas: "))
                codigo = app.agregar_material(tipo, titulo, autor=autor, isbn=isbn, numero_paginas=paginas)
            elif tipo == "revista":
                fecha = input("Fecha de publicación: ")
                edicion = input("Número de edición: ")
                codigo = app.agregar_material(tipo, titulo, fecha_publicacion=fecha, numero_edicion=edicion)
            elif tipo == "dvd":
                duracion = int(input("Duración (min): "))
                director = input("Director: ")
                codigo = app.agregar_material(tipo, titulo, duracion=duracion, director=director)
            else:
                print("Tipo no válido.")
                continue
            print(f"Material agregado con código {codigo}")
        elif opcion == "2":
            for m in app.listar_materiales():
                print(f"{m.tipo.capitalize()} - {m.titulo} ({m.codigo_inventario}) - Disponible: {'Sí' if m.disponible else 'No'}")
        elif opcion == "3":
            codigo = input("Código del material: ")
            m = app.buscar_material(codigo)
            if m:
                print(f"{m.tipo.capitalize()} - {m.titulo} - Disponible: {'Sí' if m.disponible else 'No'}")
            else:
                print("Material no encontrado.")
        elif opcion == "4":
            codigo = input("Código del material: ")
            if app.borrar_material(codigo):
                print("Material borrado.")
            else:
                print("No se encontró el material.")
        elif opcion == "5":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            id_usuario = app.agregar_usuario(nombre, apellido)
            print(f"Usuario agregado con ID {id_usuario}")
        elif opcion == "6":
            for u in app.listar_usuarios():
                print(f"{u.nombre} {u.apellido} (ID: {u.id_usuario})")
        elif opcion == "7":
            id_usuario = input("ID del usuario: ")
            id_material = input("Código del material: ")
            if app.agregar_prestamo(id_usuario, id_material):
                print("Préstamo realizado.")
            else:
                print("Error en el préstamo.")
        elif opcion == "8":
            for p in app.listar_prestamos():
                print(f"Usuario: {p.id_usuario} - Material: {p.id_material} - Devuelve el {p.fecha_devolucion.date()}")
        elif opcion == "9":
            id_usuario = input("ID del usuario: ")
            info = app.info_usuario(id_usuario)
            if info:
                print(f"Nombre: {info['nombre']} {info['apellido']}")
                print("Préstamos:")
                for p in info['prestamos']:
                    print(f"  - {p}")
            else:
                print("Usuario no encontrado.")
        elif opcion == "q":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
