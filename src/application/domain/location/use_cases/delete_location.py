import logging
import uuid

from application.core.exceptions.auth_exceptions import AccessDeniedException
from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.core.exceptions.domain_exceptions import (
    LocationNotFoundByIdException,
)
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.location import (
    LocationRepository,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, id: uuid.UUID, current_user: UserResponseSchema
    ) -> None:
        if not current_user.is_admin:
            error = AccessDeniedException()
            logger.error(
                f'Доступ запрещен: пользователь {current_user.username} попытался удалить местоположение с id {id}'
            )
            raise error
        async with self._database.session() as session:
            try:
                await self._repo.delete(session=session, id=id)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error
