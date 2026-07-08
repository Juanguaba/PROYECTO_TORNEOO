from functools import wraps
from flask import flash, redirect, session, url_for


def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "usuario_id" not in session:

            flash("Debes iniciar sesión.", "warning")

            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def role_required(*roles):
    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if "usuario_rol" not in session:
                flash("Debes iniciar sesión.", "warning")
                return redirect(url_for("auth.login"))

            if session["usuario_rol"] not in roles:
                flash("No tienes permisos para acceder.", "danger")
                return redirect(url_for("main.index"))

            return view(*args, **kwargs)

        return wrapped_view

    return decorator
