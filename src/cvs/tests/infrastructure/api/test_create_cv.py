from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel

from shared.infrastructure.db_conf import engine
from main import app

client = TestClient(app)


class TestCvCreation:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_creates_cv_and_returns_200_ok(self):
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

        response = client.post("/api/cvs/", json=cv_input)
        assert response.status_code == 200
        assert response.json() == res
