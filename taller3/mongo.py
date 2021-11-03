import collections
import pymongo

from pymongo import MongoClient

cluster = MongoClient(
    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000L")
db = cluster["MongoDB"]
collection = db["Diccionario Slang"]


def Verificar(Palabra):
    v = collection.find_one(
        {"palabra": Palabra})
    if(v == None):
        return False
    else:
        return True


def Actualizar(Antigua, NuevaP, NuevaD):
    collection.update_one({"Palabra": Antigua}, {"$set": {
        "Palabra": NuevaP,
        "Definicion": NuevaD
    }})


def Borrar(Palabra):
    collection.delete_one({"Palabra": Palabra})


def Mostrar():
    palabras = collection.find()
    i = 0
    for row in palabras:
        i += 1
        print(
            f'{i}. Palabra: {row["palabra"]} Definicion: {row["definicion"]}')


while True:

    
    print("\n  Menu de opciones \n")

    o = int(input(" 1). Agregar nueva palabra \n 2). Editar palabra existente \n 3). Eliminar palabra existente \n 4). Ver listado de palabras \n 5). Buscar significado de palabra \n 6). Salir \n"))

    if(o == 1):
       
        Entrada = input("\nIngrese palabra a agregar:\n")
        EntradaD = input("\nIngrese definición:\n")
        if(len(Entrada) and len(EntradaD)):

            if(Verificar(Entrada)):
                print("\nEsta palabra ya existe ¡por favor! agregue otra palabra")
            else:
                collection.insert_one({
                    "palabra": Entrada,
                    "definicion": EntradaD
                })
        else:
            print("\n Por favor llenar ambos campos de informacion")

    elif(o == 2):
        Entrada = input("\nIngrese la palabra que desea modificar: \n")

        N = input("\nIngrese el nuevo valor de esta palabra: \n")

        Nd= input("\nIngrese la nueva definicion de la palabra: \n")

        if(len(N) and len(Nd) and len(Entrada)):
            if(Verificar(Entrada)):
                Actualizar(Entrada, N, Nd )
            else:
                print("\n La palabra no existe!, vuelva a intentarlo")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(o == 3):
        Entrada = input("\n Ingrese la palabra que desea eliminar \n")

        if(len(Entrada)):
            if(Verificar(Entrada)):
                Borrar(Entrada)

            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(o == 4):
        Mostrar()
    elif(o == 5):
        Entrada = input("\nIngrese la palabra que desea ver su significado \n")
        if(len(Entrada)):
            if(Verificar(Entrada)):
                getPalabra = collection.find_one({"palabra": Entrada})
                print(f'La definicion es: {getPalabra["definicion"]}')
            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(o == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")