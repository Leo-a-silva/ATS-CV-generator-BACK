from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel
from fastapi import FastAPI

from shared.infrastructure.db_conf import engine

from src.shared.infrastructure.logger_conf import logger


def create_test_app():
    from src.cvs.infrastructure.api.router import router as cvs_router
    from src.users.infrastructure.api.routes import router as users_router

    app = FastAPI()
    app.include_router(cvs_router, prefix="/api", tags=["CVs"])
    app.include_router(users_router, prefix="/api", tags=["Users"])
    return app


app = create_test_app()

client = TestClient(app)


class TestCvCreation:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_creates_cv_and_returns_200_ok(self):
        # Create fake user
        request_data = {
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "test@example.com",
            "password": "Secure_password123",
        }

        client.post("/api/users/register/", json=request_data)

        request_login = {
            "email_address": "test@example.com",
            "password": "Secure_password123",
        }

        login_response = client.post("/api/users/login/", json=request_login)

        # Create CV
        cv_input = {
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@example.com",
            "phone_number": "+543434586789",
            "linkedin_url": "https://linkedin.com/",
            "portfolio_url": "https://ats.com/",
            "country": "ARG",
            "city": "Buenos Aires",
            "summary": "Star",
        }

        res = {
            "detail": {"message": "Cv created succesfully"},
            "data": {
                "cv_id": 1,
                "user_id": 1,
                "description": [
                    {
                        "first_name": "Steve",
                        "last_name": "Jobs",
                        "email_address": "steve.jobs@example.com",
                        "phone_number": "+543434586789",
                        "linkedin_url": "https://linkedin.com/",
                        "portfolio_url": "https://ats.com/",
                        "country": "ARG",
                        "city": "Buenos Aires",
                        "summary": "Star",
                    }
                ],
            },
        }

        headers = {
            "Authorization": f"Bearer {(login_response.json())['data']['access_token']}"
        }

        response = client.post("/api/cvs/create/", json=cv_input, headers=headers)
        assert response.json() == res
        assert response.status_code == 201
