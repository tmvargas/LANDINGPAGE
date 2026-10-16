from unittest.mock import patch

from flask_login import FlaskLoginClient

from app import create_app
from app.models.user import User


def _authenticated_client():
    app = create_app("testing")
    app.test_client_class = FlaskLoginClient
    user = User(
        id=1,
        email="thiago@example.com",
        name="Thiago",
        password_hash="unused",
        is_active_account=True,
    )
    client = app.test_client(user=user)
    return client, user


def test_consulting_presentation_requires_login():
    app = create_app("testing")
    client = app.test_client()

    response = client.get("/apresentacao/consultoria")

    assert response.status_code == 302
    assert "/acesso/login" in response.headers["Location"]
    assert "next=" in response.headers["Location"]


def test_consulting_presentation_denies_user_without_entitlement():
    client, user = _authenticated_client()

    with (
        patch("app.repositories.user_repository.UserRepository.find_active_by_id", return_value=user),
        patch("app.controllers.presentation_controller.CatalogService.user_can_access", return_value=False),
    ):
        response = client.get("/apresentacao/consultoria")

    assert response.status_code == 403


def test_consulting_presentation_renders_for_authorized_user():
    client, user = _authenticated_client()

    with (
        patch("app.repositories.user_repository.UserRepository.find_active_by_id", return_value=user),
        patch("app.controllers.presentation_controller.CatalogService.user_can_access", return_value=True) as access,
    ):
        response = client.get("/apresentacao/consultoria")

    assert response.status_code == 200
    assert "sistemas conectados" in response.text
    assert "Automação nativa Sienge" in response.text
    assert "Engenharia e controle de custo" in response.text
    assert "Contas a pagar" in response.text
    assert "Pagamento escritural e DDA" in response.text
    assert "Contratos e medições" in response.text
    assert "Voltar ao sistema solar" in response.text
    assert 'data-space-target="financeiro"' in response.text
    assert 'data-space-view="visao-geral"' in response.text
    assert "Agendar" not in response.text
    access.assert_called_once_with(1, "consultoria-ps")
