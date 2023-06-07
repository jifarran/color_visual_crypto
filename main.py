# coding=utf-8
from skimage import io
from time import time
from shamir import generarSecretos, juntarSecretos


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
    print("\t\nInfo: This program only works with PPM and PNG images")
    print("\tColor image secret sharing\n")
    print("\t\t1. Generate the shared images")
    print("\t\t2. Reconstruct the original shared image")
    print("\t\t0. Exit")
    opcion = input("\n\tSelect an option: ")

    return int(opcion)

def dividirImagenEnSecretos():
    while True:
        try:
            n = int(input("Introduce the number of shares: "))
            break
        except ValueError:
            print("The number must be integer, try again")

    while True:
        try:
            k = int(input("Introduce the threshold of the secret sharing: "))
            break
        except ValueError:
            print("The number must be integer, try again")

    while True:
        try:
            ruta = input("Introduce the path to the original image: ")
            imagen = io.imread(ruta)
            break
        except:
            print("The path is not valid, try again")

    if(formatoValido(ruta) == False):
        print("The image format is not valid, it should be PPM or PNG")
    else:
        print("Generating the shares, it may take some minutes...")
        tiempo_inicial = time()
        generarSecretos(imagen, k, n)
        tiempo_final = time()
        tiempo = tiempo_final - tiempo_inicial
        print("The shares of the images are saved")
        print("The computation time has been", tiempo, "seconds")


def descifrarImagen():
    while True:
        try:
            k = int(input("Introduce the threshold: "))
            break
        except ValueError:
            print("The number must be integer, try again")

    imagenes = []

    for i in range(k):
        while True:
            try:
                ruta=input(f"Introduce the path to the share {i + 1} : ")
                imagen = io.imread(ruta)
                break
            except:
                print("The path is not valid, try again")
        imagenes.append(imagen)

    print("Reconstructing the original image, it may take some minutes...")
    tiempo_inicial = time()
    imagenOriginal = juntarSecretos(imagenes)
    tiempo_final = time()
    tiempo = tiempo_final - tiempo_inicial
    print("The original image has been reconstructed")
    print("The computation time has been", tiempo, "seconds")
    io.imsave('original.png', imagenOriginal)


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
            print("Thank you for using this program")
        else:
            print("Not valid option: it must be 1, 2, or 0")
