import sqlite3
BASE = "inventario.db"

def obtener_conexion():
    return sqlite3.connect(BASE)


def crear_tablas():
    tablas = []
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    for t in tablas:
        cursor.execute(t)


def principal():
    crear_tablas()
    menu = """

    menu de opciones 
    
a) Agregar nuevo producto
b) Editar producto existente
c) Eliminar producto existente
d) Ver listado de productos
e) Buscar descripcion de producto
f) Salir
Elige: """
    opcion = ""
    while opcion != "f":
        opcion = input(menu)
        if opcion == "a":
            producto = input("\nIngresa producto: ")
            # Comprobar si no existe
            posible_descripcion = buscar_descripcion_producto(producto)
            if posible_descripcion:
                print(f"El producto'{producto}' ya existe")
            else:
                descripcion= input("Ingresa la descripcion: ")
                agregar_producto(producto, descripcion)
                print("Producto agregado")

        if opcion == "b":
            producto = input("\nIngresa el producto que quieres editar: ")
            nueva_descripcion = input("Ingresa la descripcion: ")
            editar_producto(producto, nueva_descripcion)
            print("Producto actualizado")

        if opcion == "c":
            producto = input("\nIngresa el producto a eliminar: ")
            eliminar_producto(producto)

        if opcion == "d":
            productos = obtener_productos()
            print("\n========Lista de productos========\n")
            for producto in productos:
                print(producto[0])
        if opcion  == "e":
            producto = input(
                "\nIngresa el producto el cual quieres saber el descripcion: ")
            descripcion = buscar_descripcion_producto(producto)
            if descripcion:
                print(f"La descripción de '{producto}' es:\n{descripcion[0]}")
            else:
                print(f"Producto '{producto}' no encontrada")


def agregar_producto(producto, descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO inventario(producto, descripcion) VALUES (?, ?)"
    cursor.execute(sentencia, [producto, descripcion])
    conexion.commit()


def editar_producto(producto, nueva_descripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "UPDATE inventario SET descripción = ? WHERE producto = ?"
    cursor.execute(sentencia, [nueva_descripcion, producto])
    conexion.commit()


def eliminar_producto(producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM inventario WHERE producto = ?"
    cursor.execute(sentencia, [producto])
    conexion.commit()


def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT producto FROM inventario"
    cursor.execute(consulta)
    return cursor.fetchall()


def buscar_descripcion_producto(producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT descripcion FROM inventario WHERE producto = ?"
    cursor.execute(consulta, [producto])
    return cursor.fetchone()


if __name__ == '__main__':
   principal()