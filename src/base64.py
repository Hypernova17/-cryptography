

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

#Esta funcion convierte los bytes en cóigo binario :)
def encode(archivo_ini : str) -> None:  
    if "." in archivo_ini:
        nombre_base = archivo_ini[:archivo_ini.rfind(".")]
    else:
        nombre_base = archivo_ini
    arch_destino = nombre_base + ".b64"  

    with open(archivo_ini, "rb") as f:
        datos = f.read()

    if not datos:
        with open(arch_destino, "w", encoding="utf-8") as f:
            f.write("")
        return
    
    binary = ""
    for byte in datos:
        bite = bin(byte)[2:]
        bite = bite.zfill(8)
        binary += bite

    resultado = ""

    for i in range (0, len(binary), 6):
        longsix = binary [i : i + 6]

        while len(longsix) < 6:
            longsix += "0"

        number = int(longsix, 2)
        letra = ALFABETO[number]
        resultado += letra

    while len(resultado) % 4 != 0:
        resultado += "="
    with open(arch_destino, "w", encoding="utf-8") as f:
        f.write(resultado)

    print(f"El archivo fue codificado en: '{arch_destino}'")


def decode(arch_ini: str) -> None:  
    if "." in arch_ini:
        nombre_base = arch_ini[:arch_ini.rfind(".")]
    else:
        nombre_base = arch_ini
    arch_destino = nombre_base 

    with open(arch_ini, "r", encoding="utf-8") as f:
        texto = f.read().strip()

    if not texto:
        with open(arch_destino, "wb") as f:
            f.write(b"")
        return

    contar = texto.count("=")
    limpiar = texto.replace ("=", "")

    binary = ""

    for letra in limpiar:
        numero = ALFABETO.index(letra)
        bits = bin(numero)[2:]
        bits = bits.zfill(6)
        binary += bits 

    if contar == 1:
        binary = binary[:-2]
    elif contar == 2:
        binary = binary[:-4]

    resultado = bytearray()

    for i in range(0, len(binary), 8):
        pedazo = binary [i : i + 8]
        inicial = int(pedazo, 2)
        resultado.append(inicial)
        
    extens= extension(bytes(resultado))
    if extens:
        if "." in arch_destino:
            nombre_base = arch_destino[:arch_destino.rfind(".")]
        else:
            nombre_base = arch_destino
        arch_destino = nombre_base + extens
    else:  # AGREGADO: si no se detecta extensión, se usa una por defecto
        arch_destino = arch_destino + ".bin"  # AGREGADO

    with open(arch_destino, "wb") as f:
        f.write(resultado)

    print(f"El archivo fue decodificado en: '{arch_destino}'")

# -------------------------------------------------------------
# Esta parte del código es utilizada para decifrar el tipo de extencion de la práctica :D
# -------------------------------------------------------------

def extension(datos: bytes) -> str:
    """
    Analiza la firma de bytes iniciales de cualquier archivo
    para deducir su extensión real.
    """
    cabecera = datos[:16]

    if cabecera.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    elif cabecera.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    elif cabecera.startswith(b"%PDF"):
        return ".pdf"
    elif b"ftyp" in cabecera:
        return ".mp4"
    elif cabecera.startswith(b"PK\x03\x04"):
        return ".zip"
    elif cabecera.startswith(b"GIF87a") or cabecera.startswith(b"GIF89a"):
        return ".gif"


if __name__ == "__main__":
    decode("base64.lol")