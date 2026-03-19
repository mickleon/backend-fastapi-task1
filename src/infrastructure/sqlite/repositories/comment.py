from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    PostNotFoundException,
    UserNotFoundException,
)
from src.infrastructure.sqlite.models.comment import Comment as CommentModel
from src.infrastructure.sqlite.models.user import User as UserModel
from src.infrastructure.sqlite.models.post import Post as PostModel
from src.schemas.comment import CommentRequestSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel
        self._author_model: Type[UserModel] = UserModel
        self._post_model: Type[PostModel] = PostModel

    def get(self, session: Session, id: int) -> CommentModel:
        query = select(self._model).where(self._model.id == id)
        comment = session.scalar(query)

        if not comment:
            raise CommentNotFoundException()

        return comment

    def create(
        self, session: Session, data: CommentRequestSchema
    ) -> CommentModel:
        author = session.get(self._author_model, data.author_id)
        if not author:
            raise UserNotFoundException()

        post = session.get(self._post_model, data.post_id)
        if not post:
            raise PostNotFoundException()

        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def update(
        self, session: Session, id: int, data: CommentRequestSchema
    ) -> CommentModel:
        comment = session.get(self._model, id)
        if not comment:
            raise CommentNotFoundException()

        update_data = data.model_dump(exclude_unset=True)

        if (
            'author_id' in update_data
            and update_data['author_id'] != comment.author_id
        ):
            author = session.get(self._author_model, update_data['author_id'])
            if not author:
                raise UserNotFoundException()

        if (
            'post_id' in update_data
            and update_data['post_id'] != comment.post_id
        ):
            post = session.get(self._post_model, update_data['post_id'])
            if not post:
                raise PostNotFoundException()

        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def delete(self, session: Session, id: int):
        query = (
            delete(self._model)
            .where(self._model.id == id)
            .returning(self._model)
        )
        comment = session.scalar(query)

        if not comment:
            raise CommentNotFoundException()
