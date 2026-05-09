from typing import Type, cast

from sqlalchemy import CursorResult, delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)
from application.infrastructure.postgress.models.post import (
    Post as PostModel,
)
from application.infrastructure.postgress.models.user import (
    User as UserModel,
)
from application.schemas.user import UserRequestSchema


class UserRepository:
    def __init__(self) -> None:
        self._model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    async def get(self, session: AsyncSession, username: str) -> UserModel:
        query = select(self._model).where(self._model.username == username)
        user = await session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    async def get_posts(
        self,
        session: AsyncSession,
        username: str,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.username == username)
        user = await session.scalar(query)

        if not user:
            raise UserNotFoundException()

        query = (
            select(self._post_model)
            .where(self._post_model.author_id == user.id)
            .order_by(self._post_model.pub_date.desc())
            .offset(offset)
            .limit(limit)
        )
        posts = (await session.scalars(query)).all()
        return list(posts)

    async def create(
        self, session: AsyncSession, data: UserRequestSchema
    ) -> UserModel:
        existing_user = await session.scalar(
            select(self._model).where(
                or_(
                    self._model.username == data.username,
                    self._model.email == data.email,
                )
            )
        )

        if existing_user is not None:
            if existing_user.username == data.username:
                raise UserUsernameAlreadyExistsException()
            elif existing_user.email == data.email:
                raise UserEmailAlreadyExistsException()

        query = (
            insert(self._model)
            .values(**data.model_dump())
            .returning(self._model)
        )
        user = await session.scalar(query)

        return user  # pyright: ignore[reportReturnType]

    async def update(
        self, session: AsyncSession, username: str, data: UserRequestSchema
    ) -> UserModel:
        user = await self.get(session=session, username=username)

        if data.email and data.email != user.email:
            existing_email = await session.scalar(
                select(self._model).where(
                    self._model.email == data.email,
                    self._model.username != username,
                )
            )
            if existing_email:
                raise UserEmailAlreadyExistsException()

        if data.username and data.username != user.username:
            existing_username = await session.scalar(
                select(self._model).where(
                    self._model.username == data.username,
                    self._model.username != username,
                )
            )
            if existing_username:
                raise UserUsernameAlreadyExistsException()

        user_data = data.model_dump(exclude_unset=True)

        if 'password' in user_data:
            user_data['password'] = user_data['password']

        query = (
            update(self._model)
            .where(self._model.username == username)
            .values(**user_data)
            .returning(self._model)
        )
        user = await session.scalar(query)

        return user  # pyright: ignore[reportReturnType]

    async def delete(self, session: AsyncSession, username: str) -> None:
        query = delete(self._model).where(self._model.username == username)
        result = cast(CursorResult, await session.execute(query))

        if not result.rowcount:
            raise UserNotFoundException()
