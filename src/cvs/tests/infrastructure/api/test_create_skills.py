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


class TestSkillCreation:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_creates_skills_and_returns_201_ok(self):
        # Create fake user
        request_user_data = {
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "test@example.com",
            "password": "Secure_password123",
        }

        client.post("/api/users/register/", json=request_user_data)

        # Create fake CV
        request_cv_data = {
            "user_id": 1,
            "cv": {
                "first_name": "Steve",
                "last_name": "Jobs",
                "email_address": "steve.jobs@example.com",
                "phone_number": "+543434586789",
                "linkedin_url": "https://linkedin.com/",
                "portfolio_url": "https://ats.com/",
                "country": "ARG",
                "city": "Buenos Aires",
                "summary": "Star",
            },
        }

        client.post("/api/cvs/create/", json=request_cv_data)

        # Create Skills
        request_skill_data = {
            "cv_id": 1,
            "skills": ["Python", "Javascript", "React", "FastAPI"],
        }

        success_response = {
            "detail": {"message": "Skills saved successfully"},
            "data": {
                "cv_id": 1,
                "description": ["Python", "Javascript", "React", "FastAPI"],
            },
        }

        response = client.post("/api/cvs/skills/", json=request_skill_data)
        assert response.status_code == 201
        assert response.json() == success_response