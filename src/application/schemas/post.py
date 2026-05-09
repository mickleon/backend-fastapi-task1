import uuid
from datetime import datetime, timezone

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from application.resources.field_description import (
    AUTHOR_ID,
    CATEGORY_ID,
    CREATED_AT,
    HAS_NEXT,
    IMAGE_URL,
    IS_PUBLISHED,
    LOCATION_ID,
    POST_ID,
    POST_LIST_ITEMS,
    PUB_DATE,
    TEXT,
    TITLE,
)


class PostBaseSchema(BaseModel):
    title: str = Field(max_length=256, description=TITLE)
    text: str = Field(max_length=5000, description=TEXT)
    pub_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description=PUB_DATE,
    )

    location_id: uuid.UUID | None = Field(default=None, description=LOCATION_ID)
    category_id: uuid.UUID | None = Field(default=None, description=CATEGORY_ID)
    image_url: AnyUrl | None = Field(default=None, description=IMAGE_URL)

    is_published: bool = Field(default=True, description=IS_PUBLISHED)


class PostRequestSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    id: uuid.UUID = Field(description=POST_ID)
    author_id: int = Field(description=AUTHOR_ID)
    created_at: datetime = Field(description=CREATED_AT)

    model_config = ConfigDict(from_attributes=True)


class PostsPageResponseSchema(BaseModel):
    items: list[PostResponseSchema] = Field(
        default_factory=list, description=POST_LIST_ITEMS
    )
    has_next: bool = Field(description=HAS_NEXT)
