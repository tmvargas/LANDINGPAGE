import re
import os
from unittest.mock import patch

from app import create_app


def test_home_preserves_public_content():
    app = create_app("testing")
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert "Consultoria + Tecnologia" in response.text
    assert "Plataforma de Inteligência" in response.text
    assert "Contabilidade" in response.text
    assert 'href="#consultoria"' in response.text
    assert 'href="#produtos"' in response.text
    assert 'href="#sistemas"' in response.text
    assert "Dashboard de Gestão Integrada" in response.text
    assert "Sistemas sob demanda" in response.text
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


def test_login_accepts_six_character_password_for_legacy_account():
    app = create_app("testing")
    client = app.test_client()

    with patch("app.controllers.auth_controller.AuthService.authenticate", return_value=None) as authenticate:
        response = client.post(
            "/acesso/login",
            data={"email": "thiago@example.com", "password": "123456"},
        )

    assert response.status_code == 200
    authenticate.assert_called_once_with("thiago@example.com", "123456")


def test_staging_prefix_is_applied_to_generated_urls():
    app = create_app("testing")
    client = app.test_client()

    response = client.get(
        "/",
        headers={"X-Forwarded-Prefix": "/staging/landingpage"},
    )

    assert response.status_code == 200
    assert 'href="/staging/landingpage/acesso/login"' in response.text
    assert 'href="/staging/landingpage/static/css/styles.css"' in response.text


def test_staging_environment_allows_session_cookie_over_http():
    with patch.dict(os.environ, {"APP_ENV": "staging"}):
        app = create_app()

    assert app.config["SESSION_COOKIE_SECURE"] is False
    assert app.config["SESSION_COOKIE_NAME"] == "landingpage_session"
    assert app.config["SESSION_COOKIE_PATH"] == "/staging/landingpage"
    assert app.config["TESTING"] is False


def test_missing_csrf_session_redirects_to_login_with_friendly_feedback():
    app = create_app("testing")
    app.config["WTF_CSRF_ENABLED"] = True
    first_browser = app.test_client()
    token = re.search(
        r'name="csrf_token"[^>]+value="([^"]+)"',
        first_browser.get("/acesso/login").text,
    ).group(1)

    # Simula o envio por outra sessão, como ocorre quando outro sistema
    # sobrescreve o cookie compartilhado no host de staging.
    response = app.test_client().post(
        "/acesso/login?next=/apresentacao/consultoria",
        data={"csrf_token": token, "email": "thiago@example.com", "password": "123456"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Sua sessão expirou. Entre novamente para continuar." in response.text
    assert "Bad Request" not in response.text
