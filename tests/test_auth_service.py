from types import SimpleNamespace

from app.services.auth_service import AuthService


class FakeUserRepository:
    def __init__(self, user):
        self.user = user
        self.received_email = None

    def find_active_by_email(self, email):
        self.received_email = email
        return self.user


def test_authenticate_normalizes_email_and_accepts_valid_password():
    user = SimpleNamespace(check_password=lambda password: password == "segura-123")
    repository = FakeUserRepository(user)

    result = AuthService(repository).authenticate(" Thiago@PlanSmart.com.br ", "segura-123")

    assert result is user
    assert repository.received_email == "thiago@plansmart.com.br"


def test_authenticate_rejects_invalid_password():
    user = SimpleNamespace(check_password=lambda _password: False)

    result = AuthService(FakeUserRepository(user)).authenticate("user@example.com", "incorreta")

    assert result is None
