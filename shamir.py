from skimage import io
import numpy as np
from Crypto.Cipher import AES
from random import randint
from galois import GF
from bitarray import bitarray
from bitarray.util import ba2int, int2ba
from cbc import cifradocbd, descifradocbc
from conversorImagenes import pasarABits, pasarListaBloqueBytesACadenaBits, \
    pasarCadenaBitsAListaBits, pasarABytes, convertirBytesAMatrizBytes


FF = GF(2**64)


def generarElemento(cadena64Bits):
    """Converts a bitarray of 64 bits into an element of FF"""
    bin = bitarray(cadena64Bits)
    return FF(ba2int(bin))

def generarElementoAleatorio():
    """Returns a random element of FF"""
    return FF(randint(0, 2**64 - 1))

def sacarElementoCuerpoFinito(elemento):
    """Converts an element of FF into a bitarray of 64 bits"""
    aux = int(elemento)
    return int2ba(aux, 64)

def sacarSubloquesEnCuerpoFinito(imagenBits):
    """Input: list of 16 bitarrays of size 8 
    Output: list of two elements of FF"""
    bloqueInicial = []
    cadena = ""
    for i in range (16):
        if(i == 8):
            bloqueInicial.append(generarElemento(cadena))
            cadena = ""
        cadena += imagenBits[i]
    bloqueInicial.append(generarElemento(cadena))
    return bloqueInicial

def generarCoeficiente0(imagenBits):
    cadena = ""
    for i in range(8):
        cadena += imagenBits[i]
    return generarElemento(cadena)

def generarElementosAleatorios(n):
    """Returns a list with n random elements of FF"""
    vectores = []
    for i in range(0, n):
        vectores.append(generarElementoAleatorio())
    return vectores

def elementoNeutroCF():
    """Returns the unit of FF"""
    return generarElemento("00000000000000000000000000000000\
                           00000000000000000000000000000001")


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
    clave = sacarElementoCuerpoFinito(bloque1bits[0]) + \
        sacarElementoCuerpoFinito(bloque1bits[1])
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
        nombre = 'share'
        nombre = nombre + str(i + 1)
        nombre = nombre + '.png'
        io.imsave(nombre, imagenCifradaBytes)

def juntarSecretos(imagenes):
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
    imagenOriginal = descifrar(claveAES, imagenOriginal, 
                               len(imagenes[0]), len(imagenes[0][0]))
    return imagenOriginal

def sacarUltimaFila(imagenbits, width):
    bitsPorFila = len(imagenbits[0]) * 24
    imageninvertida = imagenbits[::-1]
    ultimaFila = imageninvertida[0:bitsPorFila]
    return ultimaFila[::-1]

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
