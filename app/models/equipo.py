from app import db


class Equipo(db.Model):

    __tablename__ = "equipos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    ciudad = db.Column(
        db.String(100),
        nullable=False
    )

    entrenador = db.Column(
        db.String(100),
        nullable=False
    )

    fundacion = db.Column(
        db.Integer,
        nullable=False
    )

    escudo = db.Column(
        db.String(255),
        default="default_team.png"
    )

    estado = db.Column(
        db.Boolean,
        default=True
    )

    jugadores = db.relationship(
        "Jugador",
        back_populates="equipo",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Equipo {self.nombre}>"

    torneos = db.relationship(
        "Torneo",
        secondary="torneo_equipos",
        back_populates="equipos"
    )
