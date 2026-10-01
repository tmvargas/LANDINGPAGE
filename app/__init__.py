from flask import Flask

from app.config import config_by_name
from app.db import bcrypt, csrf, db, login_manager, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    selected_config = config_name or app.config.get("ENV", "production")
    app.config.from_object(config_by_name.get(selected_config, config_by_name["production"]))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Garante que todos os models façam parte do metadata usado pelo Alembic.
    from app import models  # noqa: F401

    from app.controllers.auth_controller import auth_bp
    from app.controllers.public_controller import public_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)

    return app
