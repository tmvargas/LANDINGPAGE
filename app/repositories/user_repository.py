from sqlalchemy import select

from app.db import db
from app.models.user import User


class UserRepository:
    def find_active_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id, User.is_active_account.is_(True))
        return db.session.scalar(statement)

    def find_active_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email, User.is_active_account.is_(True))
        return db.session.scalar(statement)
