from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository | None = None):
        self.repository = repository or UserRepository()

    def authenticate(self, email: str, password: str):
        normalized_email = email.strip().lower()
        user = self.repository.find_active_by_email(normalized_email)
        if user is None or not user.check_password(password):
            return None
        return user
