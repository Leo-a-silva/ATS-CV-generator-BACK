from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.user import User
from ..schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate) -> User:
    # Validate email
    existing_user = (
        db.query(User).filter(User.email_address == user_data.email_address).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email_address=user_data.email_address,
        password_hash=user_data.password_hash,
    )

    # Save
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
