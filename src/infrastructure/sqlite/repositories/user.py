from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.user import User
from src.schemas.user import UserRequestSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, username: str) -> User:
        query = select(self._model).where(self._model.username == username)
        user = session.scalar(query)
        return user

    def create(self, session: Session, data: UserRequestSchema) -> User:
        user_data = {
            **data.model_dump(exclude={'password'}, exclude_none=True),
            'password': data.password.get_secret_value(),
        }
        query = insert(self._model).values(**user_data).returning(self._model)
        user = session.scalar(query)

        return user

    def update(
        self, session: Session, username: str, data: UserRequestSchema
    ) -> User:
        user_data = data.model_dump(exclude_unset=True)

        if 'password' in user_data:
            user_data['password'] = user_data['password'].get_secret_value()

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
        session.execute(query)

