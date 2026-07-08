from app import db


class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)

    # Relación con usuarios
    usuarios = db.relationship(
        "Usuario",
        back_populates="rol",
        lazy=True
    )

    def __repr__(self):
        return f"<Rol {self.nombre}>"
