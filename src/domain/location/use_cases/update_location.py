import logging
import uuid

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.core.exceptions.domain_exceptions import LocationNotFoundByIdException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationRequestSchema, LocationResponseSchema
from src.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self,
        id: uuid.UUID,
        data: LocationRequestSchema,
        current_user: UserResponseSchema,
    ) -> LocationResponseSchema:
        with self._database.session() as session:
            try:
                location = self._repo.update(session=session, id=id, data=data)
            except LocationNotFoundException:
                error = LocationNotFoundByIdException(id=id)
                username = current_user.username
                logger.error(
                    f'Пользователь {username} довел приложение до ошибки: {error.get_detail()}'
                )
                raise error

            return LocationResponseSchema.model_validate(obj=location)
