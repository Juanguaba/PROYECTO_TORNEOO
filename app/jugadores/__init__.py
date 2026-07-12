from flask import Blueprint

jugadores_bp = Blueprint(
    "jugadores",
    __name__,
    url_prefix="/jugadores"
)

from . import routes
