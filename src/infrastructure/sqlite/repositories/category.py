import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.category import Category
from src.schemas.category import CategoryRequestSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, id: uuid.UUID) -> Category:
        query = select(self._model).where(self._model.id == id)
        category = session.scalar(query)
        return category

    def create(
        self, session: Session, data: CategoryRequestSchema
    ) -> Category:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        return category

    def update(
        self, session: Session, id: uuid.UUID, data: CategoryRequestSchema
    ) -> Category:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        return category

    def delete(self, session: Session, id: uuid.UUID):
        query = delete(self._model).where(self._model.id == id)
        session.execute(query)
