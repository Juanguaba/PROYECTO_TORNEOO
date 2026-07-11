import os
import uuid

from PIL import Image
from werkzeug.utils import secure_filename


EXTENSIONES_PERMITIDAS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def extension_permitida(nombre_archivo):

    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower()
        in EXTENSIONES_PERMITIDAS
    )


def guardar_escudo(archivo, carpeta_destino):

    if archivo.filename == "":
        return "default_team.png"

    if not extension_permitida(archivo.filename):
        return None

    nombre = f"{uuid.uuid4().hex}.png"

    nombre = secure_filename(nombre)

    ruta = os.path.join(carpeta_destino, nombre)

    imagen = Image.open(archivo)

    imagen = imagen.convert("RGBA")

    imagen = imagen.resize((300, 300))

    imagen.save(
        ruta,
        format="PNG",
        optimize=True
    )

    return nombre


def eliminar_escudo(nombre_archivo, carpeta):

    if not nombre_archivo:
        return

    if nombre_archivo == "default_team.png":
        return

    ruta = os.path.join(carpeta, nombre_archivo)

    if os.path.exists(ruta):
        os.remove(ruta)
