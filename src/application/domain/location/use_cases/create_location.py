import logging
from application.core.exceptions.auth_exceptions import AccessDeniedException
from application.infrastructure.postgress.database import database
from application.infrastructure.postgress.repositories.location import (
    LocationRepository,
)
from application.schemas.location import (
    LocationRequestSchema,
    LocationResponseSchema,
)
from application.schemas.user import UserResponseSchema

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, data: LocationRequestSchema, current_user: UserResponseSchema
    ) -> LocationResponseSchema:
        if not current_user.is_admin:
            error = AccessDeniedException()
            logger.error(
                f'Доступ запрещен: пользователь {current_user.username} попытался создать местоположение'
            )
            raise error
        async with self._database.session() as session:
            location = await self._repo.create(session=session, data=data)

            return LocationResponseSchema.model_validate(obj=location)
