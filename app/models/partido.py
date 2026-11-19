
from datetime import datetime

from app import db


class Partido(db.Model):

    __tablename__ = "partidos"

    id = db.Column(db.Integer, primary_key=True)

    torneo_id = db.Column(
        db.Integer,
        db.ForeignKey("torneos.id"),
        nullable=False
    )

    equipo_local_id = db.Column(
        db.Integer,
        db.ForeignKey("equipos.id"),
        nullable=False
    )

    equipo_visitante_id = db.Column(
        db.Integer,
        db.ForeignKey("equipos.id"),
        nullable=False
    )

    estadio_id = db.Column(
        db.Integer,
        db.ForeignKey("estadios.id")
    )

    arbitro_id = db.Column(
        db.Integer,
        db.ForeignKey("arbitros.id")
    )

    fecha = db.Column(
        db.DateTime,
        nullable=False
    )

    goles_local = db.Column(
        db.Integer,
        default=0
    )

    goles_visitante = db.Column(
        db.Integer,
        default=0
    )

    estado = db.Column(
        db.String(30),
        default="Programado"
    )

    torneo = db.relationship(
        "Torneo",
        back_populates="partidos"
    )

    equipo_local = db.relationship(
        "Equipo",
        foreign_keys=[equipo_local_id]
    )

    equipo_visitante = db.relationship(
        "Equipo",
        foreign_keys=[equipo_visitante_id]
    )

    estadio = db.relationship(
        "Estadio",
        back_populates="partidos"
    )

    arbitro = db.relationship(
        "Arbitro",
        back_populates="partidos"
    )

    eventos = db.relationship(
        "Evento",
        back_populates="partido",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Partido {self.id}>"
