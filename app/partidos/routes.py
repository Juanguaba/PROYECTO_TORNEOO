
from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app import db
from app.models import (
    Partido,
    Torneo,
    Equipo,
    Estadio,
    Arbitro
)

from . import partidos_bp


@partidos_bp.route("/")
def index():

    partidos = Partido.query.order_by(
        Partido.fecha.desc()
    ).all()

    return render_template(
        "partidos/index.html",
        partidos=partidos
    )


@partidos_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    torneos = Torneo.query.order_by(Torneo.nombre).all()
    estadios = Estadio.query.filter_by(estado=True).order_by(
        Estadio.nombre
    ).all()
    arbitros = Arbitro.query.filter_by(estado=True).order_by(
        Arbitro.nombre
    ).all()

    if request.method == "POST":

        torneo_id = request.form.get("torneo_id")
        equipo_local_id = request.form.get("equipo_local_id")
        equipo_visitante_id = request.form.get("equipo_visitante_id")
        estadio_id = request.form.get("estadio_id") or None
        arbitro_id = request.form.get("arbitro_id") or None
        fecha = request.form.get("fecha")
        estado = request.form.get("estado", "Programado")

        if not all([
            torneo_id,
            equipo_local_id,
            equipo_visitante_id,
            fecha,
            estado
        ]):
            flash("Completa todos los campos obligatorios.", "danger")

        else:
            try:
                torneo = db.session.get(Torneo, int(torneo_id))
                equipo_local = db.session.get(Equipo, int(equipo_local_id))
                equipo_visitante = db.session.get(
                    Equipo, int(equipo_visitante_id)
                )

                if not torneo or not equipo_local or not equipo_visitante:
                    raise ValueError("Selecciona un torneo y equipos válidos.")

                if equipo_local.id == equipo_visitante.id:
                    raise ValueError(
                        "Un equipo no puede enfrentarse a sí mismo."
                    )

                if (
                    equipo_local not in torneo.equipos
                    or equipo_visitante not in torneo.equipos
                ):
                    raise ValueError(
                        "Ambos equipos deben estar inscritos en el torneo."
                    )

                fecha_partido = datetime.strptime(
                    fecha, "%Y-%m-%dT%H:%M"
                )

                estadio = None
                arbitro = None

                if estadio_id:
                    estadio = db.session.get(Estadio, int(estadio_id))
                    if not estadio or not estadio.estado:
                        raise ValueError("El estadio seleccionado"
                                         "no está disponible.")

                if arbitro_id:
                    arbitro = db.session.get(Arbitro, int(arbitro_id))
                    if not arbitro or not arbitro.estado:
                        raise ValueError("El árbitro seleccionado no"
                                         "está disponible.")

                partido = Partido(
                    torneo=torneo,
                    equipo_local=equipo_local,
                    equipo_visitante=equipo_visitante,
                    estadio=estadio,
                    arbitro=arbitro,
                    fecha=fecha_partido,
                    goles_local=0,
                    goles_visitante=0,
                    estado=estado
                )

                db.session.add(partido)
                db.session.commit()

                flash("Partido registrado correctamente.", "success")
                return redirect(url_for("partidos.index"))

            except ValueError as error:
                db.session.rollback()
                flash(str(error), "danger")

            except (TypeError, OverflowError):
                db.session.rollback()
                flash("Los datos seleccionados no son válidos.", "danger")

            except Exception:
                db.session.rollback()
                flash("No fue posible registrar el partido.", "danger")

    return render_template(
        "partidos/nuevo.html",
        torneos=torneos,
        estadios=estadios,
        arbitros=arbitros
    )


@partidos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    partido = db.session.get(Partido, id)

    if not partido:
        flash("El partido no existe.", "danger")
        return redirect(url_for("partidos.index"))

    torneos = Torneo.query.order_by(Torneo.nombre).all()
    estadios = Estadio.query.filter_by(estado=True).order_by(
        Estadio.nombre
    ).all()
    arbitros = Arbitro.query.filter_by(estado=True).order_by(
        Arbitro.nombre
    ).all()

    if request.method == "POST":

        torneo_id = request.form.get("torneo_id")
        equipo_local_id = request.form.get("equipo_local_id")
        equipo_visitante_id = request.form.get("equipo_visitante_id")
        estadio_id = request.form.get("estadio_id") or None
        arbitro_id = request.form.get("arbitro_id") or None
        fecha = request.form.get("fecha")
        estado = request.form.get("estado")

        print("DATOS RECIBIDOS:", request.form.to_dict())

        if not all([
            torneo_id,
            equipo_local_id,
            equipo_visitante_id,
            fecha,
            estado
        ]):
            flash("Faltan datos obligatorios para actualizar"
                  " el partido.", "danger")
            return redirect(url_for("partidos.editar", id=id))

        try:
            torneo = db.session.get(Torneo, int(torneo_id))
            equipo_local = db.session.get(Equipo, int(equipo_local_id))
            equipo_visitante = db.session.get(
                Equipo, int(equipo_visitante_id)
            )

            if not torneo or not equipo_local or not equipo_visitante:
                raise ValueError("Selecciona un torneo y equipos válidos.")

            if equipo_local.id == equipo_visitante.id:
                raise ValueError(
                    "Un equipo no puede enfrentarse a sí mismo."
                )

            if (
                equipo_local not in torneo.equipos
                or equipo_visitante not in torneo.equipos
            ):
                raise ValueError(
                    "Ambos equipos deben estar inscritos en el torneo."
                )

            fecha_partido = datetime.strptime(
                fecha, "%Y-%m-%dT%H:%M"
            )

            estadio = None
            arbitro = None

            if estadio_id:
                estadio = db.session.get(Estadio, int(estadio_id))
                if not estadio or not estadio.estado:
                    raise ValueError("El estadio seleccionado"
                                     "no está disponible.")

            if arbitro_id:
                arbitro = db.session.get(Arbitro, int(arbitro_id))
                if not arbitro or not arbitro.estado:
                    raise ValueError("El árbitro seleccionado"
                                     "no está disponible.")

            partido.torneo = torneo
            partido.equipo_local = equipo_local
            partido.equipo_visitante = equipo_visitante
            partido.estadio = estadio
            partido.arbitro = arbitro
            partido.fecha = fecha_partido
            partido.estado = estado

            db.session.commit()

            flash("Partido actualizado correctamente.", "success")
            return redirect(url_for("partidos.index"))

        except (ValueError, TypeError, OverflowError) as error:
            db.session.rollback()
            flash(str(error) or "Los datos ingresados"
                  "no son válidos.", "danger")

        except Exception:
            db.session.rollback()
            flash("No fue posible actualizar el partido.", "danger")

    return render_template(
        "partidos/editar.html",
        partido=partido,
        torneos=torneos,
        estadios=estadios,
        arbitros=arbitros
    )


@partidos_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    partido = db.session.get(Partido, id)

    if not partido:
        flash("El partido no existe.", "danger")
        return redirect(url_for("partidos.index"))

    db.session.delete(partido)
    db.session.commit()

    flash("Partido eliminado correctamente.", "success")

    return redirect(url_for("partidos.index"))
