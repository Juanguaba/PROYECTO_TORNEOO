
from flask import render_template

from app.models import Usuario, Equipo, Jugador

from . import admin_bp


@admin_bp.route("/")
def dashboard():

    total_usuarios = Usuario.query.count()
    total_equipos = Equipo.query.count()
    total_jugadores = Jugador.query.count()

    return render_template(
        "admin/dashboard.html",
        total_usuarios=total_usuarios,
        total_equipos=total_equipos,
        total_jugadores=total_jugadores,
        total_torneos=0
    )
