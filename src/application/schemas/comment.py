import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from application.resources.field_description import (
    AUTHOR_ID,
    COMMENT_ID,
    COMMENTS_LIST_ITEMS,
    CREATED_AT,
    HAS_NEXT,
    IS_PUBLISHED,
    POST_ID,
    TEXT,
)


class CommentUpdateSchema(BaseModel):
    text: str = Field(max_length=5000, description=TEXT)


class CommentRequestSchema(CommentUpdateSchema):
    post_id: uuid.UUID = Field(description=POST_ID)


class CommentRequestAdminSchema(CommentRequestSchema):
    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class CommentResponseSchema(CommentRequestAdminSchema):
    id: uuid.UUID = Field(description=COMMENT_ID)
    author_id: int = Field(description=AUTHOR_ID)
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)


class CommentsPageResponseSchema(BaseModel):
    items: list[CommentResponseSchema] = Field(
        default_factory=list, description=COMMENTS_LIST_ITEMS
    )
    has_next: bool = Field(description=HAS_NEXT)
