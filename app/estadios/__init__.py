
from flask import Blueprint

estadios_bp = Blueprint(
    "estadios",
    __name__,
    url_prefix="/estadios"
)

from . import routes
