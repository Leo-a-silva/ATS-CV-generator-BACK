import pytest
from users.domain.models import User
from users.domain.value_objects import UserEmailAddress, HashedPassword
from users.infrastructure.repositories import SQLModelUsersRepository, engine, UserModel
from sqlmodel import SQLModel, Session, select


class TestSQLModelCvRepository:
    @pytest.fixture(autouse=True)
    def clean_up_db(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
        yield
        SQLModel.metadata.drop_all(engine)

    def test_saves_user_to_database(self) -> None:
        repo = SQLModelUsersRepository()

        repo.save(
            User(
                first_name="Steve",
                last_name="Jobs",
                email_address=UserEmailAddress(value="steve.jobs@example.com"),
                hashed_password=HashedPassword(value="fakehashingPassword1"),
            )
        )

        with Session(engine) as session:
            statement = select(UserModel)
            user = session.exec(statement).first()
            assert user.first_name == "Steve"
            assert user.email_address == "steve.jobs@example.com"
