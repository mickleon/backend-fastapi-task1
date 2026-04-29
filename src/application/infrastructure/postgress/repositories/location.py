import uuid
from typing import Type, cast
from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.infrastructure.postgress.models.location import (
    Location as LocationModel,
)
from application.schemas.location import LocationRequestSchema


class LocationRepository:
    def __init__(self) -> None:
        self._model: Type[LocationModel] = LocationModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> LocationModel:
        query = select(self._model).where(self._model.id == id)
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    async def create(
        self, session: AsyncSession, data: LocationRequestSchema
    ) -> LocationModel:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        location = await session.scalar(query)

        return location

    async def update(
        self, session: AsyncSession, id: uuid.UUID, data: LocationRequestSchema
    ) -> LocationModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    async def delete(self, session: AsyncSession, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise LocationNotFoundException()
