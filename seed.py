from app import create_app, db
from app.models.rol import Rol

app = create_app()

with app.app_context():
    roles = [
        "Administrador",
        "Organizador",
        "Usuario"
    ]

    for nombre in roles:
        existe = Rol.query.filter_by(nombre=nombre).first()

        if not existe:
            db.session.add(Rol(nombre=nombre))

    db.session.commit()

    print("Roles creados correctamente.")
