# coding=utf-8
from skimage import io
from time import time
from Shamir.shamir import generarSecretos, juntarSecretos

def formatoValido(ruta):
    ruta = ruta[::-1]
    extension = ''

    for i in ruta:
        if (i == '.'):
            break
        extension = extension + i

    if (extension == 'gnp' or extension == 'mpp'):
        return True
    else:
        return False

def menuPrincipal():
    print("\t\nInfo: Este programa solo es capaz de cifrar imágenes en formato ppm y png")
    print("\tCompartición de secretos mediante imágenes\n")
    print("\t\t1. Dividir una Imágen en Secretos")
    print("\t\t2. Juntar Imágenes para Obtener la Original")
    print("\t\t0. Salir")
    opcion = input("\n\tSeleccione una opción: ")

    return int(opcion)

def dividirImagenEnSecretos():
    while True:
        try:
            n = int(input("Introduzca el Número de sombras de la Imágen que se desea que se obtengan a partir de la original: "))
            break
        except ValueError:
            print("Debe introducir un número entero")

    while True:
        try:
            k = int(input("Introduzca el mínimo de sombras necesarias para posteriormente obtener la imágen original: "))
            break
        except ValueError:
            print("Debe introducir un número entero")

    while True:
        try:
            ruta = input("Introduzca la ruta exacta de la imágen: ")
            imagen = io.imread(ruta)
            break
        except:
            print("La ruta introducida no contiene una imágen, intentelo otra vez")

    if(formatoValido(ruta) == False):
        print("La imágen introducida no es un formato válido, solo se admiten formatos png y ppm")
    else:
        print("Generando sombras de la imágen, este proceso tardará varios minutos ....")
        tiempo_inicial = time()
        generarSecretos(imagen, k, n)
        tiempo_final = time()
        tiempo = tiempo_final - tiempo_inicial
        print("Se han generado las sombras de la imágen en la carpeta resultadocifrado")
        print("El tiempo de cifrado ha sido de ", tiempo, " segundos")


def descifrarImagen():
    while True:
        try:
            k = int(input("Introduzca el número de imágenes mínimas necesarias  para obtener la original: "))
            break
        except ValueError:
            print("Debe introducir un número entero")

    imagenes = []

    for i in range(k):
        while True:
            try:
                ruta=input(f"Introduzca la ruta exacta de la imagen {i + 1} : ")
                imagen = io.imread(ruta)
                break
            except:
                print("La ruta introduccida no contiene una imágen")
        imagenes.append(imagen)

    print("Generando imágen original, esto tardará varios minutos...")
    tiempo_inicial = time()
    imagenOriginal = juntarSecretos(imagenes)
    tiempo_final = time()
    tiempo = tiempo_final - tiempo_inicial
    print("Se ha recuperado la imágen original, será guardada en la carpeta resultadodescifrado")
    print("El tiempo de descifrado ha sido de ", tiempo, " segundos")
    io.imsave('imagenes/resultadodescifrado/imagenDescifrada.png',imagenOriginal)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    opcion = -1

    while(opcion != 0):
        opcion = menuPrincipal()
        if opcion == 1:
            dividirImagenEnSecretos()
        elif opcion == 2:
            descifrarImagen()
        elif opcion == 0:
            print("Gracias por usar la aplicación")
        else:
            print("Opción erronea selecion 1,2 o 0.")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
