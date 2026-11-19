from flask import Blueprint

partidos_bp = Blueprint(
    "partidos",
    __name__,
    url_prefix="/partidos"
)

from . import routes