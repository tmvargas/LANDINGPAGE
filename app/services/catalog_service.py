from app.repositories.application_repository import ApplicationRepository


class CatalogService:
    def __init__(self, repository: ApplicationRepository | None = None):
        self.repository = repository or ApplicationRepository()

    def applications_for_user(self, user_id: int):
        return self.repository.list_for_user(user_id)
