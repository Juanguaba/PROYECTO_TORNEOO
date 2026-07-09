from flask import Blueprint

equipos_bp = Blueprint(
    "equipos",
    __name__,
    url_prefix="/equipos"
)

from . import routes
