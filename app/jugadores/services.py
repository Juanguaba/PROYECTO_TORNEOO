from datetime import datetime

from app.models.jugador import Jugador
from app import db


def obtener_jugadores(equipo_id):

    return (
        Jugador.query
        .filter_by(equipo_id=equipo_id)
        .order_by(Jugador.numero)
        .all()
    )


def crear_jugador(formulario, equipo_id):

    jugador = Jugador(
        equipo_id=equipo_id,
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
