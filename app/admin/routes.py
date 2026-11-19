
from flask import render_template

from app.models import Usuario, Equipo, Jugador, Torneo

from . import admin_bp


@admin_bp.route("/")
def dashboard():

    usuarios_count = Usuario.query.count()
    equipos_count = Equipo.query.count()
    jugadores_count = Jugador.query.count()
    torneos_count = Torneo.query.count()

    return render_template(
        "admin/dashboard.html",
        usuarios_count=usuarios_count,
        equipos_count=equipos_count,
        jugadores_count=jugadores_count,
        torneos_count=torneos_count
    )
