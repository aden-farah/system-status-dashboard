import pytest

from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"System Status Dashboard" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["service"] == "system-status-dashboard"
    assert data["version"] == "1.0.0"


def test_metrics_endpoint(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"python_info" in response.data
    assert b"http_requests_total" in response.data