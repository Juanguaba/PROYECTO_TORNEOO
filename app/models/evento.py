
from datetime import datetime

from app import db


class Evento(db.Model):

    __tablename__ = "eventos"

    id = db.Column(db.Integer, primary_key=True)

    partido_id = db.Column(
        db.Integer,
        db.ForeignKey("partidos.id"),
        nullable=False
    )

    jugador_id = db.Column(
        db.Integer,
        db.ForeignKey("jugadores.id")
    )

    minuto = db.Column(
        db.Integer,
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    descripcion = db.Column(
        db.String(255)
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    partido = db.relationship(
        "Partido",
        back_populates="eventos"
    )

    jugador = db.relationship(
        "Jugador"
    )

    def __repr__(self):
        return f"<Evento {self.tipo} - Partido {self.partido_id}>"
