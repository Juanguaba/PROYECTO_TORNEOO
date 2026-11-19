
from datetime import datetime

from app import db


class Configuracion(db.Model):

    __tablename__ = "configuracion"

    id = db.Column(db.Integer, primary_key=True)

    # Identidad del sistema
    nombre_sistema = db.Column(
        db.String(120),
        nullable=False,
        default="Sistema de Gestión de Torneos"
    )

    descripcion = db.Column(
        db.String(300),
        nullable=True
    )

    organizacion = db.Column(
        db.String(150),
        nullable=True
    )

    logo = db.Column(
        db.String(255),
        nullable=True
    )

    # Información de contacto
    email_contacto = db.Column(
        db.String(120),
        nullable=True
    )

    telefono_contacto = db.Column(
        db.String(30),
        nullable=True
    )

    # Preferencias deportivas
    duracion_partido = db.Column(
        db.Integer,
        nullable=False,
        default=90
    )

    descanso = db.Column(
        db.Integer,
        nullable=False,
        default=15
    )

    puntos_victoria = db.Column(
        db.Integer,
        nullable=False,
        default=3
    )

    puntos_empate = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    puntos_derrota = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # Personalización visual
    color_principal = db.Column(
        db.String(20),
        nullable=False,
        default="#126B48"
    )

    # Control de actualización
    fecha_actualizacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Configuracion {self.nombre_sistema}>"
