import re
from unittest.mock import patch

from app import create_app


def test_home_preserves_public_content():
    app = create_app("testing")
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Gestão inteligente" in response.text
    assert "Acessar aplicações" in response.text


def test_health_does_not_depend_on_database():
    app = create_app("testing")
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_invalid_login_with_valid_csrf_returns_feedback():
    app = create_app("testing")
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()

    login_page = client.get("/acesso/login")
    token = re.search(r'name="csrf_token"[^>]+value="([^"]+)"', login_page.text).group(1)

    with patch("app.controllers.auth_controller.AuthService.authenticate", return_value=None):
        response = client.post(
            "/acesso/login",
            data={
                "csrf_token": token,
                "email": "thiago@example.com",
                "password": "senha-incorreta",
            },
        )

    assert response.status_code == 200
    assert "E-mail ou senha inválidos." in response.text
