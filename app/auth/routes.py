from flask import render_template, request, redirect, url_for, flash

from app import db
from app.models.usuario import Usuario
from app.models.rol import Rol
from . import auth_bp


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
        if Usuario.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for("auth.register"))

        # Validar correo
        if Usuario.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("auth.register"))

        rol = Rol.query.filter_by(nombre="Usuario").first()

        usuario = Usuario(
            nombre=nombre,
            username=username,
            email=email,
            rol=rol
        )

        usuario.set_password(password)

        db.session.add(usuario)
        db.session.commit()

        flash("Usuario registrado correctamente.", "success")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/profile")
def profile():
    return render_template("auth/profile.html")
