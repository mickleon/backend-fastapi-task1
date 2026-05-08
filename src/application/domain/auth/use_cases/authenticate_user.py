import logging

from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.user import (
    UserRepository,
)
from application.schemas.user import UserResponseSchema
from application.resources.auth import verify_password
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    WrongUsernameOrPasswordException,
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
            async with self._database.session() as session:
                user = await self._repo.get(session=session, username=username)
        except UserNotFoundException:
            error = WrongUsernameOrPasswordException()
            logger.error(error.get_detail())
            raise error

        if not verify_password(
            plain_password=password, hashed_password=user.password
        ):
            error = WrongUsernameOrPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserResponseSchema.model_validate(obj=user)
