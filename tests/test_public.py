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
