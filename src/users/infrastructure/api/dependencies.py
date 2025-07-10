from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.users.infrastructure.services import JWTTokenService
from src.shared.infrastructure.jwt import SECRET_KEY

security = HTTPBearer()


def get_jwt_token_service() -> JWTTokenService:
    return JWTTokenService(secret_key=SECRET_KEY)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    token_service: JWTTokenService = Depends(get_jwt_token_service),
) -> int:
    token = credentials.credentials
    user_id = token_service.decode_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_id
