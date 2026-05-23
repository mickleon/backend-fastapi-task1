import uuid
from typing import Type, cast

from sqlalchemy import CursorResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
)
from application.infrastructure.postgress.models.comment import (
    Comment as CommentModel,
)
from application.infrastructure.postgress.models.post import Post as PostModel
from application.infrastructure.postgress.models.user import User as UserModel
from application.infrastructure.postgress.repositories.image import (
    ImageRepository,
)
from application.infrastructure.postgress.repositories.post import (
    PostRepository,
)
from application.schemas.comment import (
    CommentRequestAdminSchema,
    CommentRequestSchema,
    CommentUpdateSchema,
)


class CommentRepository:
    def __init__(self) -> None:
        self._post_repository = PostRepository()
        self._model: Type[CommentModel] = CommentModel
        self._author_model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel
        self._image_repo = ImageRepository()

    async def get(self, session: AsyncSession, id: uuid.UUID) -> CommentModel:
        query = select(self._model).where(self._model.id == id)
        comment = await session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        return comment

    async def get_published(
        self, session: AsyncSession, id: uuid.UUID
    ) -> CommentModel:
        query = select(self._model).where(
            (self._model.id == id) & (self._model.is_published)
        )
        comment = await session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        post = await self._post_repository.get_published(
            session=session, id=comment.post_id
        )

        if not post:
            raise CommentNotFoundException()

        return comment

    async def create(
        self,
        session: AsyncSession,
        data: CommentRequestSchema | CommentRequestAdminSchema,
        author_id: int,
    ) -> CommentModel:
        post = await self._post_repository.get(session=session, id=data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(
                **data.model_dump(exclude_none=True, exclude={'image_ids'}),
                author_id=author_id,
            )
            .returning(self._model)
        )
        comment = await session.scalar(query)

        if data.image_ids:
            await self._image_repo.validate_exist(
                session=session, ids=data.image_ids
            )
            await self._image_repo.associate_with_comment(
                session=session,
                image_ids=data.image_ids,
                comment_id=comment.id,  # pyright: ignore[reportArgumentType]
            )

        await session.refresh(comment, ['images'])
        return comment  # pyright: ignore[reportReturnType]

    async def create_published(
        self, session: AsyncSession, data: CommentRequestSchema, author_id: int
    ) -> CommentModel:
        post = await self._post_repository.get_published(
            session=session, id=data.post_id
        )
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(
                **data.model_dump(exclude_none=True, exclude={'image_ids'}),
                author_id=author_id,
            )
            .returning(self._model)
        )
        comment = await session.scalar(query)

        if data.image_ids:
            await self._image_repo.validate_exist(
                session=session, ids=data.image_ids
            )
            await self._image_repo.associate_with_comment(
                session=session,
                image_ids=data.image_ids,
                comment_id=comment.id,  # pyright: ignore[reportArgumentType]
            )

        await session.refresh(comment, ['images'])
        return comment  # pyright: ignore[reportReturnType]

    async def update(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        data: CommentUpdateSchema | CommentRequestAdminSchema,
    ) -> CommentModel:
        comment = await self.get(session=session, id=id)
        if not comment:
            raise CommentNotFoundException()

        update_data = data.model_dump(
            exclude_unset=True, exclude={'post_id', 'image_ids'}
        )

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(**update_data)
            .returning(self._model)
        )
        comment = await session.scalar(query)

        if 'image_ids' in data.model_dump(exclude_unset=True):
            await self._image_repo.dissociate_from_comment(
                session=session, comment_id=id
            )
            if data.image_ids:
                await self._image_repo.validate_exist(
                    session=session, ids=data.image_ids
                )
                await self._image_repo.associate_with_comment(
                    session=session,
                    image_ids=data.image_ids,
                    comment_id=id,
                )

        await session.refresh(comment, ['images'])
        return comment  # pyright: ignore[reportReturnType]

    async def delete(self, session: AsyncSession, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise CommentNotFoundException()
