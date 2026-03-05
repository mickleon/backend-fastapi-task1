import uuid
from typing import Type
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.comment import Comment
from src.schemas.comment import CommentRequestSchema


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get(self, session: Session, id: uuid.UUID) -> Comment:
        query = session.query(self._model).where(self._model.id == id)

        return query.scalar()

    def create(self, session: Session, comment: Comment) -> Comment:
        session.add(comment)
        session.commit()

        return comment

    def update(self, session: Session, comment: Comment, data: CommentRequestSchema):
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(comment, field, value)
        session.commit()

        return comment

    def delete(self, session: Session, comment: Comment):
        session.delete(comment)
        session.commit()

