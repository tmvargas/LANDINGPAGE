import os

from flask import Flask, flash, redirect, request, url_for
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import config_by_name
from app.db import bcrypt, csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    selected_config = config_name or os.getenv("APP_ENV", "production")
    app.config.from_object(config_by_name.get(selected_config, config_by_name["production"]))
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Garante que todos os models façam parte do metadata usado pelo Alembic.
    from app import models  # noqa: F401

    from app.controllers.auth_controller import auth_bp
    from app.controllers.presentation_controller import presentation_bp
    from app.controllers.public_controller import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(presentation_bp)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(_error):
        # Uma aba antiga ou um cookie substituído não deve expor um 400 técnico.
        # Reinicia a sessão pelo formulário, preservando o destino solicitado.
        flash("Sua sessão expirou. Entre novamente para continuar.", "error")
        next_url = request.args.get("next")
        return redirect(url_for("auth.login", next=next_url) if next_url else url_for("auth.login"))

    return app
