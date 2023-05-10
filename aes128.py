# ALGORITMO DE CIFRADO AES128

from math import ceil
from copy import deepcopy

"""
    Bienvenido a la librería de cifrado y descifrado de AES 128. Esta librería cuenta con dos
    funciones accesibles para los usuarios, una de cifrado basado en el cifrado simétrico
    AES 128 y su correspondiente descifrado; ambas funciones están implementadas en los programas
    aes12() y Descifrado() respectivamente. 

    Autores: 
        Ignacio Aranguren
        Guillermo Centeno
        David Cerezo
        Carlos Cubo
"""


def aes128(mensaje, clave):
    """
    Función de cifrado:
    -------------------------------------------------------------------------------------
    -Datos de entrada: texto asici con el mensaje y con la clave

    -Funcionamiento: Función principal de cifrado de datos. El usuario inserta un mensaje
    y una clave para cifrar, ambos en texto plano.  Se realiza el proceso de cifrado AES
    128 según su estándar.Finalmente se devuelve al usuario el mensaje cifrado en formato
    hexadecimal
    .
    -Datos de salida: texto en hexadecimal con el mensaje cifrado
    -------------------------------------------------------------------------------------
"""
    matrizClave = [[0] * 4 for i in range(4)]
    matrizAux = [[0] * 4 for i in range(4)]
    menCifrado = ''

    _getClave(matrizClave, clave)
    matrizAux = deepcopy(matrizClave)

    posbloque = 0

    bloque = [[0] * 4 for i in range(4)]
    matrizClave = deepcopy(matrizAux)
    mensajeEnBytes = pasarAbytes(mensaje)

    for j in range(4):
        for i in range(4):
            bloque[i][j] = mensajeEnBytes[posbloque]
            posbloque = posbloque + 1

    # metodo cifrado

    # XOR bloque - clave
    _AddRoundKey(bloque, matrizClave)
    # Vueltas del cifrado
    for vuelta in range(9):
        _SubBytes(bloque)
        _ShiftRows(bloque)
        bloque = _MixColumns(bloque)
        matrizClave = _ExpansionK(matrizClave, vuelta)
        _AddRoundKey(bloque, matrizClave)

    # Ultima vuelta del cifrado
    _SubBytes(bloque)
    _ShiftRows(bloque)
    matrizClave = _ExpansionK(matrizClave, 9)
    _AddRoundKey(bloque, matrizClave)

    for columna in range(4):
        for fila in range(4):
            valor = hex(bloque[fila][columna])[2:]
            if len(valor) < 2:
                valor = '0' + valor
            menCifrado = menCifrado + valor

    menCifrado = pasarHexAbits(menCifrado)
    #print("\nSu mensaje cifrado es: ")
    #print(menCifrado) Esta en hexadecimal, pasar a binario

    return menCifrado


def Descifrar(mensaje, clave):
    """
    Función de descifrado:
    ------------------------------------------------------------------------------------
    -Datos de entrada: Texto en hexadecimal con el mensaje cifrado y clave en ascii

    -Funcionamiento: Función principal de descifrado de datos (funcionamiento inverso del
     descifrado). El usuario inserta un mensaje y una clave para cifrar, ambos en texto
    plano.  Se realiza el proceso de descifrado AES 128 según su estándar.Finalmente se
    devuelve al usuario el mensaje cifrado en formato hexadecimal.

    -Datos de salida: Texto en ascii descifrado

    ------------------------------------------------------------------------------------
"""

    matrizClave = [[0] * 4 for i in range(4)]
    menCifrado = ''
    claves = [[[0] * 4 for i in range(4)]] * 11

    _getClave(matrizClave, clave)

    # Generacion claves
    claves[0] = deepcopy(matrizClave)
    for x in range(1, 11):
        claves[x] = _ExpansionK(claves[x - 1], x - 1)

    posbloque = 0

    bloque = [[0] * 4 for i in range(4)]
    mensajeBytes = pasarAbytes(mensaje)
    for j in range(4):
        for i in range(4):
            bloque[i][j] = mensajeBytes[posbloque]
            posbloque = posbloque + 1

    # metodo cifrado

    _AddRoundKey(bloque, claves[10])
    _InvShiftRows(bloque)
    _InvSubBytes(bloque)

    vuelta = 9
    for i in range(9):
        _AddRoundKey(bloque, claves[vuelta])
        bloque = _InvMixColumns(bloque)
        _InvShiftRows(bloque)
        _InvSubBytes(bloque)
        vuelta = vuelta - 1

    _AddRoundKey(bloque, claves[0])

    for columna in range(4):
        for fila in range(4):
            valor = format(bloque[fila][columna], '08b')
            menCifrado = menCifrado + valor


    return menCifrado

