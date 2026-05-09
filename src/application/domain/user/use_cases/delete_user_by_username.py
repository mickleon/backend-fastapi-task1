import logging

from application.core.exceptions.auth_exceptions import AccessDeniedException
from application.core.exceptions.database_exceptions import (
    UserNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.user import (
    UserRepository,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class DeleteUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, target_username: str, current_user: UserResponseSchema
    ) -> None:
        if not current_user.is_admin:
            error = AccessDeniedException()
            logger.error(
                f'Доступ запрещен: пользователь {current_user.username} попытался удалить пользователя {target_username}'
            )
            raise error
        async with self._database.session() as session:
            try:
                await self._repo.delete(
                    session=session, username=target_username
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
