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


def guardar_imagen(
    archivo,
    carpeta_destino,
    imagen_por_defecto,
    ancho=300,
    alto=300
):

    if not archivo or archivo.filename == "":
        return imagen_por_defecto

    if not extension_permitida(archivo.filename):
        return None

    nombre = f"{uuid.uuid4().hex}.png"

    nombre = secure_filename(nombre)

    ruta = os.path.join(carpeta_destino, nombre)

    imagen = Image.open(archivo)

    imagen = imagen.convert("RGBA")

    imagen = imagen.resize((ancho, alto))

    imagen.save(
        ruta,
        format="PNG",
        optimize=True
    )

    return nombre


def eliminar_imagen(
    nombre_archivo,
    carpeta,
    imagen_por_defecto
):

    if not nombre_archivo:
        return

    if nombre_archivo == imagen_por_defecto:
        return

    ruta = os.path.join(carpeta, nombre_archivo)

    if os.path.exists(ruta):
        os.remove(ruta)
