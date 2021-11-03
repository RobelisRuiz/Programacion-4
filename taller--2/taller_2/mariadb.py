import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
engine = sqlalchemy.create_engine(
    "mariadb+mariadbconnector://root:2280@127.0.0.1:3306/slang")

base_datos = "diccionario.db"
datos=""
def obtener():
    return datos (base_datos)
def creacion_tablas():
    tabla = [ ]
    conectar= obtener()
    cursor = conectar.cursor()
    for t in tabla:
        cursor.execute(t)
def menu ():
    creacion_tablas()
    opcion = """
    
        BIENVENIDO 

      ---- MENU ----

a) Agregar nueva palabra
b) Editar palabra existente
c) Eliminar palabra existente
d) Ver listado de palabras
e) Buscar significado de palabra
f) Salir
Elige: """
    e = ""
    while e != "f":
        e = input(opcion)
        if e == "a":
            p = input("Escriba la palabra: ")
            significado2 = buscar_significado(p)
            if significado2:
                print(f"La palabra '{p}' ya existe")
            else:
                significado = input("Escriba el significado: ")
                agregar_palabra(p, significado)
                print("La palabra fue agregada")
        if e == "b":
            p = input("Escriba la palabra que quieres editar: ")
            nuevo = input("Escriba el nuevo significado: ")
            editar_palabra(p, nuevo)
            print("La palabra fue actualizada")
        if e == "c":
            p = input("Escriba la palabra a eliminar: ")
            eliminar_palabra(p)
        if e == "d":
            pala = obtener_palabras()
            print("---  Lista de palabras  ---")
            for p in pala:
                print(p[0])
        if e == "e":
            p = input(
                "Escriba la palabra de la cual quiere saber el significado: ")
            significado = buscar_significado(p)
            if significado:
                print(f"El significado de '{p}' es:\n{significado[0]}")
            else:
                print(f" La palabra '{p}' no fue encontrada")
def agregar_palabra(p, significado):
    conexion = obtener()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario(palabra, significado) VALUES (?, ?)"
    cursor.execute(sentencia, [p, significado])
    conexion.commit()
def editar_palabra(p, nuevo_significado):
    conexion = obtener()
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = ? WHERE palabra = ?"
    cursor.execute(sentencia, [nuevo_significado, p])
    conexion.commit()
def eliminar_palabra(p):
    conexion = obtener()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = ?"
    cursor.execute(sentencia, [p])
    conexion.commit()
def obtener_palabras():
    conexion = obtener()
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    return cursor.fetchall()
def buscar_significado(p):
    conexion = obtener()
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = ?"
    cursor.execute(consulta, [p])
    return cursor.fetchone()
if __name__ == '__main__':
    menu()