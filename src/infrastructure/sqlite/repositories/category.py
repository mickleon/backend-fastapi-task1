import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import CategoryNotFoundException
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.category import CategoryRequestSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get(self, session: Session, id: uuid.UUID) -> CategoryModel:
        query = select(self._model).where(self._model.id == id)
        category = session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    def create(
        self, session: Session, data: CategoryRequestSchema
    ) -> CategoryModel:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        return category

    def update(
        self, session: Session, id: uuid.UUID, data: CategoryRequestSchema
    ) -> CategoryModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        category = session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    def delete(self, session: Session, id: uuid.UUID):
        query = delete(self._model).where(self._model.id == id)
        result = session.execute(query)

        if not result.rowcount:
            raise CategoryNotFoundException()
