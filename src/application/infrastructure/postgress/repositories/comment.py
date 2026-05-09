from typing import Type, cast
from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.infrastructure.postgress.models.comment import (
    Comment as CommentModel,
)
from application.infrastructure.postgress.models.user import User as UserModel
from application.infrastructure.postgress.models.post import Post as PostModel
from application.schemas.comment import CommentRequestSchema


class CommentRepository:
    def __init__(self) -> None:
        self._model: Type[CommentModel] = CommentModel
        self._author_model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, id: int) -> CommentModel:
        query = select(self._model).where(self._model.id == id)
        comment = await session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        return comment

    async def create(
        self, session: AsyncSession, data: CommentRequestSchema, author_id: int
    ) -> CommentModel:
        post = await session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(**data.model_dump(exclude_none=True), author_id=author_id)
            .returning(self._model)
        )
        comment = await session.scalar(query)

        return comment  # pyright: ignore[reportReturnType]

    async def update(
        self, session: AsyncSession, id: int, data: CommentRequestSchema
    ) -> CommentModel:
        comment = await session.get(self._model, id)
        if not comment:
            raise CommentNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if (
            'post_id' in update_data
            and update_data['post_id'] != comment.post_id
        ):
            post = await session.get(self._post_model, update_data['post_id'])
            if not post:
                raise PostNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(**update_data)
            .returning(self._model)
        )
        comment = await session.scalar(query)

        return comment  # pyright: ignore[reportReturnType]

    async def delete(self, session: AsyncSession, id: int) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise CommentNotFoundException()
