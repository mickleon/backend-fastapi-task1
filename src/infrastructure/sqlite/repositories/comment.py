from typing import Type
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comment import CommentRequestSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, id: int) -> Comment:
        query = select(self._model).where(self._model.id == id)
        comment = session.scalar(query)
        return comment

    def create(self, session: Session, data: CommentRequestSchema) -> Comment:
        query = (
            insert(self._model)
            .values(data.model_dump(exclude_none=True))
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def update(
        self, session: Session, id: int, data: CommentRequestSchema
    ) -> Comment:
        query = (
            update(self._model)
            .where(self._model.id == id)
            .values(data.model_dump(exclude_unset=True))
            .returning(self._model)
        )
        comment = session.scalar(query)

        return comment

    def delete(self, session: Session, id: int):
        query = delete(self._model).where(self._model.id == id)
        session.execute(query)

