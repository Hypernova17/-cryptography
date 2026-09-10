from decimado_descifrado import encontrar_inverso, firmas

def cifrado_afin(bytes_originales, a, b):
    """
    Fórmula del cifrado afin: C = (X * a + b) mod 256
    Cifra los bytes originales multiplicandolos por la a y sumandole b y luego aplica modulo 256
    """
    #si a es par compartiria factor 2 con mod 256 y entonces no tiene inverso multiplicativo
    if a % 2 == 0:
        raise ValueError(f"La clave {a} debe ser impar")
    # se crea un bytearray para ir almacenando los bytes que se vayan cifrando
    bytes_cifrados = bytearray()

    for byte in bytes_originales:
        # se aplica la fórmula del cifrado afin a cada byte original
        byte_cifrado = (byte * a + b) % 256
        bytes_cifrados.append(byte_cifrado)
    return bytes_cifrados

def descifrado_afin(bytes_originales, a, b):
    """
    Fórmula del descifrado afin: X = (C - b) * a^-1  mod 256
    Descifra los bytes originales restandoles b y multiplicandolos por el inv multiplicativo de a y luego modulo 256
    """
    if a % 2 == 0:
        raise ValueError(f"La clave {a} debe ser impar")
    # calcula el inverso multiplicativo de a modulo 256
    a_inv = encontrar_inverso(a, 256)
    # se crea un bytearray para ir almacenando los bytes que se vayan cifrando
    bytes_descifrados = bytearray()
    for byte in bytes_originales:
        # se aplica la fórmula del cifrado afin a cada byte original
        byte_descifrado = ((byte - b) * a_inv) % 256
        bytes_descifrados.append(byte_descifrado)
    return bytes_descifrados


def romper_afin(ruta_archivo):
    """
    Rompe el cifrado afin probando pares (a, b) y usando magic bytes para validar si la combinación es correcta
    se prueba para todas las combinaciones de a y b posibles
    """
    with open(ruta_archivo, "rb") as f:
        datos_cifrados = f.read()
    for a in range(1, 256, 2):
        for b in range (256):
            for nombre_formato, firma in firmas.items():
                primeros_bytes = datos_cifrados[:len(firma)]
                descifrados = descifrado_afin(primeros_bytes, a, b)
                descifrados = bytes(descifrados)
                if descifrados.startswith(firma):
                    print(f"a={a}, b={b} formato={nombre_formato}")
                    datos_descifrados = descifrado_afin(datos_cifrados, a, b)
                    nombre_salida = f"descifrado.{nombre_formato.lower()}"
                    with open(nombre_salida, "wb") as f:
                        f.write(datos_descifrados)
                    print(f"Archivo creado: {nombre_salida}")

                    return
if __name__ == "__main__":
    romper_afin("afin.lol") #se generó el archivo pero no se ve):
    romper_afin("afin2.lol") #lo mismo que el anterior):
    romper_afin("¿_.lol")