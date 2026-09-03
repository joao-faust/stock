from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import UnauthorizedError
from app.core.settings import settings

auth_schema = OAuth2PasswordBearer(tokenUrl="/tokens")


class HasherABC(ABC):
    @abstractmethod
    def hash(self, plain_text: str) -> str: ...

    @abstractmethod
    def verify(self, plain_text: str, hash: str) -> bool: ...


class Argon2Hasher(HasherABC):
    def __init__(self, hasher: PasswordHasher):
        self.hasher = hasher

    def hash(self, plain_text: str):
        return self.hasher.hash(plain_text)

    def verify(self, plain_text: str, hash: str):
        try:
            self.hasher.verify(hash, plain_text)
            
            return True
        except VerifyMismatchError:
            return False


class DecodedToken:
    def __init__(self, id: int):
        self.id = id


class TokenManagerABC(ABC):
    @abstractmethod
    def create(self, id: int) -> str: ...

    @abstractmethod
    def decode(self, token: str) -> DecodedToken | None: ...


class JwtManager(TokenManagerABC):
    def __init__(self, secret: str, algorithm: str, expires_minutes: int):
        self.secret = secret
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes

    def create(self, id: int):
        now = datetime.now(timezone.utc)

        return jwt.encode(
            {
                "sub": str(id),
                "iat": now,
                "exp": now + timedelta(minutes=self.expires_minutes),
            },
            self.secret,
            self.algorithm,
        )

    def decode(self, token: str):
        try:
            payload = jwt.decode(token, self.secret, [self.algorithm])
            id = int(payload["sub"])

            return DecodedToken(id)
        except jwt.exceptions.InvalidTokenError:
            return None


def get_argon2_hasher():
    return Argon2Hasher(PasswordHasher())


def get_jwt_manager():
    return JwtManager(
        settings.jwt_secret,
        settings.jwt_algorithm,
        settings.jwt_expires_minutes,
    )


def decode_jwt(token: str = Depends(auth_schema)):
    if not token:
        raise UnauthorizedError("Missing token")

    manager = get_jwt_manager()

    decoded_token = manager.decode(token)

    if decoded_token is None:
        raise UnauthorizedError("Invalid token")

    return decoded_token
