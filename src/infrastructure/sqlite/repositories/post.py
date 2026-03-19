import uuid
from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.post import Post
from src.schemas.post import PostRequestSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, id: uuid.UUID) -> Post:
        query = select(self._model).where(self._model.id == id)
        post = session.scalar(query)
        return post

    def create(self, session: Session, data: PostRequestSchema) -> Post:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def update(
        self, session: Session, id: uuid.UUID, data: PostRequestSchema
    ) -> Post:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        post = session.scalar(query)

        return post

    def delete(self, session: Session, id: uuid.UUID):
        query = delete(self._model).where(self._model.id == id)
        session.execute(query)
