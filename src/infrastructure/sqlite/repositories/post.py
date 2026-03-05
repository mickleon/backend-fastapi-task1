import uuid
from typing import Type
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.post import Post
from src.schemas.post import PostRequestSchema


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get(self, session: Session, id: uuid.UUID) -> Post:
        query = session.query(self._model).where(self._model.id == id)

        return query.scalar()

    def create(self, session: Session, post: Post) -> Post:
        session.add(post)
        session.commit()

        return post

    def update(self, session: Session, post: Post, data: PostRequestSchema):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(post, field, value)
        session.commit()

        return post

    def delete(self, session: Session, post: Post):
        session.delete(post)
        session.commit()

