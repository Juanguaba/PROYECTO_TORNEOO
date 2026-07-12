from app import db


class Jugador(db.Model):

    __tablename__ = "jugadores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    equipo_id = db.Column(
        db.Integer,
        db.ForeignKey("equipos.id"),
        nullable=False
    )

    foto = db.Column(
        db.String(255),
        default="default_player.png"
    )

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    apellido = db.Column(
        db.String(100),
        nullable=False
    )

    fecha_nacimiento = db.Column(
        db.Date,
        nullable=False
    )

    nacionalidad = db.Column(
        db.String(100),
        nullable=False
    )

    numero = db.Column(
        db.Integer,
        nullable=False
    )

    posicion = db.Column(
        db.String(50),
        nullable=False
    )

    pie_habil = db.Column(
        db.String(20),
        nullable=False
    )

    altura = db.Column(
        db.Float,
        nullable=False
    )

    peso = db.Column(
        db.Float,
        nullable=False
    )

    estado = db.Column(
        db.String(30),
        default="Activo"
    )

    lesionado = db.Column(
        db.Boolean,
        default=False
    )

    capitan = db.Column(
        db.Boolean,
        default=False
    )

    observaciones = db.Column(
        db.Text
    )

    equipo = db.relationship(
        "Equipo",
        back_populates="jugadores"
    )

    def __repr__(self):
        return f"<Jugador {self.nombre} {self.apellido}>"
