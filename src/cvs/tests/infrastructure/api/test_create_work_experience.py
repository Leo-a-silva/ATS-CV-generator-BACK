from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel
from fastapi import FastAPI

from shared.infrastructure.db_conf import engine


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
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_creates_work_education_and_returns_200_ok(self):
        # Create fake user
        request_user_data = {
            "email_address": "test@example.com",
            "password": "Secure_password123",
        }

        client.post("/api/users/register/", json=request_user_data)

        # Create fake cv
        request_cv_data = {
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

        client.post("/api/cvs/create/", json=request_cv_data)

        # Create Work Experience
        request_we_data = [
            {
                "cv_id": 1,
                "role": "Dev Ops",
                "company_name": "Share IT",
                "summary": "Design and implemented CI/CD Pipelines.",
                "start_date": "2023-06-24",
                "end_date": "2024-06-24",
            }
        ]

        success_response = [
            {
                "role": "Dev Ops",
                "company_name": "Share IT",
                "summary": "Design and implemented CI/CD Pipelines.",
                "start_date": "2023-06-24",
                "end_date": "2024-06-24",
            }
        ]

        response = client.post("/api/cvs/work-experience", json=request_we_data)
        assert response.json() == success_response
        assert response.status_code == 201
