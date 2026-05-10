import uuid
from datetime import datetime, timezone
from typing import Type, cast

from sqlalchemy import CursorResult, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
)
from application.infrastructure.postgress.models.category import (
    Category as CategoryModel,
)
from application.infrastructure.postgress.models.comment import (
    Comment as CommentModel,
)
from application.infrastructure.postgress.models.location import (
    Location as LocationModel,
)
from application.infrastructure.postgress.models.post import (
    Post as PostModel,
)
from application.infrastructure.postgress.models.user import (
    User as UserModel,
)
from application.schemas.post import (
    PostRequestAdminSchema,
    PostRequestSchema,
    PostUpdateAdminSchema,
    PostUpdateSchema,
)
from application.schemas.user import UserResponseSchema


class PostRepository:
    def __init__(self) -> None:
        self._model: Type[PostModel] = PostModel
        self._author_model: Type[UserModel] = UserModel
        self._location_model: Type[LocationModel] = LocationModel
        self._category_model: Type[CategoryModel] = CategoryModel
        self._comments_model: Type[CommentModel] = CommentModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> PostModel:
        query = select(self._model).where(self._model.id == id)
        post = await session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    async def get_published(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        current_user: UserResponseSchema | None = None,
    ) -> PostModel:
        query = select(self._model).where(
            (self._model.id == id) & (self._model.is_published)
        )

        if current_user:
            query = query.where(
                (self._model.pub_date <= datetime.now(timezone.utc))
                | (self._model.author_id == current_user.id)
            )
        else:
            query = query.where(
                self._model.pub_date <= datetime.now(timezone.utc)
            )

        post = await session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    async def get_comments(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[CommentModel]:
        query = select(self._model).where(self._model.id == id)
        post = await session.scalar(query)

        if not post:
            raise PostNotFoundException()

        query = (
            select(self._comments_model)
            .where(self._comments_model.post_id == id)
            .order_by(self._comments_model.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        comments = (await session.scalars(query)).all()
        return list(comments)

    async def get_published_comments(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[CommentModel]:
        await self.get_published(session=session, id=id)
        query = (
            select(self._comments_model)
            .where(
                (self._comments_model.post_id == id)
                & (self._comments_model.is_published)
            )
            .order_by(self._comments_model.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        comments = (await session.scalars(query)).all()
        return list(comments)

    async def create(
        self,
        session: AsyncSession,
        data: PostRequestSchema | PostRequestAdminSchema,
        author_id: int,
    ) -> PostModel:
        if data.location_id:
            location = await session.get(self._location_model, data.location_id)
            if not location or not location.is_published:
                raise LocationNotFoundException()

        if data.category_id:
            category = await session.get(self._category_model, data.category_id)
            if not category or not category.is_published:
                raise CategoryNotFoundException()

        query = (
            insert(self._model)
            .values(**data.model_dump(exclude_none=True), author_id=author_id)
            .returning(self._model)
        )
        post = await session.scalar(query)

        return post  # pyright: ignore[reportReturnType]

    async def update(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        data: PostUpdateSchema | PostUpdateAdminSchema,
    ) -> PostModel:
        post = await session.get(self._model, id)
        if not post:
            raise PostNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if (
            'location_id' in update_data
            and update_data['location_id'] != post.location_id
        ):
            location = await session.get(
                self._location_model, update_data['location_id']
            )
            if not location or not location.is_published:
                raise LocationNotFoundException()

        if (
            'category_id' in update_data
            and update_data['category_id'] != post.category_id
        ):
            category = await session.get(
                self._category_model, update_data['category_id']
            )
            if not category or not category.is_published:
                raise CategoryNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(**update_data)
            .returning(self._model)
        )
        post = await session.scalar(query)

        return post  # pyright: ignore[reportReturnType]

    async def delete(self, session: AsyncSession, id: uuid.UUID) -> None:
        query = delete(self._model).where(self._model.id == id)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise PostNotFoundException()
