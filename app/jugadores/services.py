from datetime import datetime

from sqlalchemy import or_

from app import db
from app.models.jugador import Jugador


def obtener_jugadores(equipo_id, buscar=None):

    query = (
        Jugador.query
        .filter_by(equipo_id=equipo_id)
    )

    if buscar:

        query = query.filter(
            or_(
                Jugador.nombre.ilike(f"%{buscar}%"),
                Jugador.apellido.ilike(f"%{buscar}%"),
                Jugador.posicion.ilike(f"%{buscar}%"),
                Jugador.numero.cast(db.String).ilike(f"%{buscar}%")
            )
        )

    return (
        query
        .order_by(Jugador.numero)
        .all()
    )


def obtener_jugador_por_id(jugador_id):

    return Jugador.query.get_or_404(jugador_id)


def crear_jugador(
    formulario,
    equipo_id,
    foto="default_player.png"
):

    jugador = Jugador(
        equipo_id=equipo_id,
        foto=foto,
        nombre=formulario["nombre"],
        apellido=formulario["apellido"],
        fecha_nacimiento=datetime.strptime(
            formulario["fecha_nacimiento"],
            "%Y-%m-%d"
        ).date(),
        nacionalidad=formulario["nacionalidad"],
        numero=int(formulario["numero"]),
        posicion=formulario["posicion"],
        pie_habil=formulario["pie_habil"],
        altura=float(formulario["altura"]),
        peso=float(formulario["peso"]),
        estado=formulario["estado"],
        capitan="capitan" in formulario,
        lesionado="lesionado" in formulario,
        observaciones=formulario["observaciones"]
    )

    db.session.add(jugador)
    db.session.commit()

    return jugador


def actualizar_jugador(
    jugador,
    formulario,
    foto=None
):

    jugador.nombre = formulario["nombre"]
    jugador.apellido = formulario["apellido"]

    jugador.fecha_nacimiento = datetime.strptime(
        formulario["fecha_nacimiento"],
        "%Y-%m-%d"
    ).date()

    jugador.nacionalidad = formulario["nacionalidad"]
    jugador.numero = int(formulario["numero"])
    jugador.posicion = formulario["posicion"]
    jugador.pie_habil = formulario["pie_habil"]
    jugador.altura = float(formulario["altura"])
    jugador.peso = float(formulario["peso"])
    jugador.estado = formulario["estado"]
    jugador.capitan = "capitan" in formulario
    jugador.lesionado = "lesionado" in formulario
    jugador.observaciones = formulario["observaciones"]

    if foto:
        jugador.foto = foto

    db.session.commit()

    return jugador


def eliminar_jugador(jugador):

    db.session.delete(jugador)

    db.session.commit()
