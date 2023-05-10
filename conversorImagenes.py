import numpy as np

"""Coge la matriz de bytes y la convierte en bits, lo que devuelve
es una lista en la que cada elemento es un bloque de 8 bits"""
def pasarABits(img):
    lista = []

    for i in img:
        for j in i:
            for k in j:
                byte = format(k, '08b')
                lista.append(byte)
    return lista


def pasarListaACadena(Lista):
    cadena = ""
    for i in Lista:
        cadena += str(i)

    return cadena


def pasarABytes(cadenaBits, high, width):
    img = np.zeros(shape=(high, width, 3), dtype=np.uint8)
    posicion = 0

    for i in img:
        for j in i:
            for k in range(0, 3):
                if(posicion < len(cadenaBits)):
                    j[k] = int(str(cadenaBits[posicion]), 2)
                    posicion = posicion + 1
                else:
                    break
    return img

def convertirBytesAMatrizBytes(imagen, high, width):
    img = np.zeros(shape=(high, width, 3), dtype=np.uint8)
    posicion = 0

    for i in img:
        for j in i:
            for k in range(0,3):
                if(posicion < len(imagen)):
                    j[k] = imagen[posicion]
                    posicion = posicion + 1
                else:
                    break
    return img

""" Transforma una cadena de caracteres de bits en una lista de cadenas de ocho bits tal que así:
    Entrada:
        '01010101010101010101010101010101'
    Salida:
        [['01010101'],['01010101'],['01010101'],['01010101']]
"""

def pasarCadenaBitsAListaBits(cadenabits):
    lista = []
    aux = ''
    posicion = 0

    for i in range(len(cadenabits)):
        aux = aux + cadenabits[i]
        if posicion == 7:
            lista.append(aux)
            posicion = 0
            aux = ''
        else:
            posicion = posicion + 1

    return lista
""" Hace lo inverso a la fución pasarCadenaBits, transforma una lista de cadenas se 8 bits en una cadena de bits:
    Entrada:
        [['01010101'],['01010101'],['01010101'],['01010101']]
    Salida:
        '01010101010101010101010101010101'
        
"""
def pasarListaBloqueBytesACadenaBits(imagen):
    img = ''

    for i in imagen:
        img = img + i

    return img

