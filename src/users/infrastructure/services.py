import bcrypt
from datetime import datetime, timedelta
import jwt
from typing import Optional

from ..domain.services import PasswordHashingService
from ..domain.value_objects import PlainPassword, HashedPassword


class BcryptPasswordHashingService(PasswordHashingService):
    def hash_password(self, plain_password: PlainPassword) -> HashedPassword:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.value.encode("utf-8"), salt)
        return HashedPassword(value=hashed.decode("utf-8"))

    def verify_password(
        self, plain_password: PlainPassword, hashed_password: HashedPassword
    ) -> bool:
        return bcrypt.checkpw(
            plain_password.value.encode("utf-8"), hashed_password.value.encode("utf-8")
        )


class JWTTokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        expires_delta: timedelta = timedelta(hours=24),
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_delta = expires_delta

    def create_access_token(self, user_id: int) -> str:
        expire = datetime.now() + self.expires_delta
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = int(payload.get("sub"))
            return user_id
        except (jwt.PyJWTError, ValueError):
            return None
