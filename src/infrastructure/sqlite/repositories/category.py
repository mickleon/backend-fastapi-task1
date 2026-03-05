import uuid
from typing import Type
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.category import Category
from src.schemas.category import CategoryRequestSchema


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def get(self, session: Session, id: uuid.UUID) -> Category:
        query = session.query(self._model).where(self._model.id == id)

        return query.scalar()

    def create(self, session: Session, category: Category) -> Category:
        session.add(category)
        session.commit()

        return category

    def update(self, session: Session, category: Category, data: CategoryRequestSchema):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(category, field, value)
        session.commit()

        return category

    def delete(self, session: Session, category: Category):
        session.delete(category)
        session.commit()