def _getClave(mclave, textclave):
    """
    Función_getClave():
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    pos = 0
    claveBytes = pasarAbytes(textclave)

    for j in range(4):
        for i in range(4):
            mclave[i][j] = claveBytes[pos]
            pos = pos + 1


def _SubBytes(estado):
    """
    Funcion SubBytes
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------

"""
    matrizSubBytes = [[' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],
                      ['0', 0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB,
                       0x76],
                      ['1', 0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72,
                       0xC0],
                      ['2', 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31,
                       0x15],
                      ['3', 0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2,
                       0x75],
                      ['4', 0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F,
                       0x84],
                      ['5', 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58,
                       0xCF],
                      ['6', 0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F,
                       0xA8],
                      ['7', 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3,
                       0xD2],
                      ['8', 0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19,
                       0x73],
                      ['9', 0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B,
                       0xDB],
                      ['A', 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4,
                       0x79],
                      ['B', 0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE,
                       0x08],
                      ['C', 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B,
                       0x8A],
                      ['D', 0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D,
                       0x9E],
                      ['E', 0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28,
                       0xDF],
                      ['F', 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB,
                       0x16]]

    for fila in range(4):
        for columna in range(4):
            valor = hex(estado[fila][columna])[2:]
            if len(valor) < 2:
                valor = '0' + valor
            valor = valor.upper()
            for car1 in range(17):
                if valor[0] == matrizSubBytes[car1][0]:
                    filBusq = car1
            for car2 in range(17):
                if valor[1] == matrizSubBytes[0][car2]:
                    colBusq = car2
            estado[fila][columna] = matrizSubBytes[filBusq][colBusq]


def _ShiftRows(estado):
    """
    Funcion ShiftRows
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""

    for fila in range(1, 4):
        for i in range(1, fila + 1):
            primero = estado[fila][0]
            for x in range(3):
                estado[fila][x] = estado[fila][x + 1]
            estado[fila][3] = primero


def _MixColumns(estado):
    """
    Funcion MixColumns
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    gf = [[0x02, 0x03, 0x01, 0x01],
          [0x01, 0x02, 0x03, 0x01],
          [0x01, 0x01, 0x02, 0x03],
          [0x03, 0x01, 0x01, 0x02]]

    resultado = [[0] * 4 for i in range(4)]

    for columna in range(4):
        resultado[0][columna] = _Galois(estado[0][columna], gf[0][0]) ^ _Galois(estado[1][columna], gf[0][1]) ^ _Galois(
            estado[2][columna], gf[0][2]) ^ _Galois(estado[3][columna], gf[0][3])
        resultado[1][columna] = _Galois(estado[0][columna], gf[1][0]) ^ _Galois(estado[1][columna], gf[1][1]) ^ _Galois(
            estado[2][columna], gf[1][2]) ^ _Galois(estado[3][columna], gf[1][3])
        resultado[2][columna] = _Galois(estado[0][columna], gf[2][0]) ^ _Galois(estado[1][columna], gf[2][1]) ^ _Galois(
            estado[2][columna], gf[2][2]) ^ _Galois(estado[3][columna], gf[2][3])
        resultado[3][columna] = _Galois(estado[0][columna], gf[3][0]) ^ _Galois(estado[1][columna], gf[3][1]) ^ _Galois(
            estado[2][columna], gf[3][2]) ^ _Galois(estado[3][columna], gf[3][3])

    return resultado


def _Galois(celEstado, celGalois):
    """
    Funcion para multiplicar en un cuerpo finito
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    result = 0
    ultbit = 0
    while (celGalois != 0):
        if celGalois & 1 == 1:
            result = result ^ celEstado
        ultbit = celEstado & 128
        # xTime()
        celEstado = celEstado << 1
        if ultbit == 128:
            celEstado = celEstado ^ 0x11b
        celGalois = celGalois >> 1
    return result


def _AddRoundKey(estado, clave):
    """
    Funcion AddRoundKey
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    for fila in range(4):
        for columna in range(4):
            estado[fila][columna] = estado[fila][columna] ^ clave[fila][columna]


def _ExpansionK(clave, vuelta):
    """
    Funcion Expansion de claves
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

    nextClave = [[0] * 4 for i in range(4)]
    nextClave = deepcopy(clave)

    _RotWord(nextClave)
    _SubBytes(nextClave)

    # XOR
    for fila in range(4):
        nextClave[fila][0] = nextClave[fila][0] ^ clave[fila][0]

    # RCON
    nextClave[0][0] = nextClave[0][0] ^ rcon[vuelta]

    # XOR Resto de clave
    for columna in range(3):
        for fila2 in range(4):
            nextClave[fila2][columna + 1] = nextClave[fila2][columna] ^ clave[fila2][columna + 1]

    return nextClave


