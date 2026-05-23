import uuid
from typing import Type

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    ImageNotFoundException,
)
from application.infrastructure.postgress.models.image import (
    Image as ImageModel,
)


class ImageRepository:
    def __init__(self) -> None:
        self._model: Type[ImageModel] = ImageModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> ImageModel:
        image = await session.get(self._model, id)
        if not image:
            raise ImageNotFoundException()
        return image

    async def get_by_ids(
        self, session: AsyncSession, ids: list[uuid.UUID]
    ) -> list[ImageModel]:
        query = select(self._model).where(self._model.id.in_(ids))
        images = (await session.scalars(query)).all()
        return list(images)

    async def create(self, session: AsyncSession, path: str) -> ImageModel:
        query = insert(self._model).values(path=path).returning(self._model)
        image = await session.scalar(query)
        return image  # pyright: ignore[reportReturnType]

    async def bulk_create(
        self, session: AsyncSession, paths: list[str]
    ) -> list[ImageModel]:
        values = [{'path': path} for path in paths]
        query = insert(self._model).values(values).returning(self._model)
        images = (await session.scalars(query)).all()
        return list(images)

    async def associate_with_post(
        self,
        session: AsyncSession,
        image_ids: list[uuid.UUID],
        post_id: uuid.UUID,
    ) -> None:
        if not image_ids:
            return
        query = (
            update(self._model)
            .where(self._model.id.in_(image_ids))
            .values(post_id=post_id)
        )
        await session.execute(query)

    async def associate_with_comment(
        self,
        session: AsyncSession,
        image_ids: list[uuid.UUID],
        comment_id: uuid.UUID,
    ) -> None:
        if not image_ids:
            return
        query = (
            update(self._model)
            .where(self._model.id.in_(image_ids))
            .values(comment_id=comment_id)
        )
        await session.execute(query)

    async def dissociate_from_post(
        self, session: AsyncSession, post_id: uuid.UUID
    ) -> None:
        query = (
            update(self._model)
            .where(self._model.post_id == post_id)
            .values(post_id=None)
        )
        await session.execute(query)

    async def dissociate_from_comment(
        self, session: AsyncSession, comment_id: uuid.UUID
    ) -> None:
        query = (
            update(self._model)
            .where(self._model.comment_id == comment_id)
            .values(comment_id=None)
        )
        await session.execute(query)
