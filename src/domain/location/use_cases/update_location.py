import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationRequestSchema, LocationResponseSchema


class UpdateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(
        self, id: uuid.UUID, data: LocationRequestSchema
    ) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.update(session=session, id=id, data=data)

            return LocationResponseSchema.model_validate(obj=location)

