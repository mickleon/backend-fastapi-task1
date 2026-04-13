import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserResponseSchema
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    WrongPasswordException,
)

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        username: str,
        password: str,
    ) -> UserResponseSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get(session=session, username=username)
        except UserNotFoundException:
            error = UserNotFoundByUsernameException(username=username)
            logger.error(error.get_detail())
            raise error

        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserResponseSchema.model_validate(obj=user)
