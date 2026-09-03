from abc import ABC, abstractmethod

from sqlalchemy import delete as delete_stmt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.movements import Movement
from app.models.products import Product
from app.models.users import User


class UsersRepositoryABC(ABC):
    @abstractmethod
    def create(self, user: User) -> User: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def delete(self, user: User) -> None: ...


class UserRepository(UsersRepositoryABC):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)

        return self.db.scalar(stmt)

    def get_by_id(self, id: int):
        return self.db.get(User, id)

    def save(self, user: User):
        self.db.merge(user)
        self.db.commit()

    def delete(self, user: User):
        product_ids: list[int] = []
        movement_ids: list[int] = []

        for product in user.products:
            product_ids.append(product.id)

            for movement in product.movements:
                movement_ids.append(movement.id)

        if movement_ids:
            stmt = delete_stmt(Movement).where(Movement.id.in_(movement_ids))
            self.db.execute(stmt)
        if product_ids:
            stmt = delete_stmt(Product).where(Product.id.in_(product_ids))
            self.db.execute(stmt)

        self.db.delete(user)
        self.db.commit()


def get_user_repository():
    return UserRepository(next(get_db()))
