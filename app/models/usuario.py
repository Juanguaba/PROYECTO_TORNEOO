from datetime import datetime

from app import db

from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    descripcion = db.Column(db.Text)

    foto = db.Column(
        db.String(255),
        default="default.png"
    )

    activo = db.Column(
        db.Boolean,
        default=True
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=lambda: datetime.now()
    )

    rol_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )

    rol = db.relationship(
        "Rol",
        back_populates="usuarios"
    )

    def __repr__(self):
        return f"<Usuario {self.username}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
