from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app import db
from app.models import Torneo, Equipo

from . import torneos_bp


@torneos_bp.route("/")
def index():

    torneos = Torneo.query.order_by(
        Torneo.fecha_creacion.desc()
    ).all()

    return render_template(
        "torneos/index.html",
        torneos=torneos
    )


@torneos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    equipos = Equipo.query.order_by(Equipo.nombre).all()

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        formato = request.form.get("formato")
        estado = request.form.get("estado")
        equipos_ids = request.form.getlist("equipos")

        if not all([nombre, fecha_inicio, fecha_fin, formato, estado]):
            flash("Completa todos los campos obligatorios.", "danger")

            return render_template(
                "torneos/nuevo.html",
                equipos=equipos
            )

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

            if fin < inicio:
                flash(
                    "La fecha de finalización no puede"
                    " ser anterior al inicio.",
                    "danger"
                )

                return render_template(
                    "torneos/nuevo.html",
                    equipos=equipos
                )

        except ValueError:
            flash("Las fechas ingresadas no son válidas.", "danger")

            return render_template(
                "torneos/nuevo.html",
                equipos=equipos
            )

        torneo = Torneo(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=inicio,
            fecha_fin=fin,
            formato=formato,
            estado=estado
        )

        equipos_seleccionados = Equipo.query.filter(
            Equipo.id.in_(equipos_ids)
        ).all() if equipos_ids else []

        torneo.equipos = equipos_seleccionados

        db.session.add(torneo)
        db.session.commit()

        flash("Torneo creado correctamente.", "success")

        return redirect(url_for("torneos.index"))

    return render_template(
        "torneos/nuevo.html",
        equipos=equipos
    )


@torneos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    torneo = db.session.get(Torneo, id)

    if not torneo:
        flash("El torneo no existe.", "danger")
        return redirect(url_for("torneos.index"))

    equipos = Equipo.query.order_by(Equipo.nombre).all()

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        formato = request.form.get("formato")
        estado = request.form.get("estado")
        equipos_ids = request.form.getlist("equipos")

        if not all([nombre, fecha_inicio, fecha_fin, formato, estado]):
            flash("Completa todos los campos obligatorios.", "danger")

            return render_template(
                "torneos/editar.html",
                torneo=torneo,
                equipos=equipos
            )

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

            if fin < inicio:
                flash(
                    "La fecha de finalización no puede"
                    "ser anterior al inicio.",
                    "danger"
                )

                return render_template(
                    "torneos/editar.html",
                    torneo=torneo,
                    equipos=equipos
                )

        except ValueError:
            flash("Las fechas ingresadas no son válidas.", "danger")

            return render_template(
                "torneos/editar.html",
                torneo=torneo,
                equipos=equipos
            )

        torneo.nombre = nombre
        torneo.descripcion = descripcion
        torneo.fecha_inicio = inicio
        torneo.fecha_fin = fin
        torneo.formato = formato
        torneo.estado = estado

        torneo.equipos = Equipo.query.filter(
            Equipo.id.in_(equipos_ids)
        ).all() if equipos_ids else []

        db.session.commit()

        flash("Torneo actualizado correctamente.", "success")

        return redirect(url_for("torneos.index"))

    return render_template(
        "torneos/editar.html",
        torneo=torneo,
        equipos=equipos
    )


@torneos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    torneo = db.session.get(Torneo, id)

    if not torneo:
        flash("El torneo no existe.", "danger")
        return redirect(url_for("torneos.index"))

    if torneo.partidos:
        flash(
            "No puedes eliminar un torneo que tiene partidos registrados.",
            "warning"
        )
        return redirect(url_for("torneos.index"))

    db.session.delete(torneo)
    db.session.commit()

    flash("Torneo eliminado correctamente.", "success")

    return redirect(url_for("torneos.index"))
