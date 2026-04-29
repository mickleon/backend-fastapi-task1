import logging

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    UserUsernameOrEmailIsNotUniqueException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.user import (
    UserRepository,
)
from application.schemas.user import UserRequestSchema, UserResponseSchema

logger = logging.getLogger(__name__)


class UpdateUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        target_username: str,
        data: UserRequestSchema,
        current_user: UserResponseSchema,
    ) -> UserResponseSchema:
        async with self._database.session() as session:
            try:
                user = await self._repo.update(
                    session=session, username=target_username, data=data
                )
            except UserNotFoundException:
                error = UserNotFoundByUsernameException(
                    username=target_username
                )
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except UserUsernameAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_username(
                    username=data.username
                )
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except UserEmailAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return UserResponseSchema.model_validate(obj=user)
