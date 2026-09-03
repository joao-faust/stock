from abc import ABC, abstractmethod

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    DecodedToken,
    HasherABC,
    TokenManagerABC,
    get_argon2_hasher,
    get_jwt_manager,
)
from app.models.users import User
from app.repositories.tokens import (
    TokenRepositoryABC,
    get_token_repository,
)
from app.schemas.tokens import CreateTokenSchema
from app.services.users import UsersServiceABC, get_user_service


class TokenServiceABC(ABC):
    @abstractmethod
    def create(self, data: CreateTokenSchema) -> str: ...

    @abstractmethod
    def get_user(self, decoded_token: DecodedToken) -> User: ...


class TokenService(TokenServiceABC):
    def __init__(
        self,
        token_repository: TokenRepositoryABC,
        user_service: UsersServiceABC,
        token_manager: TokenManagerABC,
        hasher: HasherABC,
    ):
        self.token_repository = token_repository
        self.user_service = user_service
        self.token_manager = token_manager
        self.hasher = hasher

    def create(self, data: CreateTokenSchema):
        user = self.token_repository.get_user_by_email(data.email)

        if not user or not self.hasher.verify(data.password, user.password):
            raise UnauthorizedError("Invalid credentials")

        return self.token_manager.create(user.id)

    def get_user(self, decoded_token: DecodedToken):
        return self.user_service.get_by_id(decoded_token.id)


def get_token_service():
    return TokenService(
        get_token_repository(),
        get_user_service(),
        get_jwt_manager(),
        get_argon2_hasher(),
    )
