from flask import render_template, redirect, request, url_for, flash

from . import equipos_bp
from .forms import EquipoForm
from .services import (
    crear_equipo,
    obtener_equipos,
    obtener_equipo_por_nombre
)


@equipos_bp.route("/")
def index():

    equipos = obtener_equipos()

    return render_template(
        "equipos/index.html",
        equipos=equipos
    )


@equipos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    if request.method == "POST":

        form = EquipoForm(request.form)

        if not form.valido():

            flash("Todos los campos son obligatorios.", "danger")

            return render_template("equipos/nuevo.html")

        equipo = obtener_equipo_por_nombre(form.nombre)

        if equipo:

            flash("Ya existe un equipo con ese nombre.", "danger")

            return render_template("equipos/nuevo.html")

        crear_equipo(
            nombre=form.nombre,
            ciudad=form.ciudad,
            entrenador=form.entrenador,
            fundacion=form.fundacion,
            estado=form.estado
        )

        flash("Equipo creado correctamente.", "success")

        return redirect(url_for("equipos.index"))

    return render_template("equipos/nuevo.html")
