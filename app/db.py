from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Entre para acessar suas aplicações."


@login_manager.user_loader
def load_user(user_id: str):
    from app.repositories.user_repository import UserRepository

    if not user_id.isdigit():
        return None
    return UserRepository().find_active_by_id(int(user_id))
