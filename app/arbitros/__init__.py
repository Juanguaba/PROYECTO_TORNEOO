
from flask import Blueprint

arbitros_bp = Blueprint(
    "arbitros",
    __name__,
    url_prefix="/arbitros"
)

from . import routes
