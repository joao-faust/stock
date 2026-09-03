from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.users import User


class TokenRepositoryABC(ABC):
    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None: ...


class TokenRepository(TokenRepositoryABC):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)

        return self.db.scalar(stmt)


def get_token_repository():
    return TokenRepository(next(get_db()))
