import logging

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
        async with self._database.session() as session:
            location = await self._repo.create(session=session, data=data)

            return LocationResponseSchema.model_validate(obj=location)
