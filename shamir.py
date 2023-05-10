from skimage import io
import numpy as np
from Crypto.Cipher import AES
from random import randint
from galois import GF
from bitarray import bitarray
from bitarray.util import ba2int, int2ba
from CBC.cbc import cifradocbd, descifradocbc
from ConversorImagen.conversorImagenes import pasarABits, pasarListaBloqueBytesACadenaBits, pasarCadenaBitsAListaBits, \
    pasarABytes, convertirBytesAMatrizBytes

FF = GF(2**64)

"""Recibe una cadena de 64 bits y la introduce en un cuerpo finito de 64 bits"""
def generarElemento(cadena64Bits):##cambiado y se usa

    bin = bitarray(cadena64Bits)

    return FF(ba2int(bin))

"""Devuelve un elemento aleatorio de un cuerpo fintio de 64 bits"""
def generarElementoAleatorio():##cambiado y se usa
    return FF(randint(0, 2**64 - 1))

"""Devuelve un tipo de dato bitarray con el contenido el cuerpo finito en binario de 64 bits, para pasar de 
    bitarray a string usar la funcion to01()"""
def sacarElementoCuerpoFinito(elemento):
    aux = int(elemento)
    return int2ba(aux, 64)

"""Recibe por parámetro una lista de bloques de 8 bits, y devuelve una lista de dos elementos, contienen los dos primeros bloques 
de 64 bits pasados a cuerpo finito"""
def sacarSubloquesEnCuerpoFinito(imagenBits):
    bloqueInicial = []
    cadena = ""
    for i in range (16):
        if(i == 8):
            bloqueInicial.append(generarElemento(cadena))
            cadena = ""
        cadena += imagenBits[i]

    bloqueInicial.append(generarElemento(cadena))


    return bloqueInicial

def generarCoeficiente0(imagenBits):##no se usa
    cadena = ""
    for i in range(8):
        cadena += imagenBits[i]

    return generarElemento(cadena)

"""Se genera un array con n elementos aleatorios de un cuerpo finito de 64 bits"""
def generarElementosAleatorios(n):
    vectores = []
    for i in range(0, n):
        vectores.append(generarElementoAleatorio())

    return vectores

"""devuelve el elemento neutro del campo finito de 64 bits"""
def elementoNeutroCF():
    return generarElemento("0000000000000000000000000000000000000000000000000000000000000001")

"""
    Imagenes = es una lista de cuerpos finitos, los cuales son todas las imagenes de uno de los dos polimios de shamir (cada cuerpo finito es el valor de aplicar un VI en el polinomio),
    debe de contener tantos elementos como usuarios se necesiten para recuperar la imagen original.
"""
def sacarClave(imagenes,vectoresIncializacion): #Hay que lanzar una excepcion que salte si el sistema no tiene solucion (no se han reunido los suficientes usuarios)
    A = []
    B = []

    for i in range(len(vectoresIncializacion)):
        fila = []
        for j in range(len(vectoresIncializacion)):
            fila.append(vectoresIncializacion[i]**j)

        A.append(fila)

    A = np.array(A)

    A = FF(A)

    for i in range(len(imagenes)):
        fila = []
        fila.append(imagenes[i])
        B.append(fila)

    B = np.array(B)
    B = FF(B)

    return np.linalg.solve(A,B)[0]

def generarImagenesPolinomio(coeficientes, vectoresInicializacion, bloqueInicial):
    imagenes = []

    for i in range(len(vectoresInicializacion)):
        imagen = bloqueInicial
        for j in range(len(coeficientes)):
            imagen = imagen + (coeficientes[j] * (vectoresInicializacion[i]**(j+1)))

        imagenes.append(imagen)

    return imagenes



def generarSecretos(img, k, n):

    imagenBits = pasarABits(img)
    bloque1bits = sacarSubloquesEnCuerpoFinito(imagenBits)
    vectoresInicializacion = generarElementosAleatorios(n)
    coeficientesP1 = generarElementosAleatorios(k - 1)
    coeficientesP2 = generarElementosAleatorios(k - 1)
    imagenesP1 = generarImagenesPolinomio(coeficientesP1, vectoresInicializacion, bloque1bits[0])
    imagenesP2 = generarImagenesPolinomio(coeficientesP2, vectoresInicializacion, bloque1bits[1])
    p1 = sacarElementoCuerpoFinito(imagenesP1[0])
    p2 = sacarElementoCuerpoFinito(imagenesP2[0])

    clave = sacarElementoCuerpoFinito(bloque1bits[0]) + sacarElementoCuerpoFinito(bloque1bits[1])

    imgb = pasarListaBloqueBytesACadenaBits(imagenBits)
    cont = 0
    while (len(imgb) % 128 != 0):
        cont = cont + 1
        imgb = imgb + '0'

    for i in range(len(imagenesP1)):
        p = sacarElementoCuerpoFinito(imagenesP1[i]) + sacarElementoCuerpoFinito(imagenesP2[i])
        imagenCifradaBits = cifrar(p,imgb,clave, len(img) + 1, len(img[0]),cont)
        vi = sacarElementoCuerpoFinito(vectoresInicializacion[i])
        imagenCifradaBits = imagenCifradaBits + vi
        imagenCifradaBits = pasarCadenaBitsAListaBits(imagenCifradaBits.to01())
        imagenCifradaBytes = pasarABytes(imagenCifradaBits, len(img) + 1, len(img[0]))
        nombre = 'imagenes/resultadocifrado/imagencifrada'
        nombre = nombre + str(i + 1)
        nombre = nombre + '.png'
        io.imsave(nombre, imagenCifradaBytes)



