from fastapi import FastAPI
from fastapi.testclient import TestClient


def create_test_app():
    from users.infrastructure.api.routes import router

    app = FastAPI()

    app.include_router(router, prefix="/api")

    return app


app = create_test_app()


client = TestClient(app)


class TestUserLogin:
    def test_login_and_returns_200_ok(self):
        test_user = {
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@gmail.com",
            "password": "IloveApples99!",
        }
        client.post("/api/users/register/", json=test_user)

        request_data = {
            "email_address": "steve.jobs@gmail.com",
            "password": "IloveApples99!",
        }

        response = client.post("/api/users/login/", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert (
            data["data"]["description"][0]["email_address"]
            == request_data["email_address"]
        )
        assert "user_id" in data["data"]
        assert "access_token" in data["data"]

    def test_login_using_wrong_password_and_returns_401_unauthorized(self):
        test_user = {
            "first_name": "Steve",
            "last_name": "Jobs",
            "email_address": "steve.jobs@gmail.com",
            "password": "IloveApples99!",
        }
        client.post("/api/users/register/", json=test_user)

        request_data = {
            "email_address": "steve.jobs@gmail.com",
            "password": "IloveWindows98!",
        }

        response = client.post("/api/users/login/", json=request_data)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "The password that you've entered is incorrect."
