
from datetime import datetime

from app import db


torneo_equipos = db.Table(
    "torneo_equipos",

    db.Column(
        "torneo_id",
        db.Integer,
        db.ForeignKey("torneos.id"),
        primary_key=True
    ),

    db.Column(
        "equipo_id",
        db.Integer,
        db.ForeignKey("equipos.id"),
        primary_key=True
    )
)


class Torneo(db.Model):

    __tablename__ = "torneos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    descripcion = db.Column(db.Text)

    fecha_inicio = db.Column(
        db.Date,
        nullable=False
    )

    fecha_fin = db.Column(
        db.Date,
        nullable=False
    )

    formato = db.Column(
        db.String(50),
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        default="Pendiente"
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.now
    )

    equipos = db.relationship(
        "Equipo",
        secondary=torneo_equipos,
        back_populates="torneos"
    )

    partidos = db.relationship(
        "Partido",
        back_populates="torneo"
    )

    def __repr__(self):
        return f"<Torneo {self.nombre}>"
