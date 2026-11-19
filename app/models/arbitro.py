
from app import db


class Arbitro(db.Model):

    __tablename__ = "arbitros"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    documento = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True
    )

    telefono = db.Column(
        db.String(30)
    )

    categoria = db.Column(
        db.String(50),
        nullable=False
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    partidos = db.relationship(
        "Partido",
        back_populates="arbitro"
    )

    def __repr__(self):
        return f"<Arbitro {self.nombre} {self.apellido}>"