def juntarSecretos(imagenes):#excepcion de compropbar que se pasen el minimo de secretos (imagenes necesarias), y que cada imagen tenga su vi* correspondiente

    imagenesBits = []
    imagenesPolinomio1 = []
    imagenesPolinomio2 = []
    vectoresIdentificacion = []

    bitsPorFila = len(imagenes[0][0]) * 24
    for i in range(len(imagenes)):
        imagen = pasarABits(imagenes[i])
        imagen = pasarListaBloqueBytesACadenaBits(imagen)
        imagenInvertida = imagen[::-1]
        ultimaFila = imagenInvertida[0:bitsPorFila]
        ultimaFila = ultimaFila[::-1]

        ##ultimaFila = sacarUltimaFila(imagen, len(imagenes[i][0]))
        longitudImagenOriginal = len(imagen) - len(ultimaFila)
        numeroBitsAdicionales = 0

        while(longitudImagenOriginal % 128 != 0):
            numeroBitsAdicionales = numeroBitsAdicionales + 1
            longitudImagenOriginal = longitudImagenOriginal + 1

        vectorIdentificacion = ultimaFila[numeroBitsAdicionales:numeroBitsAdicionales+64]
        vectoresIdentificacion.append(generarElemento(vectorIdentificacion))
        imagen = imagen[0:longitudImagenOriginal]
        imagen = pasarCadenaBitsAListaBits(imagen)
        imagenesBits.append(imagen)



    for i in range(len(imagenesBits)):
        cabeceraImagen = sacarSubloquesEnCuerpoFinito(imagenesBits[i])
        imagenesPolinomio1.append(cabeceraImagen[0])
        imagenesPolinomio2.append(cabeceraImagen[1])

    k1 = sacarClave(imagenesPolinomio1, vectoresIdentificacion)
    k2 = sacarClave(imagenesPolinomio2, vectoresIdentificacion)

    claveAES = sacarElementoCuerpoFinito(k1) + sacarElementoCuerpoFinito(k2)

    imagenOriginal = pasarListaBloqueBytesACadenaBits(imagenesBits[0])

    imagenOriginal = descifrar(claveAES, imagenOriginal,len(imagenes[0]), len(imagenes[0][0]))

    #imagenOriginal = descifradocbc(imagenOriginal, claveAES.to01())

    #imagenOriginal = pasarCadenaBitsAListaBits(imagenOriginal)
    #imagenOriginal = pasarABytes(imagenOriginal, len(imagenes[0]), len(imagenes[0][0]))

    return imagenOriginal

def sacarUltimaFila(imagenbits, width):
    bitsPorFila = len(imagenbits[0]) * 24 #cuentas el numero de pixeles por fila y lo multiplicas por 24 que son los bits que ocupa un pixel
    imageninvertida = imagenbits[::-1]
    ultimaFila = imageninvertida[0:bitsPorFila]

    return ultimaFila[::-1]


"Se pasa la imagen en un array de bytes y el vi en binario"
def cifrar(vi,imagen,clave, high, width, padding):
    vi = bitarray(vi)
    clave = bitarray(clave)
    vi = vi.tobytes()
    clave = clave.tobytes()
    img = bitarray(imagen)
    img = img.tobytes()
    cipher = AES.new(clave, AES.MODE_CBC, vi)

    imagencifrada = cipher.encrypt(img[16:])
    imagencifrada = img[0:16] + imagencifrada

    imagencifrada = convertirBytesAMatrizBytes(imagencifrada, high, width)

    imagencifrada = pasarABits(imagencifrada)
    imagencifrada = pasarListaBloqueBytesACadenaBits(imagencifrada)

    bitsPorFila = width * 24
    imagenInvertida = imagencifrada[::-1]
    ultimaFila = imagenInvertida[0:bitsPorFila]
    ultimaFila = ultimaFila[::-1]
    imagencifrada = imagencifrada[0:len(imagencifrada)-bitsPorFila]
    ultimaFila = ultimaFila[0:padding]
    imagencifrada = imagencifrada + ultimaFila

    return bitarray(imagencifrada)


def descifrar(clave, imagencifrada, high, width):
    img = bitarray(imagencifrada)
    img = img.tobytes()
    vi = img[0:16]
    clave = clave.tobytes()
    cipher = AES.new(clave, AES.MODE_CBC, vi)

    imagen = cipher.decrypt(img[16:])

    imagen = clave + imagen

    imagen = convertirBytesAMatrizBytes(imagen, high-1, width)

    return imagen








