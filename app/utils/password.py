import re
from passlib.context import CryptContext
from fastapi import HTTPException


def is_secure_password(password: str) -> bool:
    """
    Check if a password is secure.

    A secure password must:
    - Be at least 8 characters long.
    - Contain at least one uppercase letter.
    - Contain at least one lowercase letter.
    - Contain at least one number.
    - Contain at least one special character.
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter.",
        )

    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter.",
        )

    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number."
        )

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character.",
        )

    return True


# Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Generate secure hashing"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the password matches"""
    return pwd_context.verify(plain_password, hashed_password)
