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

#Lista de extensiones más comunes y sus firmas correspondientes 
firmas = [
    bytes.fromhex("89504e470d0a1a0a"),
    b"%PDF",
    b"PK\x03\x04",
    bytes.fromhex("ffd8ff"),
    b"GIF89a",
    b"GIF87a",
]

extensiones = [
    "png",
    "pdf",
    "zip",
    "jpg",
    "gif",
    "gif",
]


def encontrar_shift_extension(datos_cifrados):
    """
    Encuentra la llave necesaria para el cifrado cesar probando con las 256 posibles corrimientos 
    y compara con las firmas ya conocidas. 
    """
    primeros_bytes = datos_cifrados[:8]
    
    for k in range(256):
        intento = bytes((b - k) % 256 for b in primeros_bytes)
        for i in range(len(firmas)):
            if coincide(intento, firmas[i]):
                print(f"Se encontró la llave = {k} -> {intento} ({extensiones[i]})")
                return k, extensiones[i]
    
    return None, None

#Leer el archivo cifrado
datos_cifrados = leer_archivo_cesar()
print("Bytes cifrados:", datos_cifrados[:8])
print("En hex:", datos_cifrados[:8].hex())

#Encuentra la llave y el corrimiento aplicado
shift, extension = encontrar_shift_extension(datos_cifrados)
print("Corrimiento encontrado:", shift)
print("Extension original:" , extensiones)


"""
    Segunda Parte: Descifrar el archivo
"""

def descifrar(datos_cifrados, shift):
    datos_descifrados = []
    #Recorremos cada del archivo
    for byte in datos_cifrados:
        #Se resta el corrimiento que se le haya aplicado a cada byte  
        byte_descifrado = byte - shift 

        #Si el resultado es negativo entonces aplicamos mod 256
        if byte_descifrado < 0:
            byte_descifrado = byte_descifrado + 256

        #Volvemos a convertir la lista a bytes
        datos_descifrados.append(byte_descifrado)

    return bytes(datos_descifrados)

if shift is None: 
    print("No se encontró la llave necesaria para descifrar el archivo")
else:
    #Descifra todos los datos con el corrimiento encontrado 
    datos_descifrados = descifrar(datos_cifrados, shift)

    #Se agrega al archivo descifrado la extension correspondiente
    nombre_final = "cesar_descifrado." + extension

    with open(nombre_final, 'wb') as f:
        f.write(datos_descifrados)

    print("Archivo descifrado: ", nombre_final)

