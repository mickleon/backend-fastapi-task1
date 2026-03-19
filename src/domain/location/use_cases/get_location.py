import uuid

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationResponseSchema


class GetLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, id: uuid.UUID) -> LocationResponseSchema:
        with self._database.session() as session:
            location = self._repo.get(session=session, id=id)

            return LocationResponseSchema.model_validate(obj=location)