def _RotWord(nextClave):
    """
    Funcion RotWord
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    primero = nextClave[0][3]

    for fila in range(3):
        nextClave[fila][0] = nextClave[fila + 1][3]

    nextClave[3][0] = primero


def _InvSubBytes(estado):
    """
    Funcion InvSubBytes
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    invMatrizSubBytes = [[' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'],
                         ['0', 0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7,
                          0xFB],
                         ['1', 0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9,
                          0xCB],
                         ['2', 0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3,
                          0x4E],
                         ['3', 0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1,
                          0x25],
                         ['4', 0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6,
                          0x92],
                         ['5', 0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D,
                          0x84],
                         ['6', 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45,
                          0x06],
                         ['7', 0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A,
                          0x6B],
                         ['8', 0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6,
                          0x73],
                         ['9', 0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF,
                          0x6E],
                         ['A', 0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE,
                          0x1B],
                         ['B', 0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A,
                          0xF4],
                         ['C', 0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC,
                          0x5F],
                         ['D', 0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C,
                          0xEF],
                         ['E', 0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99,
                          0x61],
                         ['F', 0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C,
                          0x7D]]

    for fila in range(4):
        for columna in range(4):
            valor = hex(estado[fila][columna])[2:]
            if len(valor) < 2:
                valor = '0' + valor
            valor = valor.upper()
            for car1 in range(17):
                if valor[0] == invMatrizSubBytes[car1][0]:
                    filBusq = car1
            for car2 in range(17):
                if valor[1] == invMatrizSubBytes[0][car2]:
                    colBusq = car2
            estado[fila][columna] = invMatrizSubBytes[filBusq][colBusq]


def _InvMixColumns(estado):
    """
    Funcion InvMixColumns
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    gf = [[0x0E, 0x0B, 0x0D, 0x09],
          [0x09, 0x0E, 0x0B, 0x0D],
          [0x0D, 0x09, 0x0E, 0x0B],
          [0x0B, 0x0D, 0x09, 0x0E]]

    resultado = [[0] * 4 for i in range(4)]

    for columna in range(4):
        resultado[0][columna] = _Galois(estado[0][columna], gf[0][0]) ^ _Galois(estado[1][columna], gf[0][1]) ^ _Galois(
            estado[2][columna], gf[0][2]) ^ _Galois(estado[3][columna], gf[0][3])
        resultado[1][columna] = _Galois(estado[0][columna], gf[1][0]) ^ _Galois(estado[1][columna], gf[1][1]) ^ _Galois(
            estado[2][columna], gf[1][2]) ^ _Galois(estado[3][columna], gf[1][3])
        resultado[2][columna] = _Galois(estado[0][columna], gf[2][0]) ^ _Galois(estado[1][columna], gf[2][1]) ^ _Galois(
            estado[2][columna], gf[2][2]) ^ _Galois(estado[3][columna], gf[2][3])
        resultado[3][columna] = _Galois(estado[0][columna], gf[3][0]) ^ _Galois(estado[1][columna], gf[3][1]) ^ _Galois(
            estado[2][columna], gf[3][2]) ^ _Galois(estado[3][columna], gf[3][3])

    return resultado


def _InvShiftRows(estado):
    """
    Funcion InvShiftRows
    -------------------------------------------------------------------------------

    WARNING: Esta es una función privada y no debería ser invicada directamente.

    -------------------------------------------------------------------------------
"""
    for fila in range(1, 4):
        for i in range(1, 5 - fila):
            primero = estado[fila][0]
            for x in range(3):
                estado[fila][x] = estado[fila][x + 1]
            estado[fila][3] = primero
#nuevo
def pasarAbytes(cadena):
    listaBytes = []
    posicion = 0

    byte = ''
    for i in range(len(cadena)):
        byte = byte + str(cadena[i])
        if posicion == 7:
            posicion = 0
            listaBytes.append(int(str(byte), 2))
            byte = ''
        else:
            posicion = posicion + 1

    return listaBytes

def pasarHexAbits(cadenaHex):
    pos = 0
    cadenabits = ''
    while(pos < len(cadenaHex)):
        cadenabits = cadenabits + str(format(int(cadenaHex[pos] + cadenaHex[pos + 1], 16), '08b'))
        pos = pos + 2

    return cadenabits
