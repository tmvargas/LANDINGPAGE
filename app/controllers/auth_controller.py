from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import LoginForm
from app.services.auth_service import AuthService
from app.services.catalog_service import CatalogService


auth_bp = Blueprint("auth", __name__, url_prefix="/acesso")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.applications"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService().authenticate(form.email.data, form.password.data)
        if user is not None:
            login_user(user)
            return redirect(url_for("auth.applications"))
        flash("E-mail ou senha inválidos.", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.get("/aplicacoes")
@login_required
def applications():
    items = CatalogService().applications_for_user(current_user.id)
    return render_template("auth/applications.html", applications=items)


@auth_bp.post("/sair")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))
