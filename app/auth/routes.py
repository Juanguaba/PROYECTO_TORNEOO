from flask import render_template, request, redirect, url_for, flash

from flask import session
from .services import autenticar_usuario
from app.models.usuario import Usuario
from .decorators import login_required
from . import auth_bp
from .services import (
    buscar_usuario_por_email,
    buscar_usuario_por_username,
    crear_usuario
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nombre = request.form["nombre"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmar = request.form["confirmar"]

        # Validar contraseña
        if password != confirmar:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("auth.register"))

        # Validar usuario
        if buscar_usuario_por_username(username):
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for("auth.register"))

        # Validar correo
        if buscar_usuario_por_email(email):
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("auth.register"))

        crear_usuario(nombre, username, email, password)

        flash("Usuario registrado correctamente.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario_o_email = request.form["usuario"]
        password = request.form["password"]

        usuario = autenticar_usuario(
            usuario_o_email,
            password
        )

        if usuario:

            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            session["usuario_rol"] = usuario.rol.nombre

            flash("Bienvenido.", "success")

            return redirect(url_for("auth.profile"))

        flash("Credenciales incorrectas.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/profile")
@login_required
def profile():

    usuario = Usuario.query.get(session["usuario_id"])

    return render_template(
        "auth/profile.html",
        usuario=usuario
    )


@auth_bp.route("/logout")
@login_required
def logout():

    session.clear()

    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("auth.login"))
