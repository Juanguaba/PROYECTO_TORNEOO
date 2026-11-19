
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from sqlalchemy import or_, func

from app import db
from app.models import Estadio, Partido

from . import estadios_bp


@estadios_bp.route("/")
def index():

    busqueda = request.args.get("q", "").strip()
    filtro_estado = request.args.get("estado", "")

    consulta = Estadio.query

    if busqueda:
        consulta = consulta.filter(
            or_(
                Estadio.nombre.ilike(f"%{busqueda}%"),
                Estadio.ciudad.ilike(f"%{busqueda}%"),
                Estadio.direccion.ilike(f"%{busqueda}%")
            )
        )

    if filtro_estado == "activo":
        consulta = consulta.filter_by(estado=True)

    elif filtro_estado == "inactivo":
        consulta = consulta.filter_by(estado=False)

    estadios = consulta.order_by(Estadio.nombre.asc()).all()

    total_estadios = Estadio.query.count()
    estadios_activos = Estadio.query.filter_by(estado=True).count()
    estadios_inactivos = Estadio.query.filter_by(estado=False).count()

    total_capacidad = db.session.query(
        func.coalesce(func.sum(Estadio.capacidad), 0)
    ).scalar()

    total_partidos = Partido.query.filter(
        Partido.estadio_id.isnot(None)
    ).count()

    return render_template(
        "estadios/index.html",
        estadios=estadios,
        busqueda=busqueda,
        filtro_estado=filtro_estado,
        total_estadios=total_estadios,
        estadios_activos=estadios_activos,
        estadios_inactivos=estadios_inactivos,
        total_capacidad=total_capacidad,
        total_partidos=total_partidos
    )


@estadios_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        ciudad = request.form.get("ciudad", "").strip()
        direccion = request.form.get("direccion", "").strip()
        capacidad = request.form.get("capacidad", "").strip()

        if not nombre or not ciudad or not capacidad:
            flash("Completa los campos obligatorios.", "danger")

        else:
            try:
                capacidad = int(capacidad)

                if capacidad <= 0:
                    raise ValueError(
                        "La capacidad debe ser mayor que cero."
                    )

                estadio_existente = Estadio.query.filter(
                    func.lower(Estadio.nombre) == nombre.lower(),
                    func.lower(Estadio.ciudad) == ciudad.lower()
                ).first()

                if estadio_existente:
                    raise ValueError(
                        "Ya existe un estadio con ese nombre en esa ciudad."
                    )

                estadio = Estadio(
                    nombre=nombre,
                    ciudad=ciudad,
                    direccion=direccion or None,
                    capacidad=capacidad,
                    estado=True
                )

                db.session.add(estadio)
                db.session.commit()

                flash("Estadio registrado correctamente.", "success")

                return redirect(url_for("estadios.index"))

            except ValueError as error:
                db.session.rollback()
                flash(str(error), "danger")

            except Exception:
                db.session.rollback()
                flash("No fue posible registrar el estadio.", "danger")

    return render_template("estadios/nuevo.html")


@estadios_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    estadio = db.session.get(Estadio, id)

    if not estadio:
        flash("El estadio no existe.", "danger")
        return redirect(url_for("estadios.index"))

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        ciudad = request.form.get("ciudad", "").strip()
        direccion = request.form.get("direccion", "").strip()
        capacidad = request.form.get("capacidad", "").strip()

        estado = request.form.get("estado")

        try:
            if not nombre or not ciudad or not capacidad:
                raise ValueError(
                    "Completa los campos obligatorios."
                )

            capacidad = int(capacidad)

            if capacidad <= 0:
                raise ValueError(
                    "La capacidad debe ser mayor que cero."
                )

            if estado not in ["activo", "inactivo"]:
                raise ValueError("Selecciona un estado válido.")

            estadio_existente = Estadio.query.filter(
                func.lower(Estadio.nombre) == nombre.lower(),
                func.lower(Estadio.ciudad) == ciudad.lower(),
                Estadio.id != estadio.id
            ).first()

            if estadio_existente:
                raise ValueError(
                    "Ya existe otro estadio con ese nombre en esa ciudad."
                )

            estadio.nombre = nombre
            estadio.ciudad = ciudad
            estadio.direccion = direccion or None
            estadio.capacidad = capacidad
            estadio.estado = estado == "activo"

            db.session.commit()

            flash("Estadio actualizado correctamente.", "success")

            return redirect(url_for("estadios.index"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

        except Exception:
            db.session.rollback()
            flash("No fue posible actualizar el estadio.", "danger")

    return render_template(
        "estadios/editar.html",
        estadio=estadio
    )


@estadios_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
def cambiar_estado(id):

    estadio = db.session.get(Estadio, id)

    if not estadio:
        flash("El estadio no existe.", "danger")
        return redirect(url_for("estadios.index"))

    estadio.estado = not estadio.estado

    db.session.commit()

    mensaje = (
        "Estadio activado correctamente."
        if estadio.estado
        else "Estadio desactivado correctamente."
    )

    flash(mensaje, "success")

    return redirect(url_for("estadios.index"))


@estadios_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    estadio = db.session.get(Estadio, id)

    if not estadio:
        flash("El estadio no existe.", "danger")
        return redirect(url_for("estadios.index"))

    if estadio.partidos:
        flash(
            "No puedes eliminar este estadio porque tiene partidos asociados. "
            "Puedes desactivarlo en su lugar.",
            "warning"
        )
        return redirect(url_for("estadios.index"))

    db.session.delete(estadio)
    db.session.commit()

    flash("Estadio eliminado correctamente.", "success")

    return redirect(url_for("estadios.index"))
