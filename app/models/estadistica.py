
from app import db


class Estadistica(db.Model):

    __tablename__ = "estadisticas"

    id = db.Column(db.Integer, primary_key=True)

    jugador_id = db.Column(
        db.Integer,
        db.ForeignKey("jugadores.id"),
        nullable=False
    )

    partido_id = db.Column(
        db.Integer,
        db.ForeignKey("partidos.id"),
        nullable=False
    )

    goles = db.Column(
        db.Integer,
        default=0
    )

    asistencias = db.Column(
        db.Integer,
        default=0
    )

    tarjetas_amarillas = db.Column(
        db.Integer,
        default=0
    )

    tarjetas_rojas = db.Column(
        db.Integer,
        default=0
    )

    minutos_jugados = db.Column(
        db.Integer,
        default=0
    )

    jugador = db.relationship("Jugador")

    partido = db.relationship("Partido")

    def __repr__(self):
        return f"<Estadistica Jugador {self.jugador_id}>"
