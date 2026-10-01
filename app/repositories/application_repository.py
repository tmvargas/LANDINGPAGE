from sqlalchemy import select

from app.db import db
from app.models.application import Application, user_applications


class ApplicationRepository:
    def list_for_user(self, user_id: int) -> list[Application]:
        statement = (
            select(Application)
            .join(
                user_applications,
                Application.id == user_applications.c.application_id,
            )
            .where(Application.is_active.is_(True))
            .where(user_applications.c.user_id == user_id)
            .order_by(Application.sort_order, Application.name)
        )
        return list(db.session.scalars(statement).all())
