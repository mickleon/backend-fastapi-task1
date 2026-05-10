import logging

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserUsernameAlreadyExistsException,
)
from application.core.exceptions.domain_exceptions import (
    UserUsernameOrEmailIsNotUniqueException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.user import (
    UserRepository,
)
from application.resources.auth import get_password_hash
from application.schemas.user import (
    UserRequestAdminSchema,
    UserResponseSchema,
)

logger = logging.getLogger(__name__)


class CreateUserAdminUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        data: UserRequestAdminSchema,
        current_user: UserResponseSchema | None,
    ) -> UserResponseSchema:
        data.password = get_password_hash(password=data.password)
        async with self._database.session() as session:
            try:
                user = await self._repo.create(session=session, data=data)
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
