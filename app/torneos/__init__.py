from flask import Blueprint

torneos_bp = Blueprint(
    "torneos",
    __name__,
    url_prefix="/torneos"
)

from . import routes
