#robelis ruiz 8-976-2485
import sqlite3
Base_ = "diccionario.db"


def obtener_conexion():
    return sqlite3.connect(Base_)


def crear_tablas():
    tablas = [ ]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    for t in tablas:
        cursor.execute(t)


def principal():
    crear_tablas()
    menu = """
    
    M E N U   D E   P R O D U C T O S

a) Agregar nueva producto
b) Editar producto existente
c) Eliminar producto existente
d) Ver listado de productos
e) Buscar significado de productos
f) Salir
Elige: """
    e = ""
    while e != "f":
        e = input(menu)
        if e == "a":
            p = input("Ingresa la producto: ")
           
            po = buscar_significado_palabra(p)
            if po:
                print(f"La productos '{p}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(p, significado)
                print("Producto agregada")
        if e == "b":
            p = input("Ingresa la producto que quieres editar: ")
            nuevo = input("Ingresa el nuevo significado: ")
            editar_palabra(p, nuevo)
            print("Producto actualizada")
        if e == "c":
            p = input("Ingresa el producto a eliminar: ")
            eliminar_palabra(p)
        if e == "d":
            palabras = obtener_palabras()
            print(" LISTA DE PRODUCTOS ")
            for p in palabras:
              
                print(p[0])
        if e == "e":
            p = input(
                "Ingresa la producto de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(p)
            if significado:
                print(f"El significado de '{p}' es:\n{significado[0]}")
            else:
                print(f"Producto '{p}' no encontrada")


def agregar_palabra(palabra, significado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario(palabra, significado) VALUES (?, ?)"
    cursor.execute(sentencia, [palabra, significado])
    conexion.commit()


def editar_palabra(palabra, nuevo_significado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = ? WHERE palabra = ?"
    cursor.execute(sentencia, [nuevo_significado, palabra])
    conexion.commit()


def eliminar_palabra(palabra):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = ?"
    cursor.execute(sentencia, [palabra])
    conexion.commit()


def obtener_palabras():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    return cursor.fetchall()


def buscar_significado_palabra(palabra):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = ?"
    cursor.execute(consulta, [palabra])
    return cursor.fetchone()


if __name__ == '__main__':
    principal()