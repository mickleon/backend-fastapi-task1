import uuid
from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    LocationNotFoundException,
)
from application.infrastructure.postgress.models.location import (
    Location as LocationModel,
)
from application.infrastructure.postgress.models.post import Post as PostModel
from application.schemas.location import LocationRequestSchema


class LocationRepository:
    def __init__(self) -> None:
        self._model: Type[LocationModel] = LocationModel
        self._post_model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> LocationModel:
        query = select(self._model).where(self._model.id == id)
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        return location

    async def get_posts_published(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        query = select(self._model).where(
            (self._model.id == id) & (self._model.is_published)
        )

        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        query = (
            select(self._post_model)
            .where(
                (self._post_model.is_published)
                & (self._post_model.location_id == id)
                & (self._post_model.pub_date <= datetime.now(timezone.utc))
            )
            .order_by(self._post_model.pub_date.desc())
            .offset(offset)
            .limit(limit)
        )

        posts = (await session.scalars(query)).all()
        return list(posts)

    async def get_posts(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.id == id)
        location = await session.scalar(query)

        if not location:
            raise LocationNotFoundException()

        query = (
            select(self._post_model)
            .where(self._post_model.location_id == id)
            .order_by(self._post_model.pub_date.desc())
            .offset(offset)
            .limit(limit)
        )
        posts = (await session.scalars(query)).all()
        return list(posts)

    async def create(
        self, session: AsyncSession, data: LocationRequestSchema
    ) -> LocationModel:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        location = await session.scalar(query)

        return location  # pyright: ignore[reportReturnType]

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
