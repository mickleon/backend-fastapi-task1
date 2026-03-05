import uuid
from typing import Type
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.location import Location
from src.schemas.location import LocationRequestSchema


class LocationRepository:
    def __init__(self):
        self._model: Type[Location] = Location

    def get(self, session: Session, id: uuid.UUID) -> Location:
        query = session.query(self._model).where(self._model.id == id)

        return query.scalar()

    def create(self, session: Session, location: Location) -> Location:
        session.add(location)
        session.commit()

        return location

    def update(self, session: Session, location: Location, data: LocationRequestSchema):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(location, field, value)
        session.commit()

        return location

    def delete(self, session: Session, location: Location):
        session.delete(location)
        session.commit()

