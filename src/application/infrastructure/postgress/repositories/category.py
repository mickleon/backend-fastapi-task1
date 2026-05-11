import uuid
from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
)
from application.infrastructure.postgress.models.category import (
    Category as CategoryModel,
)
from application.infrastructure.postgress.models.post import Post as PostModel
from application.schemas.category import CategoryRequestSchema


class CategoryRepository:
    def __init__(self) -> None:
        self._model: Type[CategoryModel] = CategoryModel
        self._post_model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> CategoryModel:
        query = select(self._model).where(self._model.id == id)
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        return category

    async def get_posts(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.id == id)
        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        query = (
            select(self._post_model)
            .where(self._post_model.category_id == id)
            .order_by(self._post_model.pub_date.desc())
            .offset(offset)
            .limit(limit)
        )
        posts = (await session.scalars(query)).all()
        return list(posts)

    async def get_posts_published(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        """
        Возвращаются только те публикации, которые:
        - принадлежат выбранной категории,
        - значение поля is_published равно True,
        - дата публикации не позже текущего времени.
        """
        query = select(self._model).where(
            (self._model.id == id) & (self._model.is_published)
        )

        category = await session.scalar(query)

        if not category:
            raise CategoryNotFoundException()

        query = (
            select(self._post_model)
            .where(
                (self._post_model.is_published)
                & (self._post_model.category_id == id)
                & (self._post_model.pub_date <= datetime.now(timezone.utc))
            )
            .order_by(self._post_model.pub_date.desc())
            .offset(offset)
            .limit(limit)
        )

        posts = (await session.scalars(query)).all()
        return list(posts)

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
