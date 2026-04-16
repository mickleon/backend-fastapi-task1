import logging

from src.core.exceptions.database_exceptions import (
    UserUsernameAlreadyExistsException,
    UserEmailAlreadyExistsException,
)
from src.core.exceptions.domain_exceptions import (
    UserUsernameOrEmailIsNotUniqueException,
)
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.user import UserRepository
from src.schemas.user import UserRequestSchema, UserResponseSchema
from src.resources.auth import get_password_hash

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        data: UserRequestSchema,
        current_user: UserResponseSchema | None,
    ) -> UserResponseSchema:
        data.password = get_password_hash(password=data.password)
        with self._database.session() as session:
            try:
                user = self._repo.create(session=session, data=data)
            except UserUsernameAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_username(
                    username=data.username
                )
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
            except UserEmailAlreadyExistsException:
                error = UserUsernameOrEmailIsNotUniqueException.from_email(
                    email=data.email
                )
                username = (
                    current_user.username
                    if current_user is not None
                    else 'анонимный'
                )
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return UserResponseSchema.model_validate(obj=user)
