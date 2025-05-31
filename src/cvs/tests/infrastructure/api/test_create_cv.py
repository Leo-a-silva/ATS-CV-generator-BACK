from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_creates_cv_and_returns_200_ok():
    cv_input = {
        "user_id": 1,
        "first_name": "Alex",
        "last_name": "Caniggia",
        "email_address": "alex.caniggia@example.com",
        "phone_number": "+543434586789",
        "linkedin_url": "https://linkedin.com/",
        "portfolio_url": "https://ats.com/",
        "country": "ARG",
        "city": "Buenos Aires",
        "summary": "Star",
    }

    res = {
        "first_name": "Alex",
        "last_name": "Caniggia",
        "email_address": "alex.caniggia@example.com",
        "phone_number": "+543434586789",
        "linkedin_url": "https://linkedin.com/",
        "portfolio_url": "https://ats.com/",
        "country": "ARG",
        "city": "Buenos Aires",
        "summary": "Star",
    }

    response = client.post("/cvs/", json=cv_input)
    assert response.status_code == 200
    assert response.json() == res
