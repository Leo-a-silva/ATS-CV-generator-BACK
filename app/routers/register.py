from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserResponse, UserCreate
from ..crud.create_user import create_user
from ..utils.password import hash_password, is_secure_password

router = APIRouter()


@router.post("/register/", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if password is secure
    is_secure_password(user_data.password_hash)

    # Hash
    hashed_password = hash_password(user_data.password_hash)
    user_data.password_hash = hashed_password

    return create_user(db=db, user_data=user_data)
