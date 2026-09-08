""" 
    Primera parte, descifrando utilizando código Cesar.
"""
#

#Leer la ruta del archivo
def leer_archivo_cesar():
    with open('cesar.lol', 'rb') as f:
        datos_cifrados = f.read()
    return datos_cifrados

#Función auxiliar 
def coincide(intento, firma):
    if len(intento) < len(firma):
        return False

    for i in range(len(firma)):
        if intento[i] != firma[i]:
            return False    

    return True


def encontrar_shift(datos_cifrados):
    primeros_bytes = datos_cifrados[:8]
    
    firmas = [
        bytes.fromhex("89504e470d0a1a0a"),
        b"%PDF",
        b"PK\x03\x04",
        bytes.fromhex("ffd8ff"),
        b"GIF89a",
        b"GIF87a",

    ]

    for k in range(256):
        intento = bytes((b - k) % 256 for b in primeros_bytes)
        for firma in firmas:
            if coincide(intento, firma):
                print(f"Se encontró la llave = {k} -> {intento}")
                return k 
    
    return None

datos_cifrados = leer_archivo_cesar()
print("Bytes cifrados:", datos_cifrados[:8])
print("En hex:", datos_cifrados[:8].hex())

shift = encontrar_shift(datos_cifrados)
print("Shift encontrado:", shift)

"""
    Segunda Parte: Descifrar el archivo
"""

def descifrar(datos_cifrados, shift):
    datos_descifrados = []

    for byte in datos_cifrados: 
        byte_descifrado = byte - shift 

        if byte_descifrado < 0:
            byte_descifrado = byte_descifrado + 256

        datos_descifrados.append(byte_descifrado)

    return bytes(datos_descifrados)

datos_descifrados = descifrar(datos_cifrados, shift)

with open('cesar_descifrado.jpg', 'wb') as f:
    f.write(datos_descifrados)

print("Archivo descifrado en formato jpg")
