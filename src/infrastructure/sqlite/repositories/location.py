import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.location import Location
from src.schemas.location import LocationRequestSchema


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, id: uuid.UUID) -> Location:
        query = select(self._model).where(self._model.id == id)
        location = session.scalar(query)
        return location

    def create(
        self, session: Session, data: LocationRequestSchema
    ) -> Location:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        location = session.scalar(query)

        return location

    def update(
        self, session: Session, id: uuid.UUID, data: LocationRequestSchema
    ) -> Location:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        location = session.scalar(query)

        return location

    def delete(self, session: Session, id: uuid.UUID):
        query = delete(self._model).where(self._model.id == id)
        session.execute(query)

