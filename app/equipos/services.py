from app import db
from app.models.equipo import Equipo


def obtener_equipos():
    return Equipo.query.order_by(Equipo.nombre).all()


def obtener_equipo_por_id(equipo_id):
    return Equipo.query.get(equipo_id)


def obtener_equipo_por_nombre(nombre):
    return Equipo.query.filter_by(nombre=nombre).first()


def crear_equipo(
    nombre,
    ciudad,
    entrenador,
    fundacion,
    estado=True,
    escudo="default_team.png"
):

    equipo = Equipo(
        nombre=nombre,
        ciudad=ciudad,
        entrenador=entrenador,
        fundacion=fundacion,
        estado=estado,
        escudo=escudo
    )

    db.session.add(equipo)
    db.session.commit()

    return equipo


def actualizar_equipo(
    equipo,
    nombre,
    ciudad,
    entrenador,
    fundacion,
    estado,
    escudo
):

    equipo.nombre = nombre
    equipo.ciudad = ciudad
    equipo.entrenador = entrenador
    equipo.fundacion = fundacion
    equipo.estado = estado

    if escudo:
        equipo.escudo = escudo

    db.session.commit()

    return equipo


def eliminar_equipo(equipo):

    db.session.delete(equipo)

    db.session.commit()
