from typing import Type, cast
from sqlalchemy import CursorResult, insert, or_, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.user import UserRequestSchema
from src.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)


class UserRepository:
    def __init__(self) -> None:
        self._model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    def get(self, session: Session, username: str) -> UserModel:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def get_posts(
        self,
        session: Session,
        username: str,
        offset: int,
        limit: int,
    ) -> list[PostModel]:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        query = (
            select(self._post_model)
            .where(self._post_model.author_id == user.id)
            .order_by(self._post_model.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        posts = session.scalars(query).all()
        return list(posts)

    def create(self, session: Session, data: UserRequestSchema) -> UserModel:
        existing_user = session.scalar(
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
        user = session.scalar(query)

        return user

    def update(
        self, session: Session, username: str, data: UserRequestSchema
    ) -> UserModel:
        user = self.get(session=session, username=username)

        if data.email and data.email != user.email:
            existing_email = session.scalar(
                select(self._model).where(
                    self._model.email == data.email,
                    self._model.username != username,
                )
            )
            if existing_email:
                raise UserEmailAlreadyExistsException()

        if data.username and data.username != user.username:
            existing_username = session.scalar(
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
        user = session.scalar(query)

        return user

    def delete(self, session: Session, username: str) -> None:
        query = delete(self._model).where(self._model.username == username)
        result = cast(CursorResult, session.execute(query))

        if not result.rowcount:
            raise UserNotFoundException()
