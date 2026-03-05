import uuid
from fastapi import HTTPException

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
            location = self._repo.get(session=session, id=id)

            if location is None:
                raise HTTPException(
                    status_code=404, detail=f'Местоположение с id "{id}" не найдено'
                )

            self._repo.update(session=session, location=location, data=data)

        return LocationResponseSchema.model_validate(obj=location)

