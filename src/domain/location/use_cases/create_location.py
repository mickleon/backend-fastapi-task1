from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.models.location import Location
from src.infrastructure.sqlite.repositories.location import LocationRepository
from src.schemas.location import LocationRequestSchema, LocationResponseSchema


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, data: LocationRequestSchema):
        with self._database.session() as session:
            location = Location(**data.model_dump())
            self._repo.create(session=session, location=location)

        return LocationResponseSchema.model_validate(obj=location)

