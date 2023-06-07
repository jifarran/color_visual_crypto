import numpy as np


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

def pasarListaBloqueBytesACadenaBits(imagen):
    img = ''
    for i in imagen:
        img = img + i
    return img
