
from app import db


class Estadio(db.Model):

    __tablename__ = "estadios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    ciudad = db.Column(
        db.String(100),
        nullable=False
    )

    direccion = db.Column(
        db.String(200)
    )

    capacidad = db.Column(
        db.Integer,
        nullable=False
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    partidos = db.relationship(
        "Partido",
        back_populates="estadio"
    )

    def __repr__(self):
        return f"<Estadio {self.nombre}>"
