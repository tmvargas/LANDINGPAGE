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
    assert "Desenvolvimento de sistemas e rotinas sob demanda" in response.text
    assert "Planilhas de tabulação" in response.text
    assert "PS Finance" in response.text
    assert "Configurações e Parametrizações" in response.text
    assert "Configurações de base" in response.text
    assert "Estruturas de controle" in response.text
    assert "Estruturas hierárquicas" in response.text
    assert "Parâmetros gerais do Sienge" in response.text
    assert "Voltar ao sistema solar" in response.text
    assert 'data-space-target="financeiro"' in response.text
    assert 'data-space-view="visao-geral"' in response.text
    assert response.text.count('class="scope-index-planet ') == 11
    assert response.text.count('class="planet planet-') == 24
    expected_orbital_order = [
        "seguranca",
        "configuracoes",
        "processos",
        "engenharia",
        "suprimentos",
        "comercial",
        "financeiro",
        "automacao",
        "gerencial",
        "contabilidade",
        "desenvolvimento",
    ]
    orbital_positions = [
        response.text.index(f'data-space-target="{slug}"')
        for slug in expected_orbital_order
    ]
    assert orbital_positions == sorted(orbital_positions)
    assert "Selecione um núcleo para viajar" not in response.text
    assert 'aria-label="Áreas da apresentação"' not in response.text
    assert "presentation.css?v=20261022c" in response.text
    assert 'class="spacecraft"' in response.text
    assert 'class="flight-path"' in response.text
    assert 'class="warp-burst"' in response.text
    assert 'class="arrival-flash"' in response.text
    assert 'class="cosmic-streak cosmic-streak-one"' in response.text
    assert response.text.count('role="button" data-presentation-card') == 24
    assert 'data-card-focus aria-hidden="true"' in response.text
    assert "Detalhamento do sistema" in response.text
    assert "const openCard = card" in response.text
    assert "prefers-reduced-motion: reduce" in response.text
    assert "const flyTo = async link" in response.text
    assert "Os 10 núcleos representam" not in response.text
    assert 'class="scope-index-orbit"' in response.text
    assert 'class="scope-core-mark"' not in response.text
    assert "Agendar" not in response.text
    access.assert_called_once_with(1, "consultoria-ps")
