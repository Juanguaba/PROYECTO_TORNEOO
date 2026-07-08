from flask import render_template

from app.auth.decorators import login_required, role_required
from . import admin_bp


@admin_bp.route("/")
@login_required
@role_required("Administrador")
def dashboard():
    return render_template("admin/dashboard.html")
