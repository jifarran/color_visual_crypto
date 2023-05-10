from bitarray.util import ba2int
from bitarray import bitarray
from aes128 import aes128, Descifrar
from Crypto.Cipher import AES
from binascii import a2b_qp, b2a_qp

from ConversorImagen.conversorImagenes import pasarCadenaBitsAListaBits, pasarABytes

"""
    Este subprograma recibe por parametros:
    -imagenesPolinomios = Son los primeros 128 bits 
     de la imagen cifrada formados por el resultado de 
     sustituir en p1 y p2 el vector de inicializacion de un usuario
     esta en formato bitarray. 
    -imagen = es un string con la imagen en binario
    -clave = es un string con la clave en binario
    
    Autor: David Cerezo Martínez
"""
def cifradocbd(imagenesPolinomios, imagen, clave):
    imagencifrada = imagenesPolinomios


    while(len(imagencifrada) != len(imagen)):
        bloque = ''
        l = len(imagencifrada)
        bloque = imagen[l:l + 128]
        if(l == 128):
            xor = bitarray(imagenesPolinomios) ^ bitarray(bloque)

        else:
            xor = bitarray(bloquecifrado) ^ bitarray(bloque)

        bloquecifrado = aes128(xor.to01(), clave)

        imagencifrada = imagencifrada + bloquecifrado


    return imagencifrada

def descifradocbc(imagenCifrada, clave):
    imageninvertida = imagenCifrada[::-1]
    bloque1 = ''
    bloque2 = ''
    imagen = ''

    while(len(imagen) != (len(imagenCifrada) - 128)):
        l = len(imagen)
        bloque1 = imageninvertida[l:l+128]
        bloque2 = imageninvertida[l+128:l+256]
        bloque1 = Descifrar(bloque1[::-1], clave)
        bloque1 = bitarray(bloque1) ^ bitarray(bloque2[::-1])
        imagen = imagen + bloque1.to01()[::-1]

    imagen = imagen[::-1]
    imagen = clave + imagen

    return imagen




