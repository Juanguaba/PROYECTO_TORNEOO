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
    obtener_jugador_por_id,
    crear_jugador,
    actualizar_jugador,
    eliminar_jugador
)


@jugadores_bp.route("/<int:equipo_id>")
def index(equipo_id):

    equipo = obtener_equipo_por_id(equipo_id)

    buscar = request.args.get("buscar", "").strip()

    jugadores = obtener_jugadores(
        equipo_id=equipo_id,
        buscar=buscar
    )

    if request.args.get("partial"):

        return render_template(
            "jugadores/partials/_table.html",
            jugadores=jugadores,
            equipo=equipo
        )

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


@jugadores_bp.route("/detalle/<int:jugador_id>")
def detalle(jugador_id):

    jugador = obtener_jugador_por_id(jugador_id)

    return render_template(
        "jugadores/detalle.html",
        jugador=jugador,
        equipo=jugador.equipo,
        active_tab="plantilla"
    )


@jugadores_bp.route(
    "/editar/<int:jugador_id>",
    methods=["GET", "POST"]
)
def editar(jugador_id):

    jugador = obtener_jugador_por_id(jugador_id)

    if request.method == "POST":

        actualizar_jugador(
            jugador,
            request.form
        )

        flash(
            "Jugador actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for(
                "jugadores.detalle",
                jugador_id=jugador.id
            )
        )

    return render_template(
        "jugadores/editar.html",
        jugador=jugador,
        equipo=jugador.equipo,
        active_tab="plantilla"
    )


@jugadores_bp.route("/eliminar/<int:jugador_id>", methods=["POST"])
def eliminar(jugador_id):
    jugador = obtener_jugador_por_id(jugador_id)
    equipo_id = jugador.equipo.id

    eliminar_jugador(jugador)

    flash("Jugador eliminado correctamente.", "success")

    return redirect(
        url_for(
            "jugadores.index",
            equipo_id=equipo_id
        )
    )
