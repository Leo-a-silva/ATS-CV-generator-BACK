from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_returns_200_ok():
    response = client.get("/api/health/")
    assert response.status_code == 200
    assert response.json() == {"detail": "ok"}
