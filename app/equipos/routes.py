import os
from flask import (
    render_template,
    redirect, request,
    url_for, flash,
    current_app
)
from . import equipos_bp
from .forms import EquipoForm
from app.utils.image import (
    guardar_escudo,
    eliminar_escudo
)
from .services import (
    crear_equipo,
    obtener_equipos,
    obtener_equipo_por_nombre,
    obtener_equipo_por_id,
    actualizar_equipo,
    eliminar_equipo
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

        print("FILES:", request.files)
        print("ESCUDO:", request.files.get("escudo"))

        form = EquipoForm(request.form)

        if not form.valido():

            flash("Todos los campos son obligatorios.", "danger")

            return render_template("equipos/nuevo.html")

        equipo = obtener_equipo_por_nombre(form.nombre)

        if equipo:

            flash("Ya existe un equipo con ese nombre.", "danger")

            return render_template("equipos/nuevo.html")

        archivo = request.files.get("escudo")

        carpeta = os.path.join(
            current_app.static_folder,
            "uploads",
            "equipos"
        )

        escudo = guardar_escudo(
            archivo,
            carpeta
        ) if archivo else "default_team.png"

        crear_equipo(
            nombre=form.nombre,
            ciudad=form.ciudad,
            entrenador=form.entrenador,
            fundacion=form.fundacion,
            estado=form.estado,
            escudo=escudo
        )

        flash("Equipo creado correctamente.", "success")

        return redirect(url_for("equipos.index"))

    return render_template("equipos/nuevo.html")


@equipos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    equipo = obtener_equipo_por_id(id)

    if not equipo:

        flash("El equipo no existe.", "danger")

        return redirect(url_for("equipos.index"))

    if request.method == "POST":

        form = EquipoForm(request.form)

        if not form.valido():

            flash("Todos los campos son obligatorios.", "danger")

            return render_template(
                "equipos/editar.html",
                equipo=equipo
            )

        equipo_existente = obtener_equipo_por_nombre(form.nombre)

        if (
            equipo_existente
            and equipo_existente.id != equipo.id
        ):

            flash(
                "Ya existe otro equipo con ese nombre.",
                "danger"
            )

            return render_template(
                "equipos/editar.html",
                equipo=equipo
            )

        # Aquí después actualizaremos el escudo
        archivo = request.files.get("escudo")

        nuevo_escudo = equipo.escudo

        if archivo and archivo.filename:

            archivo = request.files.get("escudo")

            carpeta = os.path.join(
                current_app.static_folder,
                "uploads",
                "equipos"
            )

            eliminar_escudo(
                equipo.escudo,
                carpeta
            )

            nuevo_escudo = guardar_escudo(
                archivo,
                carpeta
            )

        actualizar_equipo(
            equipo=equipo,
            nombre=form.nombre,
            ciudad=form.ciudad,
            entrenador=form.entrenador,
            fundacion=form.fundacion,
            estado=form.estado,
            escudo=nuevo_escudo
        )

        flash(
            "Equipo actualizado correctamente.",
            "success"
        )

        return redirect(url_for("equipos.index"))

    return render_template(
        "equipos/editar.html",
        equipo=equipo
    )


@equipos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    equipo = obtener_equipo_por_id(id)

    if not equipo:

        flash("El equipo no existe.", "danger")

        return redirect(url_for("equipos.index"))

    carpeta = os.path.join(
        current_app.static_folder,
        "uploads",
        "equipos"
    )

    eliminar_escudo(
        equipo.escudo,
        carpeta
    )

    eliminar_equipo(equipo)

    flash(
        "Equipo eliminado correctamente.",
        "success"
    )

    return redirect(url_for("equipos.index"))


@equipos_bp.route("/<int:id>")
def detalle(id):

    equipo = obtener_equipo_por_id(id)

    if not equipo:

        flash("Equipo no encontrado.", "danger")

        return redirect(url_for("equipos.index"))

    return render_template(
        "equipos/informacion.html",
        equipo=equipo,
        active_tab="info"
    )
