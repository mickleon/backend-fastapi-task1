import uuid
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from src.resources.field_description import (
    AUTHOR_ID,
    CREATED_AT,
    POST_ID,
    TEXT,
)


class CommentBaseSchema(BaseModel):
    text: str = Field(max_length=5000, description=TEXT)
    post_id: uuid.UUID = Field(description=POST_ID)
    author_id: int = Field(description=AUTHOR_ID)


class CommentRequestSchema(CommentBaseSchema):
    pass


class CommentResponseSchema(CommentBaseSchema):
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)
