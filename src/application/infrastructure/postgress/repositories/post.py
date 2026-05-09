import uuid
from typing import Type, cast
from sqlalchemy import CursorResult, insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    CategoryNotFoundException,
    LocationNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from application.infrastructure.postgress.models.post import (
    Post as PostModel,
)
from application.infrastructure.postgress.models.user import (
    User as UserModel,
)
from application.infrastructure.postgress.models.location import (
    Location as LocationModel,
)
from application.infrastructure.postgress.models.category import (
    Category as CategoryModel,
)
from application.schemas.post import PostRequestSchema


class PostRepository:
    def __init__(self) -> None:
        self._model: Type[PostModel] = PostModel
        self._author_model: Type[UserModel] = UserModel
        self._location_model: Type[LocationModel] = LocationModel
        self._category_model: Type[CategoryModel] = CategoryModel

    async def get(self, session: AsyncSession, id: uuid.UUID) -> PostModel:
        query = select(self._model).where(self._model.id == id)
        post = await session.scalar(query)

        if not post:
            raise PostNotFoundException()

        return post

    async def create(
        self, session: AsyncSession, data: PostRequestSchema, author_id: int
    ) -> PostModel:
        if data.location_id is not None:
            location = await session.get(self._location_model, data.location_id)
            if not location:
                raise LocationNotFoundException()

        if data.category_id is not None:
            category = await session.get(self._category_model, data.category_id)
            if not category:
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
        data: PostRequestSchema,
    ) -> PostModel:
        post = await session.get(self._model, id)
        if not post:
            raise PostNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if (
            'location_id' in update_data
            and update_data['location_id'] is not None
            and update_data['location_id'] != post.location_id
        ):
            location = await session.get(
                self._location_model, update_data['location_id']
            )
            if not location:
                raise LocationNotFoundException()

        if (
            'category_id' in update_data
            and update_data['category_id'] is not None
            and update_data['category_id'] != post.category_id
        ):
            category = await session.get(
                self._category_model, update_data['category_id']
            )
            if not category:
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
