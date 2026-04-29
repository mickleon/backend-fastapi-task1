import uuid
from typing import Type, cast
from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.infrastructure.postgress.models.category import (
    Category as CategoryModel,
)
from application.schemas.category import CategoryRequestSchema


class CategoryRepository:
    def __init__(self) -> None:
        self._model: Type[CategoryModel] = CategoryModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> CategoryModel:
        query = select(self._model).where(self._model.id == id)
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def create(
        self, session: AsyncSession, data: CategoryRequestSchema
    ) -> CategoryModel:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        category = await session.scalar(query)

        return category  # pyright: ignore[reportReturnType]

    async def update(
        self, session: AsyncSession, id: uuid.UUID, data: CategoryRequestSchema
    ) -> CategoryModel:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def delete(self, session: AsyncSession, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise CategoryNotFoundException()
