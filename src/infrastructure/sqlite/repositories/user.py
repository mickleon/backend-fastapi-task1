from typing import Type
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.user import User
from src.schemas.user import UserRequestSchema


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get(self, session: Session, username: str) -> User:
        query = session.query(self._model).where(self._model.username == username)

        return query.scalar()

    def create(self, session: Session, user: User) -> User:
        session.add(user)
        session.commit()

        return user

    def update(self, session: Session, user: User, data: UserRequestSchema):
        for field, value in data.model_dump(
            exclude_none=True, exclude={'password'}
        ).items():
            setattr(user, field, value)
        session.commit()

        if data.password is not None:
            user.password = data.password.get_secret_value()

        return user

    def delete(self, session: Session, user: User):
        session.delete(user)
        session.commit()

        return user
