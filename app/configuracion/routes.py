
import re

from flask import render_template, request, redirect, url_for, flash

from app import db
from app.models import Configuracion

from . import configuracion_bp


def obtener_configuracion():

    configuracion = Configuracion.query.first()

    if not configuracion:
        configuracion = Configuracion()
        db.session.add(configuracion)
        db.session.commit()

    return configuracion


@configuracion_bp.route("/")
def index():

    configuracion = obtener_configuracion()

    return render_template(
        "configuracion/index.html",
        configuracion=configuracion
    )


@configuracion_bp.route("/guardar", methods=["POST"])
def guardar():

    configuracion = obtener_configuracion()

    try:

        # Identidad del sistema
        nombre = request.form.get(
            "nombre_sistema", ""
        ).strip()

        descripcion = request.form.get(
            "descripcion", ""
        ).strip()

        organizacion = request.form.get(
            "organizacion", ""
        ).strip()

        # Contacto
        email = request.form.get(
            "email_contacto", ""
        ).strip().lower()

        telefono = request.form.get(
            "telefono_contacto", ""
        ).strip()

        # Preferencias deportivas
        duracion = int(
            request.form.get("duracion_partido", 90)
        )

        descanso = int(
            request.form.get("descanso", 15)
        )

        puntos_victoria = int(
            request.form.get("puntos_victoria", 3)
        )

        puntos_empate = int(
            request.form.get("puntos_empate", 1)
        )

        puntos_derrota = int(
            request.form.get("puntos_derrota", 0)
        )

        color = request.form.get(
            "color_principal", "#126B48"
        ).strip()

        # Validaciones generales
        if not nombre:
            raise ValueError(
                "El nombre del sistema es obligatorio."
            )

        if len(nombre) > 120:
            raise ValueError(
                "El nombre del sistema no puede superar 120 caracteres."
            )

        if len(descripcion) > 300:
            raise ValueError(
                "La descripción no puede superar 300 caracteres."
            )

        if len(organizacion) > 150:
            raise ValueError(
                "El nombre de la organización no puede superar 150 caracteres."
            )

        if len(email) > 120 or (
            email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
        ):
            raise ValueError(
                "Ingresa un correo electrónico válido."
            )

        if len(telefono) > 30:
            raise ValueError(
                "El teléfono no puede superar 30 caracteres."
            )

        if not 1 <= duracion <= 180:
            raise ValueError(
                "La duración del partido debe estar entre 1 y 180 minutos."
            )

        if not 0 <= descanso <= 60:
            raise ValueError(
                "El descanso debe estar entre 0 y 60 minutos."
            )

        if not 0 <= puntos_victoria <= 10:
            raise ValueError(
                "Los puntos por victoria deben estar entre 0 y 10."
            )

        if not 0 <= puntos_empate <= 10:
            raise ValueError(
                "Los puntos por empate deben estar entre 0 y 10."
            )

        if not 0 <= puntos_derrota <= 10:
            raise ValueError(
                "Los puntos por derrota deben estar entre 0 y 10."
            )

        if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
            raise ValueError(
                "Selecciona un color hexadecimal válido."
            )

        # Guardar identidad
        configuracion.nombre_sistema = nombre
        configuracion.descripcion = descripcion
        configuracion.organizacion = organizacion

        # Guardar contacto
        configuracion.email_contacto = email or None
        configuracion.telefono_contacto = telefono or None

        # Guardar preferencias deportivas
        configuracion.duracion_partido = duracion
        configuracion.descanso = descanso
        configuracion.puntos_victoria = puntos_victoria
        configuracion.puntos_empate = puntos_empate
        configuracion.puntos_derrota = puntos_derrota

        # Guardar apariencia
        configuracion.color_principal = color

        db.session.commit()

        flash(
            "La configuración se actualizó correctamente.",
            "success"
        )

    except ValueError as error:

        db.session.rollback()

        flash(str(error), "danger")

    except Exception:

        db.session.rollback()

        flash(
            "No fue posible guardar la configuración.",
            "danger"
        )

    return redirect(url_for("configuracion.index"))
