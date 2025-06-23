import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from shared.infrastructure.db_conf import engine


def create_test_app():
    from users.infrastructure.api.routes import router

    app = FastAPI()

    app.include_router(router, prefix="/api")

    return app


app = create_test_app()


client = TestClient(app)


class TestUserCreation:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_creates_user_and_returns_201_ok(self):
        request_data = {
            "email_address": "test@example.com",
            "password": "Secure_password123",
        }

        response = client.post("/api/users/register", json=request_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email_address"] == request_data["email_address"]
        assert "user_id" in data
        assert "created_at" in data

    def test_register_user_with_existing_email(self):
        request_data = {
            "email_address": "existing@example.com",
            "password": "Secure_password123",
        }

        # Create first user
        client.post("/api/users/register", json=request_data)

        # Try to create second user with same email
        response = client.post("/api/users/register", json=request_data)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_register_user_with_invalid_email(self):
        request_data = {
            "email_address": "invalid-email",
            "password": "Secure_password123",
        }

        response = client.post("/api/users/register", json=request_data)
        assert response.status_code == 422
        assert (
            "value is not a valid email address" in response.json()["detail"][0]["msg"]
        )
