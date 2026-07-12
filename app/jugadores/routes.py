from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.equipos.services import obtener_equipo_por_id

from . import jugadores_bp
from .services import (
    obtener_jugadores,
    crear_jugador
)


@jugadores_bp.route("/<int:equipo_id>")
def index(equipo_id):

    equipo = obtener_equipo_por_id(equipo_id)

    jugadores = obtener_jugadores(equipo_id)

    return render_template(
        "jugadores/index.html",
        jugadores=jugadores,
        equipo=equipo,
        active_tab="plantilla"
    )


@jugadores_bp.route("/<int:equipo_id>/nuevo", methods=["GET", "POST"])
def nuevo(equipo_id):

    equipo = obtener_equipo_por_id(equipo_id)

    if request.method == "POST":

        crear_jugador(request.form, equipo_id)

        flash(
            "Jugador registrado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "jugadores.index",
                equipo_id=equipo_id
            )
        )

    return render_template(
        "jugadores/nuevo.html",
        equipo=equipo,
        active_tab="plantilla"
    )
