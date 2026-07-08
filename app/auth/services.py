from app import db
from app.models.usuario import Usuario
from app.models.rol import Rol


def buscar_usuario_por_username(username):
    return Usuario.query.filter_by(username=username).first()


def buscar_usuario_por_email(email):
    return Usuario.query.filter_by(email=email).first()


def crear_usuario(nombre, username, email, password):
    rol = Rol.query.filter_by(nombre="Usuario").first()

    usuario = Usuario(
        nombre=nombre,
        username=username,
        email=email,
        rol=rol
    )

    usuario.set_password(password)

    db.session.add(usuario)
    db.session.commit()

    return usuario


def autenticar_usuario(usuario_o_email, password):
    usuario = Usuario.query.filter(
        (Usuario.username == usuario_o_email) |
        (Usuario.email == usuario_o_email)
    ).first()

    if usuario and usuario.check_password(password):
        return usuario

    return None
