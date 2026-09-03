from abc import ABC, abstractmethod

from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import DecodedToken, HasherABC, get_argon2_hasher
from app.models.users import User
from app.repositories.users import UsersRepositoryABC, get_user_repository
from app.schemas.users import DeleteSchema, RegisterSchema, UpdateUserSchema


class UsersServiceABC(ABC):
    @abstractmethod
    def create(self, data: RegisterSchema) -> User: ...

    @abstractmethod
    def get_by_id(self, id: int) -> User: ...

    @abstractmethod
    def update(self, data: UpdateUserSchema, decoded_token: DecodedToken) -> None: ...

    @abstractmethod
    def delete(self, data: DeleteSchema, decoded_token: DecodedToken) -> None: ...

    @abstractmethod
    def validate_email_available(self, email: str, user_id: int | None = None) -> None: ...

    @abstractmethod
    def validate_password(self, password: str, password_hash: str) -> None: ...


class UserService(UsersServiceABC):
    def __init__( self, user_repository: UsersRepositoryABC, hasher: HasherABC):
        self.user_repository = user_repository
        self.hasher = hasher

    def create(self, data: RegisterSchema):
        if data.confirm_password != data.password:
            raise ValidationError("Passwords don't match")

        self.validate_email_available(data.email)

        user = User()
        user.name = data.name
        user.email = data.email
        user.password = self.hasher.hash(data.password)

        return self.user_repository.create(user)

    def get_by_id(self, id: int):
        user = self.user_repository.get_by_id(id)

        if not user:
            raise NotFoundError("User not found")

        return user

    def update(self, data: UpdateUserSchema, decoded_token: DecodedToken):
        user = self.get_by_id(decoded_token.id)

        self.validate_password(data.password, user.password)
        self.validate_email_available(data.email, user.id)

        user.name = data.name
        user.email = data.email

        self.user_repository.save(user)

    def delete(self, data: DeleteSchema, decoded_token: DecodedToken):
        user = self.get_by_id(decoded_token.id)

        self.validate_password(data.password, user.password)

        self.user_repository.delete(user)

    def validate_email_available(self, email: str, user_id: int | None = None):
        user = self.user_repository.get_by_email(email)

        if user and user.id != user_id:
            raise ValidationError("Email in use")

    def validate_password(self, password: str, password_hash: str):
        if not self.hasher.verify(password, password_hash):
            raise ValidationError("Invalid password")


def get_user_service():
    return UserService(get_user_repository(), get_argon2_hasher())
