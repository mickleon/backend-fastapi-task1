from pydantic import BaseModel, Field
from datetime import datetime


class CommentRequestSchema(BaseModel):
    text: str = Field(description='Текст')
    post_id: int = Field(description='ID публикации')


class CommentResponseSchema(BaseModel):
    text: str = Field(description='Текст')
    post_id: int = Field(description='ID публикации')
    author_id: int = Field(description='ID автора')
    created_at: datetime = Field(description='Дата и время создания')
