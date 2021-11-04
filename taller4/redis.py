import redis
Pc = "Palabra"
Dc = "Defincion"
r = redis.Redis(host='127.0.0.1', port=6379)
r.set("id", -1)
print(r.keys())

def VerificarPalabraExistente(Palabra):
    CantPalabras = r.llen(Pc)
    PalabraExistente = False
    for i in range(CantPalabras):
        PalabraActual = r.lindex(Pc, i).decode('utf-8')
        if(PalabraActual == Palabra):
            PalabraExistente = True
            break
    return PalabraExistente


def AgregarPalabra(Palabra,Definicion):
    r.incr("id")
    r.rpush(Pc, Palabra)
    r.rpush(Dc, Definicion)
    print("\n ¡Palabra agregada correctamente!")


def Actualizarpalabra(AntiguaPalabra, Np, NuevaDefinicion):
    CantPalabras = r.llen(Pc)
    for i in range(CantPalabras):
        PalabraActual = r.lindex(Pc, i).decode('utf-8')
        if(PalabraActual == AntiguaPalabra):
            r.lset(Pc, i, Np)
            r.lset(Dc, i, NuevaDefinicion)
            break

    print("\n¡Palabra" + AntiguaPalabra+ "actualizada!")


def BorrarPalabra(Palabra):
    s = r.llen(Pc)
    for i in range(s):
        Pa = r.lindex(Pc, i).decode('utf-8')
        DefinicionActual = r.lindex(Dc, i).decode('utf-8')
        if(Pc == Palabra):
            r.lrem(Pc, i, Pa)
            r.lrem(Dc, i, DefinicionActual)
            break
    print("\n ¡Palabra eliminada!")


def MostrarPalabras():
    C = r.llen(Pc)
    for i in range(C):
        print(f'{i + 1}. Palabra: {r.lindex(Pc, i).decode("utf-8")} \n Definicion: {r.lindex(Dc, i).decode("utf-8")}')


while True:

    
    print("\n**** MENU DE OPCIONES ****")
    print("\nIngrese opción: \n")

    o = int(input(" 1). Agregar nueva palabra \n 2). Editar palabra existente \n 3). Eliminar palabra existente \n 4). Ver listado de palabras \n 5). Buscar significado de palabra \n 6). Salir \n"))

    if(o == 1):
        
        Entrada = input("\nIngrese palabra a agregar:\n")
        EntradaDefinicion = input(
            "\nIngrese definición: \n")
        if(len(Entrada) and len(EntradaDefinicion)):
            if(VerificarPalabraExistente(Entrada)):
                print("\nPalabra existente, ¡Por favor! ingrese otra palabra:")
            else:
                AgregarPalabra(Entrada, EntradaDefinicion)
        else:
            print("\n¡Por favor! llene los campos de información:")

    elif(o == 2):
        Entrada = input("\nIngrese palabra a modificar: \n")

        NP = input("\nIngrese el nuevo valor de esta palabra:\n")

        ND  = input(
            "\nIngrese nueva definición de la palabra:\n")

        if(len(NP) and len(ND) and len(Entrada)):
            if(VerificarPalabraExistente(Entrada)):
                Actualizarpalabra(Entrada, NP, ND)
            else:
                print("\n¡Esta palabra no existe!, vuelva a intentarlo")

        else:
            print("\n¡Por favor! llene los campos de información:")

    elif(o == 3):
        Entrada = input("\nIngrese palabra a eliminar:")

        if(len(Entrada)):
            if(VerificarPalabraExistente(Entrada)):
                BorrarPalabra(Entrada)

            else:
                print("\n¡Esta palabra no existe!")

        else:
            print("\n¡Por favor! llene los campos de información:")

    elif(o == 4):
        MostrarPalabras()
    elif(o  == 5):
        Entrada = input("\nIngrese palabra que desea ver su significado:\n")
        if(len(Entrada)):
            if(VerificarPalabraExistente(Entrada)):
                c = r.llen(Pc)
                for i in range(c):
                    Pa = r.lindex(Pc, i).decode('utf-8')
                    if(Pa== Entrada):
                        print(
                            f'La definicion es: {r.lindex(Dc, i).decode("utf-8")}')
                        break

            else:
                print("\n¡Esta palabra no existe!")

        else:
            print("\n¡Por favor! llene los campos de información:")

    elif(o  == 6):
        break

    else:
        print("\nIngrese una opcion valida:\n")