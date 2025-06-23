from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, select, Session

from ..domain.value_objects import HashedPassword, Id, UserEmailAddress

from ..domain.repositories import UsersRepository
from ..domain.models import User

from shared.infrastructure.db_conf import engine


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    __table_args__ = {"extend_existing": True}

    id: int | None = Field(default=None, primary_key=True)
    email_address: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class SQLModelUsersRepository(UsersRepository):
    def all(self) -> list[User]:
        with Session(engine) as session:
            statement = select(UserModel)
            results = session.exec(statement).all()
            return [self._to_domain_modal(user_model) for user_model in results]

    def find_by_id(self, user_id: int) -> Optional[User]:
        with Session(engine) as session:
            user_model = session.get(UserModel, user_id.value)
            return self._to_domain_model(user_model) if user_model else None

    def find_by_email(self, email: UserEmailAddress) -> Optional[User]:
        statement = select(UserModel).where(UserModel.email_address == email.value)
        with Session(engine) as session:
            user_model = session.exec(statement).first()
            return self._to_domain_model(user_model) if user_model else None

    def exists_by_email(self, email: UserEmailAddress) -> bool:
        statement = select(UserModel).where(UserModel.email_address == email.value)
        with Session(engine) as session:
            return session.exec(statement).first() is not None

    def save(self, user: User) -> None:
        if not user.is_persisted():
            return self._create_user(user)
        else:
            return self._update_user(user)

    def _create_user(self, user: User) -> User:
        user_model = UserModel(
            email_address=user.email_address().value,
            hashed_password=user.hashed_password().value,
            created_at=user.created_at(),
            updated_at=user.updated_at(),
        )

        with Session(engine) as session:
            session.add(user_model)
            session.commit()
            session.refresh(user_model)

        return self._to_domain_model(user_model)

    def _update_user(self, user: User) -> User:
        if not user.id():
            raise ValueError("Cannot update user without ID")

        with Session(engine) as session:
            user_model = session.get(UserModel, user.id().value)
            if not user_model:
                raise ValueError(f"User with id {user.id().value} not found")

            user_model.email_address = user.email_address().value
            user_model.hashed_password = user.hashed_password().value
            user_model.updated_at = user.updated_at()

            session.commit()
            session.refresh(user_model)

        return self._to_domain_model(user_model)

    def _to_domain_model(self, user_model: UserModel) -> User:
        return User.from_persistence(
            id=Id(value=user_model.id),
            email_address=UserEmailAddress(value=user_model.email_address),
            hashed_password=HashedPassword(value=user_model.hashed_password),
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )
