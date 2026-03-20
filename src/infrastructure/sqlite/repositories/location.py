import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import LocationNotFoundException
from src.infrastructure.sqlite.models.location import Location as LocationModel
from src.schemas.location import LocationRequestSchema


class LocationRepository:
    def __init__(self) -> None:
        self._model: Type[LocationModel] = LocationModel

    def get(self, session: Session, id: uuid.UUID) -> LocationModel:
        query = select(self._model).where(self._model.id == id)
        location = session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    def create(
        self, session: Session, data: LocationRequestSchema
    ) -> LocationModel:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        location = session.scalar(query)

        return location

    def update(
        self, session: Session, id: uuid.UUID, data: LocationRequestSchema
    ) -> LocationModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        location = session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    def delete(self, session: Session, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = session.execute(query)

        if not result.rowcount:
            raise LocationNotFoundException()
