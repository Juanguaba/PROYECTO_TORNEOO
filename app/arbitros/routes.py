
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from sqlalchemy import or_, func

from app import db
from app.models import Arbitro

from . import arbitros_bp


@arbitros_bp.route("/")
def index():

    busqueda = request.args.get("q", "").strip()
    filtro_estado = request.args.get("estado", "")
    filtro_categoria = request.args.get("categoria", "")

    consulta = Arbitro.query

    if busqueda:
        consulta = consulta.filter(
            or_(
                Arbitro.nombre.ilike(f"%{busqueda}%"),
                Arbitro.apellido.ilike(f"%{busqueda}%"),
                Arbitro.documento.ilike(f"%{busqueda}%"),
                Arbitro.email.ilike(f"%{busqueda}%")
            )
        )

    if filtro_estado == "activo":
        consulta = consulta.filter_by(estado=True)
    elif filtro_estado == "inactivo":
        consulta = consulta.filter_by(estado=False)

    if filtro_categoria:
        consulta = consulta.filter_by(categoria=filtro_categoria)

    arbitros = consulta.order_by(
        Arbitro.nombre.asc(),
        Arbitro.apellido.asc()
    ).all()

    categorias = [
        categoria[0]
        for categoria in db.session.query(
            Arbitro.categoria
        ).distinct().order_by(Arbitro.categoria).all()
    ]

    return render_template(
        "arbitros/index.html",
        arbitros=arbitros,
        busqueda=busqueda,
        filtro_estado=filtro_estado,
        filtro_categoria=filtro_categoria,
        categorias=categorias,
        total_arbitros=Arbitro.query.count(),
        arbitros_activos=Arbitro.query.filter_by(estado=True).count(),
        arbitros_inactivos=Arbitro.query.filter_by(estado=False).count()
    )


@arbitros_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        categoria = request.form.get("categoria", "").strip()

        try:
            if not all([nombre, apellido, documento, categoria]):
                raise ValueError(
                    "Completa los campos obligatorios."
                )

            if len(documento) > 30:
                raise ValueError("El documento no puede"
                                 "superar 30 caracteres.")

            if len(email) > 120:
                raise ValueError("El correo no puede superar 120 caracteres.")

            if len(telefono) > 30:
                raise ValueError("El teléfono no puede superar 30 caracteres.")

            if len(categoria) > 50:
                raise ValueError("La categoría no puede"
                                 "superar 50 caracteres.")

            existente = Arbitro.query.filter(
                func.lower(Arbitro.documento) == documento.lower()
            ).first()

            if existente:
                raise ValueError(
                    "Ya existe un árbitro con ese documento."
                )

            if email:
                correo_existente = Arbitro.query.filter(
                    func.lower(Arbitro.email) == email
                ).first()

                if correo_existente:
                    raise ValueError(
                        "Ya existe un árbitro con ese correo electrónico."
                    )

            arbitro = Arbitro(
                nombre=nombre,
                apellido=apellido,
                documento=documento,
                email=email or None,
                telefono=telefono or None,
                categoria=categoria,
                estado=True
            )

            db.session.add(arbitro)
            db.session.commit()

            flash("Árbitro registrado correctamente.", "success")
            return redirect(url_for("arbitros.index"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

        except Exception:
            db.session.rollback()
            flash("No fue posible registrar el árbitro.", "danger")

    return render_template("arbitros/nuevo.html")


@arbitros_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    arbitro = db.session.get(Arbitro, id)

    if not arbitro:
        flash("El árbitro no existe.", "danger")
        return redirect(url_for("arbitros.index"))

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        documento = request.form.get("documento", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        categoria = request.form.get("categoria", "").strip()
        estado = request.form.get("estado", "")

        try:
            if not all([nombre, apellido, documento, categoria]):
                raise ValueError(
                    "Completa los campos obligatorios."
                )

            if estado not in ["activo", "inactivo"]:
                raise ValueError("Selecciona un estado válido.")

            if len(documento) > 30:
                raise ValueError("El documento no puede"
                                 "superar 30 caracteres.")

            if len(email) > 120:
                raise ValueError("El correo no puede superar 120 caracteres.")

            if len(telefono) > 30:
                raise ValueError("El teléfono no puede superar 30 caracteres.")

            if len(categoria) > 50:
                raise ValueError("La categoría no puede"
                                 "superar 50 caracteres.")

            documento_existente = Arbitro.query.filter(
                func.lower(Arbitro.documento) == documento.lower(),
                Arbitro.id != arbitro.id
            ).first()

            if documento_existente:
                raise ValueError(
                    "Ese documento ya pertenece a otro árbitro."
                )

            if email:
                correo_existente = Arbitro.query.filter(
                    func.lower(Arbitro.email) == email,
                    Arbitro.id != arbitro.id
                ).first()

                if correo_existente:
                    raise ValueError(
                        "Ese correo ya pertenece a otro árbitro."
                    )

            arbitro.nombre = nombre
            arbitro.apellido = apellido
            arbitro.documento = documento
            arbitro.email = email or None
            arbitro.telefono = telefono or None
            arbitro.categoria = categoria
            arbitro.estado = estado == "activo"

            db.session.commit()

            flash("Árbitro actualizado correctamente.", "success")
            return redirect(url_for("arbitros.index"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

        except Exception:
            db.session.rollback()
            flash("No fue posible actualizar el árbitro.", "danger")

    return render_template(
        "arbitros/editar.html",
        arbitro=arbitro
    )


@arbitros_bp.route("/cambiar-estado/<int:id>", methods=["POST"])
def cambiar_estado(id):

    arbitro = db.session.get(Arbitro, id)

    if not arbitro:
        flash("El árbitro no existe.", "danger")
        return redirect(url_for("arbitros.index"))

    arbitro.estado = not arbitro.estado

    db.session.commit()

    mensaje = (
        "Árbitro activado correctamente."
        if arbitro.estado
        else "Árbitro desactivado correctamente."
    )

    flash(mensaje, "success")

    return redirect(url_for("arbitros.index"))


@arbitros_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    arbitro = db.session.get(Arbitro, id)

    if not arbitro:
        flash("El árbitro no existe.", "danger")
        return redirect(url_for("arbitros.index"))

    if arbitro.partidos:
        flash(
            "No puedes eliminar este árbitro porque tiene partidos asociados. "
            "Puedes desactivarlo en su lugar.",
            "warning"
        )
        return redirect(url_for("arbitros.index"))

    db.session.delete(arbitro)
    db.session.commit()

    flash("Árbitro eliminado correctamente.", "success")

    return redirect(url_for("arbitros.index"))
