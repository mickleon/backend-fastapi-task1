import logging
import uuid

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
