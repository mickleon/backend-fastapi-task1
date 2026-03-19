from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationRequestSchema, LocationResponseSchema


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationRequestSchema):
        with self._database.session() as session:
            location = self._repo.create(session=session, data=data)

            return LocationResponseSchema.model_validate(obj=location)

