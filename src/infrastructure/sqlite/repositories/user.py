from typing import Type
from sqlalchemy import insert, or_, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.user import User as UserModel
from src.schemas.user import UserRequestSchema
from src.core.exceptions.database_exceptions import (
    UserEmailAlreadyExistsException,
    UserNotFoundException,
    UserUsernameAlreadyExistsException,
)


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get(self, session: Session, username: str) -> UserModel:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)

        if not user:
            raise UserNotFoundException()

        return user

    def create(self, session: Session, data: UserRequestSchema) -> UserModel:
        existing_user = session.scalar(
            select(self._model).where(
                or_(
                    self._model.username == data.username,
                    self._model.email == data.email,
                )
            )
        )

        if existing_user:
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

    def delete(self, session: Session, username: str):
        query = delete(self._model).where(self._model.username == username)
        result = session.execute(query)

        if not result.rowcount:
            raise UserNotFoundException()
