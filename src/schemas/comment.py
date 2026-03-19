import uuid
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentBaseSchema(BaseModel):
    text: str = Field(max_length=5000, description='Текст')
    post_id: uuid.UUID = Field(description='ID публикации')
    author_id: int = Field(description='ID автора')


class CommentRequestSchema(CommentBaseSchema):
    pass


class CommentResponseSchema(CommentBaseSchema):
    created_at: datetime = Field(description='Дата и время создания')

    model_config = ConfigDict(from_attributes=True)
