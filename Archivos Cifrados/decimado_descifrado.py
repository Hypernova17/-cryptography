

# Fórmula del cifrado decimado: C = (X * k) mod 256
# Donde C son los bytes cifrados, X el byte original del archivo, k es la clave del cifrado y 256 los valores posibles de un byte
# Para la clave k necesitamos que sea un número primo relativo con 256
# Para el descifrado necesitamos el inverso multiplicativo de k módulo 256 (K^-1 mod 256), de tal maneta
# que (k * K^-1) mod 256 = 1


def encontrar_inverso(k, modulo=256):
    """
    Busca el inverso multiplicativo de k  por fuerza bruta,probando todos los numeros
    del 1 al 255 hasta encontrar uno que al multiplicarlo por k y sacarle el modulo de 256, de 1
    """
    for candidato in range(1, modulo):
        if (k * candidato) % modulo == 1:
            return candidato
    return None

def cifrado_decimado(bytes_originales, k):
    """
    Fórmula del cifrado decimado: C = (X * k) mod 256
    Cifra los bytes originales multiplicándolos por la clave k y aplicando el módulo 256
    """
    # quitamos los numeros pares de las claves porque tienen un factor comun de 2 y 
    # no tienen inverso multiplicativo modulo 256
    if k % 2 == 0:
        raise ValueError(f"La clave {k} debe ser impar")
    # se crea un bytearray para ir almacenando los bytes que se vayan cifrando
    bytes_cifrados = bytearray()

    for byte in bytes_originales:
        # se aplica la fórmula del cifrado decimado a cada byte original
        byte_cifrado = (byte * k) % 256
        bytes_cifrados.append(byte_cifrado)
    return bytes_cifrados


def descifrado_decimado(bytes_cifrados, k):
    """
    Fórmula del descifrado decimado: X = (C * K^-1) mod 256
    Descifra los bytes cifrados multiplicándolos por el inverso multiplicativo de la clave k y 
    aplicando el modulo 256
    """
    #quitamos los pares
    if k % 2 == 0:
        raise ValueError(f"La clave {k} debe ser impar")
    #calcula el inverso multiplicativo de k modulo 256
    k_inv = encontrar_inverso(k, 256)
    #se crea un bytearray para ir almacenando los bytes que se vayan descifrando
    bytes_descifrados = bytearray()

    for byte in bytes_cifrados:
        # se aplica la formula del descifrado decimado a cada byte cifrado
        byte_descifrado = (byte * k_inv) % 256
        bytes_descifrados.append(byte_descifrado)
    return bytes_descifrados

# Diccionario de firmas (magic bytes)
firmas = {
    "PNG": bytes.fromhex("89504E47"),
    "JPG": bytes.fromhex("FFD8FF"),
    "BMP": bytes.fromhex("424D"),
    "MP3": bytes.fromhex("494433"),
    "WAV": bytes.fromhex("52494646"),
    "OGG": bytes.fromhex("4F676753"),
    "MP4": bytes.fromhex("0000001866747970"),
    "AVI": bytes.fromhex("52494646"),
    "MKV": bytes.fromhex("1A45DFA3"),
    "DOCX": bytes.fromhex("504B0304"),
    "PDF": bytes.fromhex("25504446"),
    "EPUB": bytes.fromhex("504B0304")
}


def romper_decimado(ruta_archivo):
    """
    Rompe el cifrado decimado por fuerza bruta usando magic bytes para validar si la llave es correcta

    """
    # se abren los archivos en modo binario y se cargam los bytes para analizarlos
    with open(ruta_archivo, "rb") as f:
        datos_cifrados = f.read()
    #probamos todas las claves impares posibles
    for k in range(1, 256, 2):
        # por cada llave qu estamos probando iteramos en el diccionario de firmas para ver si la llave actual revela el formato
        for nombre_formato, firma in firmas.items():
            primeros_bytes = datos_cifrados[:len(firma)]
            descifrados = descifrado_decimado(primeros_bytes, k)
            descifrados = bytes(descifrados)
            # si  la parte que desciframos coincide con los magic bytes se descifra el archivo usando la llave encontrada
            if descifrados.startswith(firma):
                print(f"k={k}, formato={nombre_formato}")
                datos_descifrados = descifrado_decimado(datos_cifrados, k)
                nombre_salida = f"descifrado.{nombre_formato.lower()}"
                # guardamos el archivo descifrado
                with open(nombre_salida, "wb") as f:
                    f.write(datos_descifrados)
                print(f"Archivo creado: {nombre_salida}")

                return
            
romper_decimado("decimado.lol")
